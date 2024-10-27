"""
Go-Back-N transmission protocol in networking.
Author: Máximo Flores Valenzuela [https://github.com/maxfloresv].
"""

import threading
import time
import jsockets
import sys

# Controls the maximum sequence number possible
MAX_SEQ_NUM = 65535
# Controls the adaptative timeout factor (this will be multiplied with the RTT)
TIMEOUT_FACTOR = 3

mutex = threading.Lock()
condition = threading.Condition(lock=mutex)
timeout = 0.5

# Primer paquete de la ventana
base = 0
next_seq_num = 0
last_ack_received = -1
# Buffer que guarda el contenido de los paquetes
buffer = {}
# Timers de la forma [start, end] para cada paquete
timers = {}
transmission_finished = False
transmission_errors = 0
reception_errors = 0
received_bytes = 0

def convert_to_bytes(num: int) -> bytes:
    """
    Converts a number to its byte representation (2 bytes: [0...2^16 - 1]), using big-endian.
    """
    return num.to_bytes(2, byteorder='big')

def convert_from_bytes(bytes: bytes) -> int:
    """
    Converts 2 bytes to its integer result.
    """
    return int.from_bytes(bytes, byteorder='big')

def receiver(s):
    """
    Reception thread in packet transmission
    """
    global base, received_bytes, reception_errors, transmission_finished, last_ack_received
    while True:
        try:
            data = s.recv(PACK_SZ)
        except:
            data = None
        if not data:
            break
        last_recv_packet = convert_from_bytes(data[:2])
        # El receptor sólo puede aceptar si el paquete es el sucesor del último ACK recibido.
        if last_recv_packet == (last_ack_received + 1) % (MAX_SEQ_NUM + 1):
            timers[last_recv_packet].append(time.time())
            # Estamos recibiendo sólo un número de secuencia
            if len(data) == 2:
                with condition:
                  transmission_finished = True
                  condition.notify()
                break
            sys.stdout.buffer.write(data[2:])
            received_bytes += len(data[2:])
            last_ack_received = (last_ack_received + 1) % (MAX_SEQ_NUM + 1)
            with condition:
                # Deslizamos la ventana cuando confirmamos un paquete que está contenido en ella.
                # El invariante de Go-Back-N es ACK_n => ACK_i para todo i <= n. Para esto,
                # hay que considerar que el último ACK recibido coincida con el último paquete recibido.
                if (base <= last_recv_packet < next_seq_num) \
                    or (base > next_seq_num and (base <= last_recv_packet or 0 <= last_recv_packet < next_seq_num)):
                    base = (last_recv_packet + 1) % (MAX_SEQ_NUM + 1)
                    condition.notify()
                else:
                    # El paquete se recibió fuera de la ventana
                    reception_errors += 1
        else:
            # El paquete se recibió fuera de orden dentro de la ventana
            reception_errors += 1
                
def sender(s):
    """
    Sender thread in packet transmission
    """
    global base, next_seq_num, timeout, transmission_errors

    while not transmission_finished:
        with condition:
            # Packets are emitted only while being inside the window.
            while (next_seq_num < (base + WIN) % (MAX_SEQ_NUM + 1)) \
                or (next_seq_num > (base + WIN) % (MAX_SEQ_NUM + 1) and (next_seq_num <= MAX_SEQ_NUM)):
                data = sys.stdin.buffer.read(PACK_SZ - 2)
                packet = convert_to_bytes(next_seq_num) + data
                # It's not necessary to delete the old packet status. It's overwritten every time.
                buffer[next_seq_num] = packet
                timers[next_seq_num] = [time.time()]
                s.send(buffer[next_seq_num])
                next_seq_num = (next_seq_num + 1) % (MAX_SEQ_NUM + 1)

            # Wait for an ACK or a timeout. Consider that the sender has access (through mutex) to the receiver window.
            result = condition.wait(timeout=timeout)
            if result:
                # This is the very last packet that received an ACK.
                last_recv_packet = (base - 1) % (MAX_SEQ_NUM + 1)
                [start, end] = timers[last_recv_packet]
                RTT = end - start
                timeout = TIMEOUT_FACTOR * RTT
            else:
                # Las retransmisiones pueden ocurrir más de una vez, dado que en dicho caso, next_seq_num
                # no es modificado, entonces la condición del while de arriba sigue incumpliéndose.
                transmission_errors += 1
                if base <= next_seq_num:
                    for seq in range(base, next_seq_num):
                        # Debemos actualizar la medición del RTT por la retransmisión
                        timers[seq][0] = time.time()
                        s.send(buffer[seq])
                else:
                    for seq in list(range(base, MAX_SEQ_NUM + 1)) + list(range(0, next_seq_num)):
                        timers[seq][0] = time.time()
                        s.send(buffer[seq])

if len(sys.argv) != 5:
    print(f'Use: {sys.argv[0]} pack_sz win host port', file=sys.stderr)
    sys.exit(1)

PACK_SZ = int(sys.argv[1])
WIN = int(sys.argv[2])

print(f"Using pack: {PACK_SZ}, maxwin: {WIN}", file=sys.stderr)

s = jsockets.socket_udp_connect(sys.argv[3], sys.argv[4])
if s is None:
    print("Couldn't open socket", file=sys.stderr)
    sys.exit(1)

recv_thread = threading.Thread(target=receiver, args=(s,))
send_thread = threading.Thread(target=sender, args=(s,))

recv_thread.start()
send_thread.start()

recv_thread.join()
send_thread.join()
s.close()

print(f"Transmission errors: {transmission_errors}", file=sys.stderr)
print(f"Reception errors: {reception_errors}", file=sys.stderr)