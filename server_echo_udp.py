#!/usr/bin/python3
# Echo server UDP program - version of server_echo_udp.c, mono-cliente
# Author: José M. Piquer (jpiquer@dcc.uchile.cl).
import jsockets
import sys

s = jsockets.socket_udp_bind(1818)
if s is None:
    print('could not open socket')
    sys.exit(1)
while True:
    data, addr = s.recvfrom(1024 * 1024)
    if not data: break
    s.sendto(data, addr)

s.close()
