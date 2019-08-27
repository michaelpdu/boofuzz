import os
import argparse
import socket

HOST = "127.0.0.1"
PORT = 8182

def dump_file(file_path, size, output):
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(b'GET /?action=hexdump&file={},0,{} HTTP/1.1'.format(file_path, size))
    data = s.recv(size)
    head, body = data.split('\r\n\r\n')
    print(head)
    print('-----------------------')
    print(body)
    with open(output, 'wb') as fh:
        fh.write(body)
    s.close()

def main(file_path, size, output):
    dump_file(file_path, size, output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command Usages')
    parser.add_argument("file_path", type=str, help="specify file path to be read")
    parser.add_argument("-s", "--size", type=int, default=10000, help="specify file size")
    parser.add_argument("-o", "--output", type=str, default="output", help="save to local file")
    args = parser.parse_args()
    main(args.file_path, args.size, args.output)

