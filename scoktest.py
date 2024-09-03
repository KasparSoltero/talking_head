import socket
import time
import json
import struct

HOST = "127.0.0.1"
PORT = 49494


def send_data(sock, data):
    try:
        json_data = json.dumps(data)
        length = len(json_data)
        length_bytes = struct.pack("!I", length)
        sock.sendall(length_bytes + json_data.encode("utf-8"))
        print(f"Sent data: {data}")
        return True
    except Exception as e:
        print(f"Error sending data: {e}")
        return False


while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"Connected to {HOST}:{PORT}")
            while True:
                data = {"x": "i"}  # Your data here
                if not send_data(s, data):
                    break
                time.sleep(1)
    except ConnectionRefusedError:
        print(
            f"Connection refused. make sure unreal is running and listening on {HOST}:{PORT}"
        )
    except Exception as e:
        print(f"Error: {e}")

    print(f"Waiting for 5 seconds before trying again...")
    time.sleep(5)
