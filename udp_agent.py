import argparse
import socket
import struct

DEFAULT_PORT = 1337
HOST = '127.0.0.1'
HEADER_LENGTH = 5  # 1 byte for OPCODE and 4 for ID
OPCODE = 1
MAX_PACKET_SIZE = 1405


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    port = args.port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, port))
    sock.setblocking(True)
    while True:
        try:
            received_data, addr = sock.recvfrom(MAX_PACKET_SIZE)
        except socket.error as e:
            print("Error reading data from socket")
            exit(0)

        opcode_unpacked, id_bytes_unpacked = struct.unpack('>bi', received_data[:HEADER_LENGTH])
        data = received_data[HEADER_LENGTH:]
        message_to_send = struct.pack('>bi', OPCODE, id_bytes_unpacked)
        try:
            sock.sendto(message_to_send + data, addr)
        except socket.error as e:
            print("Error sending back data")
            exit(0)

if __name__ == '__main__':
    main()
