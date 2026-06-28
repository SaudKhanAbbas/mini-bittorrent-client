from src.peer.peer import Peer
from src.torrent.torrent import Torrent


def main():

    torrent = Torrent(
        "torrents/ubuntu.torrent"
    )

    peer = Peer(
        "127.0.0.1",
        6881,
        torrent
    )

    peer.connect()

    peer.send_handshake()

    peer.disconnect()


if __name__ == "__main__":
    main()