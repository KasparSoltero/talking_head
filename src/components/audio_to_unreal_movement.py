import socket
import json
import threading
import struct
import io
import numpy as np


class AudioToUnrealMovement:
    def __init__(self) -> None:
        self.host = "127.0.0.1"
        self.port = 49494
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.sample_rate = 44100
        self.chunk_size = 1024

    def process_audio_stream(self, audio_stream):
        self.try_connect_socket()
        if not self.connected:
            print(f"Not connected to {self.host}:{self.port}. Cannot send data")
            return

        buffer = io.BytesIO()
        for chunk in audio_stream:
            buffer.write(chunk)
            if buffer.tell() >= self.chunk_size * 4:  # 4 bytes per int
                buffer.seek(0)
                chunk_data = buffer.read(self.chunk_size * 4)
                mouth_shape = self._calculate_mouth_shape(chunk_data)
                self.send_data(self.socket, mouth_shape)
                buffer = io.BytesIO(buffer.read())

    def _calculate_mouth_shape(self, chunk_data):
        try:

            audio_array = np.frombuffer(chunk_data, dtype=np.float32)
            # rms ampltude
            amplitude = np.sqrt(np.mean(np.square(audio_array)))
            shape = int(amplitude * 10)
            return {"shape": str(shape)}
        except:
            return {"shape": "0"}

    def try_connect_socket(self):
        try:
            self.socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
            self.connected = True
        except ConnectionRefusedError:
            print(
                f"Connection refused. make sure unreal is running and listening on {self.host}:{self.port}"
            )
        except Exception as e:
            print(f"Error: {e}")

    def send_data(self, sock, data):
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
