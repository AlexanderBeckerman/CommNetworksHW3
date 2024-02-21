import argparse
import socket
import struct
import time

DEFAULT_PORT = 1337
DEFAULT_SIZE = 100
DEFAULT_COUNT = 10
DEFAULT_TIMEOUT = 1
HEADER_LENGTH = 5
OPCODE = 0
FIXED_MESSAGE = '0'
MAX_PACKET_SIZE = 1405



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=str)
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

    agent_address = (ip, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    for i in range(count):
        id = i
        start_time = time.time()
        data = FIXED_MESSAGE.zfill(size).encode()
        message_to_send = struct.pack('>bi', OPCODE, i) + data
        # sock.sendto(struct.pack('>b', OPCODE), agent_address)
        # sock.sendto(struct.pack('>i', id), agent_address)
        sock.sendto(message_to_send, agent_address)
        # sock.sendto(struct.pack('>b', size), agent_address)
        # sock.sendto(msg_to_send, agent_address)
        try:
            # opcode, addr = sock.recvfrom(1)
            # opcode_unpacked = struct.unpack('>b', opcode)[0]
            # # print("opcode is {}".format(opcode_unpacked))
            # id, addr = sock.recvfrom(4)
            # id_unpacked = struct.unpack('>i', id)[0]
            # # print("id is {}".format(id_unpacked))
            # data_length, addr = sock.recvfrom(1)
            # data_length_unpacked = struct.unpack('>b', data_length)[0]
            # # print("data_length is {}".format(data_length_unpacked))
            # data, addr = sock.recvfrom(data_length_unpacked)
            # # print("data is {}".format(data.decode()))
            received_data, addr = sock.recvfrom(MAX_PACKET_SIZE)
            opcode_unpacked, id_bytes_unpacked = struct.unpack('>bi', received_data[:HEADER_LENGTH])
            data = received_data[HEADER_LENGTH:]
            end_time = time.time()
            rtt = end_time - start_time
            total_bytes_len = len(received_data)
            print("{} bytes from {}: seq={} rtt={}".format(total_bytes_len, ip, i, rtt))
        except socket.timeout:
            print('requst timeout for icmp_seq {}'.format(i))
            # Discard any remaining data in the buffer
            sock.settimeout(0)  # Set timeout to non-blocking
            while True:
                try:
                    _ = sock.recv(MAX_PACKET_SIZE)
                except socket.error as e:
                    print('Socket error inside while:', e)
                    break
            sock.settimeout(timeout)  # Restore timeout to blocking
        except socket.error as e:
            print('Socket error:', e)
            exit(0)
        except Exception as e:
            print('An unexpected error occurred:', e)
            exit(0)


if __name__ == '__main__':
    main()
