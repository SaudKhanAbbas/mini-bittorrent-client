from bencode_decoder import BencodeDecoder


TORRENT_FILE = "torrents/ubuntu.torrent"


def main():
    with open(TORRENT_FILE, "rb") as file:
        torrent_data = file.read()

    decoded_data = torrent_data.decode("latin-1")

    decoder = BencodeDecoder(decoded_data)

    metadata = decoder.decode()

    announce = metadata["announce"]

    info = metadata["info"]

    name = info["name"]

    piece_length = info["piece length"]

    pieces = info["pieces"]

    number_of_pieces = len(pieces) // 20

    print("\n===== TORRENT METADATA =====\n")

    print(f"Tracker URL: {announce}")

    print(f"\nFile Name: {name}")

    print(f"\nPiece Length: {piece_length}")

    print(f"\nPiece Hash Bytes: {len(pieces)}")

    print(f"\nNumber Of Pieces: {number_of_pieces}")


if __name__ == "__main__":
    main()