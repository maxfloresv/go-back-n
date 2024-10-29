"""
Go-Back-N transmission protocol in networking.
Author: Máximo Flores Valenzuela [https://github.com/maxfloresv].
"""

import threading
import time
import jsockets
import sys

# Controls the maximum sequence number possible.
MAX_SEQ_NUM = 65535
# Controls the adaptative timeout factor (this will be multiplied with the RTT).
TIMEOUT_FACTOR = 3
# Allows to change the definition of the adaptative timeout to test transmission errors.
TEST_TRANSMISSION_ERRORS = False

mutex = threading.Lock()
condition = threading.Condition(lock=mutex)
timeout = 0.5
# The minimum timeout for every packet (10% of the base timeout).
MINIMUM_TIMEOUT = 0.1 * timeout

# First packet of the window
base = 0
next_seq_num = 0
last_ack_received = -1
# Saves packets' content
buffer = {}
# [start, end] timers for every packet
timers = {}
transmission_finished = False
last_packet_transmitted = False
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
        # Receptor thread must accept the next packet in order, and reject all other packets.
        if last_recv_packet == (last_ack_received + 1) % (MAX_SEQ_NUM + 1):
            sys.stdout.buffer.write(data[2:])
            received_bytes += len(data[2:])
            with condition:
                timers[last_recv_packet].append(time.time())
                # This is the termination packet. It contains only the sequence number.
                if len(data) == 2:
                    transmission_finished = True
                    condition.notify()
                    break
                last_ack_received = last_recv_packet
                base = (last_ack_received + 1) % (MAX_SEQ_NUM + 1)
                condition.notify()
        else:
            # Packet is out of order or outside the window.
            reception_errors += 1
                
def sender(s):
    """
    Sender thread in packet transmission
    """
    global base, next_seq_num, timeout, transmission_errors, last_packet_transmitted

    while not transmission_finished:
        with condition:
            # Packets are transmitted only while there are data to send and they are inside the window.
            # This allows to avoid empty packet transmissions.
            while not last_packet_transmitted and ((next_seq_num < (base + WIN) % (MAX_SEQ_NUM + 1)) \
                or (next_seq_num > (base + WIN) % (MAX_SEQ_NUM + 1) and (next_seq_num <= MAX_SEQ_NUM))):
                data = sys.stdin.buffer.read(PACK_SZ - 2)
                if len(data) == 0:
                    last_packet_transmitted = True
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
                # Implements the adaptative timeout.
                if TEST_TRANSMISSION_ERRORS:
                    timeout = TIMEOUT_FACTOR * RTT
                else:
                    timeout = max(MINIMUM_TIMEOUT, TIMEOUT_FACTOR * RTT)
            else:
                # Retransmissions can occur more than one time. If "base" is not modified, it will enter
                # here again and again until one packet is accepted (i.e. the window slides).
                transmission_errors += 1
                # If base > next_seq_num, then next_seq_num exceeded the MAX_PACKET value, so we have
                # to separate the interval [base...next_seq_num) in two: [base...MAX_PACKET] and [0...next_seq_num).
                if base <= next_seq_num:
                    for seq in range(base, next_seq_num):
                        # This is a retransmission. We have to update the timer.
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

print(f"[DEBUG] Received {received_bytes} bytes", file=sys.stderr)
print(f"Transmission errors: {transmission_errors}", file=sys.stderr)
print(f"Reception errors: {reception_errors}", file=sys.stderr)