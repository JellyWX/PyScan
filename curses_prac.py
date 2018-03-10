import curses
import socket

def main(scrn):
    curses.echo()
    height, width = scrn.getmaxyx()
    scrn.border(1)
    ip = ''

    while not ip:
        scrn.addstr(0, int(0.5*(width - len('Enter the IP/DN of the server:'))), 'Enter the IP/DN of the server:')
        ip = scrn.getstr(int(0.5*height), int(0.5*width)-6).decode()
        scrn.refresh()

        if any([char not in '0123456789.' for char in ip]):
            ip = socket.gethostbyname(ip)

    scrn.clear()
    scrn.border(1)
    scrn.addstr(0, int(0.5*(width - len('Scanning...'))), 'Scanning...')
    scrn.addstr(1, int(0.5*(width - len(ip))), ip)

    notable = ['START']

    f = open('log', 'a')
    for port in range(0, 65536):
        scrn.addstr(2, int(0.5*(width - len('Testing port {}/65535'.format(port)))), 'Testing port {}/65535'.format(port+1))
        s = socket.socket()
        s.settimeout(8)
        try:
            s.connect((ip, port))
        except ConnectionRefusedError:
            scrn.addstr(height-1, 1, 'Error on port {}: Connection refused'.format(port))
        except socket.timeout:
            scrn.addstr(height-1, 1, 'Timed out on port {}'.format(port))
            notable.append('Timed out on port {}'.format(port))

            f.write('{} occupied/timed out\n'.format(port))
        else:
            scrn.addstr(height-1, 1, 'Connection accepted on port {}'.format(port))
            notable.append('Connection accepted on port {}'.format(port))

            f.write('{} open\n'.format(port))
        s.close()

        i = height - 1
        for n in notable[::-1]:
            if i < height*0.75:
                break
            i -= 1
            scrn.addstr(i, 0, n)

        scrn.refresh()

    f.close()

    while True:
        scrn.addstr(0, int(0.5*(width - len('Success. Press any key to close.'))), 'Success. Press any key to close.')
        scrn.refresh()
        scrn.getch()


curses.wrapper(main)
