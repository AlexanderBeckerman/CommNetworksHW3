import argparse
import socket

DEFAULT_PORT = 1337
DEFAULT_SIZE = 100
DEFAULT_COUNT = 10
DEFAULT_TIMEOUT = 1000


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=str, required=True)
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('-s', '--size', type=int, default=DEFAULT_SIZE)
    parser.add_argument('-c', '--count', type=int, default=DEFAULT_COUNT)
    parser.add_argument('-t', '--timeout', type=int, default=DEFAULT_TIMEOUT)
    args = parser.parse_args()

    ip = args.ip
    port = args.port
    size = args.size
    count = args.count
    timeout = args.timeout


    return

if __name__ == '__main__':
    main()
