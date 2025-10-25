# client/client.py
import socket
import sys
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9000

def upload(file_path):
    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return
    filename = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)
    with socket.socket() as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        s.sendall(f'UPLOAD {filename} {filesize}\n'.encode())
        resp = s.recv(1024).decode()
        if not resp.startswith('OK'):
            print("Server refused upload:", resp)
            return
        # send file bytes
        with open(file_path, 'rb') as f:
            s.sendall(f.read())
        final = s.recv(1024).decode()
        print("Server response:", final.strip())

def download(filename, out_path=None):
    if out_path is None:
        out_path = filename
    with socket.socket() as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        s.sendall(f'DOWNLOAD {filename}\n'.encode())
        resp = s.recv(1024).decode().strip()
        if resp.startswith('ERROR'):
            print(resp)
            return
        parts = resp.split()
        if parts[0] != 'OK' or len(parts) != 2:
            print("Unexpected response:", resp)
            return
        filesize = int(parts[1])
        # receive file bytes
        received = b''
        while len(received) < filesize:
            chunk = s.recv(min(4096, filesize - len(received)))
            if not chunk:
                break
            received += chunk
        if len(received) != filesize:
            print("Download incomplete")
            return
        with open(out_path, 'wb') as f:
            f.write(received)
        print("Downloaded", out_path, "size", filesize)

def usage():
    print("Usage:")
    print("  python client.py upload <file_path>")
    print("  python client.py download <filename> [out_path]")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)
    cmd = sys.argv[1].lower()
    if cmd == 'upload':
        upload(sys.argv[2])
    elif cmd == 'download':
        filename = sys.argv[2]
        out = sys.argv[3] if len(sys.argv) >= 4 else None
        download(filename, out)
    else:
        usage()
