import socket
import json
import threading


class AudioToUnrealMovement:
    def __init__(self) -> None:
        self.host = "127.0.0.1"
        self.port = 65432
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"unreal socket listening on {self.host}:{self.port}")

        self.connection = None
        self.is_running = True
        self.server_thread = threading.Thread(target=self._accept_connections)
        self.server_thread.start()

    def _accept_connections(self):
        while self.is_running:
            try:
                self.connection, addr = self.socket.accept()
                print(f"Connected by {addr}")
            except:
                break

    def convert(self, audio_stream):
        if not self.connection:
            print("No connection")
            return

        mouth_shape = self._calculate_mouth_shape(audio_stream)
        data = json.dumps(mouth_shape)
        try:
            self.connection.sendall(data.encode("utf-8"))
        except:
            print("failed to send data")

    def _calculate_mouth_shape(self, audio_stream):
        return {"shape": "0", "intensity": 0.5}
