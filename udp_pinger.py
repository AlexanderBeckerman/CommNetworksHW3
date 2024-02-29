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
FIXED_MESSAGE = "0"
MAX_PACKET_SIZE = 1405


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", type=str)
    parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("-s", "--size", type=int, default=DEFAULT_SIZE)
    parser.add_argument("-c", "--count", type=int, default=DEFAULT_COUNT)
    parser.add_argument("-t", "--timeout", type=float, default=DEFAULT_TIMEOUT)
    args = parser.parse_args()

    ip = args.ip
    port = args.port
    size = args.size
    count = args.count
    timeout = args.timeout

    agent_address = (ip, port)
    success_recv_count = 0
    success_send_count = 0
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print("Error creating socket:", e)
        exit(0)

    sock.settimeout(timeout)
    for id in range(count):

        start_time = time.time()
        data = FIXED_MESSAGE.zfill(size).encode()
        message_to_send = struct.pack(">bi", OPCODE, id) + data
        try:
            sock.sendto(message_to_send, agent_address)
        except socket.error as e:
            print("Error sending message to socket")
            exit(0)
        success_send_count += 1
        
        try:
            while True:  # Did this so we can clear the buffer of late ping replies
                received_data, addr = sock.recvfrom(MAX_PACKET_SIZE)
                opcode_unpacked, id_bytes_unpacked = struct.unpack(
                    ">bi", received_data[:HEADER_LENGTH]
                )
                if id_bytes_unpacked != id:
                    continue
                break
            data = received_data[HEADER_LENGTH:]
            end_time = time.time()
            rtt = end_time - start_time
            total_bytes_len = len(received_data)
            print(
                "{} bytes from {}: seq={} rtt={}".format(
                    total_bytes_len, ip, id_bytes_unpacked, rtt
                )
            )
            success_recv_count += 1
        except socket.timeout:
            print("requst timeout for icmp_seq {}".format(id))
        except socket.error as e:
            print("Socket error:", e)
            exit(0)
        except Exception as e:
            print("An unexpected error occurred:", e)
            exit(0)

    packet_loss = 100 - success_recv_count / success_send_count * 100
    print("--- {} statistics ---".format(ip))
    print(
        "{} packets transmitted, {} packets received, {:.2f}% packet loss".format(
            success_send_count, success_recv_count, packet_loss
        )
    )


if __name__ == "__main__":
    main()
