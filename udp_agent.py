import argparse
import socket
import struct
import time

DEFAULT_PORT = 1337
HOST = 'localhost'
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

        received_data, addr = sock.recvfrom(MAX_PACKET_SIZE)
        opcode_unpacked, id_bytes_unpacked = struct.unpack('>bi', received_data[:HEADER_LENGTH])
        data = received_data[HEADER_LENGTH:]

        # opcode, addr = sock.recvfrom(1)
        # opcode_unpacked = struct.unpack('>b', opcode)[0]
        print("opcode is {}".format(opcode_unpacked))
        # id, addr = sock.recvfrom(4)
        # id_unpacked = struct.unpack('>i', id)[0]
        print("id is {}".format(id_bytes_unpacked))
        # data_length, addr = sock.recvfrom(1)
        # data_length_unpacked = struct.unpack('>b', data_length)[0]
        # print("data_length is {}".format(data_length_unpacked))
        # data, addr = sock.recvfrom(data_length_unpacked)
        print("data is {}".format(data.decode()))
        message_to_send = struct.pack('>bi', OPCODE, id_bytes_unpacked)
        sock.sendto(message_to_send + data, addr)
        if id_bytes_unpacked == 1:
            time.sleep(1.5)
        # sock.sendto(struct.pack('>b', opcode_unpacked), addr)
        # sock.sendto(struct.pack('>i', id_bytes_unpacked), addr)
        # sock.sendto(struct.pack('>b', ), addr)
        # sock.sendto(data, addr)


if __name__ == '__main__':
    main()
