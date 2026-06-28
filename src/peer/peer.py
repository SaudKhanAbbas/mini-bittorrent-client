import socket

from src.peer.handshake import build_handshake
from src.torrent.torrent import Torrent


class Peer:

    def __init__(self, ip, port, torrent: Torrent):

        self.ip = ip
        self.port = port
        self.torrent = torrent

        self.peer_id = b"-PC0001-123456789012"

        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

    def connect(self):

        print(f"Connecting to {self.ip}:{self.port}...")

        self.socket.connect(
            (self.ip, self.port)
        )

        print("Connected!")

    def send_handshake(self):

        handshake = build_handshake(
            self.torrent.info_hash,
            self.peer_id
        )

        self.socket.sendall(handshake)

        print("Handshake sent!")

    def receive_handshake(self):

        response = self.socket.recv(68)

        print("\nReceived Handshake:\n")

        print(response)

        return response

    def disconnect(self):

        self.socket.close()

        print("Disconnected.")