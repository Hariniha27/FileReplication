# server/server.py
import socket
import threading
import os
import shutil
import sys
import traceback

HOST = '0.0.0.0'   # listen on all interfaces
PORT = 9000

# Folder paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')
NODE_DIRS = [
    os.path.join(BASE_DIR, 'node1'),
    os.path.join(BASE_DIR, 'node2'),
    os.path.join(BASE_DIR, 'node3'),
]

# Make sure folders exist
os.makedirs(DATA_DIR, exist_ok=True)
for d in NODE_DIRS:
    os.makedirs(d, exist_ok=True)

def recv_all(conn, n):
    """Receive exactly n bytes or raise."""
    data = b''
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            raise ConnectionError("Connection closed while receiving data")
        data += packet
    return data

def handle_client(conn, addr):
    try:
        with conn:
            header = conn.recv(1024).decode('utf-8')
            if not header:
                return
            header = header.strip()
            parts = header.split()
            if not parts:
                conn.sendall(b'ERROR Invalid command\n')
                return

            cmd = parts[0].upper()
            if cmd == 'UPLOAD' and len(parts) == 3:
                filename = os.path.basename(parts[1])
                filesize = int(parts[2])
                conn.sendall(b'OK\n')  # ready to receive

                file_bytes = recv_all(conn, filesize)

                # save to main data dir
                target_path = os.path.join(DATA_DIR, filename)
                with open(target_path, 'wb') as f:
                    f.write(file_bytes)

                # replicate to nodes
                replicate_success = []
                for node in NODE_DIRS:
                    try:
                        shutil.copyfile(target_path, os.path.join(node, filename))
                        replicate_success.append(node)
                    except Exception as e:
                        print(f"Replication to {node} failed: {e}")

                resp = f'UPLOAD_OK {len(replicate_success)}\n'.encode()
                conn.sendall(resp)

            elif cmd == 'DOWNLOAD' and len(parts) == 2:
                filename = os.path.basename(parts[1])
                found_path = None
                for node in NODE_DIRS:
                    p = os.path.join(node, filename)
                    if os.path.exists(p):
                        found_path = p
                        break
                if not found_path:
                    p = os.path.join(DATA_DIR, filename)
                    if os.path.exists(p):
                        found_path = p

                if not found_path:
                    conn.sendall(b'ERROR NOT_FOUND\n')
                    return

                filesize = os.path.getsize(found_path)
                conn.sendall(f'OK {filesize}\n'.encode())

                with open(found_path, 'rb') as f:
                    conn.sendall(f.read())

            else:
                conn.sendall(b'ERROR Unknown command\n')
    except Exception as e:
        print(f"Client {addr} error: {e}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print("Accepted connection from", addr)
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

# --- main entry point with error handling ---
def main():
    try:
        start_server()
    except Exception:
        print("ERROR starting server:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

