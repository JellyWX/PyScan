import socket
import sys

ip = sys.argv[1]
if any([char not in '0123456789.' for char in ip]):
    ip = socket.gethostbyname(sys.argv[1])

f = open('log', 'a')
for port in range(0, 65536):
    s = socket.socket()
    s.settimeout(15)
    try:
        s.connect((ip, port))
    except ConnectionRefusedError:
        print('Error on port {}: Connection refused'.format(port))
    except socket.timeout:
        print('Timed out on port {}'.format(port))
        f.write('{} occupied/timed out\n'.format(port))
    else:
        print('Connection accepted on port {}'.format(port))
        f.write('{} open\n'.format(port))
    s.close()

f.close()
