import hashlib

from src.torrent.bencode_decoder import BencodeDecoder


class BencodePositionTracker:

    def __init__(self, data):
        self.data = data
        self.index = 0

    def skip(self):

        current = chr(self.data[self.index])

        if current == "i":
            self.skip_integer()

        elif current.isdigit():
            self.skip_string()

        elif current == "l":
            self.skip_list()

        elif current == "d":
            self.skip_dictionary()

        else:
            raise ValueError(f"Unsupported type: {current}")

    def skip_integer(self):

        self.index += 1

        while chr(self.data[self.index]) != "e":
            self.index += 1

        self.index += 1

    def skip_string(self):

        colon = self.data.index(b":", self.index)

        length = int(self.data[self.index:colon])

        self.index = colon + 1 + length

    def skip_list(self):

        self.index += 1

        while chr(self.data[self.index]) != "e":
            self.skip()

        self.index += 1

    def skip_dictionary(self):

        self.index += 1

        while chr(self.data[self.index]) != "e":

            self.skip()
            self.skip()

        self.index += 1


class Torrent:

    def __init__(self, torrent_file):

        self.torrent_file = torrent_file

        with open(torrent_file, "rb") as file:
            self.torrent_bytes = file.read()

        decoded = self.torrent_bytes.decode("latin-1")

        decoder = BencodeDecoder(decoded)

        self.metadata = decoder.decode()

        self.info_hash = self.generate_info_hash()

        self.announce_url = self.metadata["announce"]

        info = self.metadata["info"]

        self.file_name = info["name"]

        self.file_size = info["length"]

        self.piece_length = info["piece length"]

        self.number_of_pieces = len(info["pieces"]) // 20

    def generate_info_hash(self):

        marker = b"4:info"

        marker_position = self.torrent_bytes.find(marker)

        if marker_position == -1:
            raise ValueError("Info dictionary not found.")

        info_start = marker_position + len(marker)

        tracker = BencodePositionTracker(self.torrent_bytes)

        tracker.index = info_start

        tracker.skip()

        info_end = tracker.index

        info_bytes = self.torrent_bytes[info_start:info_end]

        return hashlib.sha1(info_bytes).digest()


def main():

    torrent = Torrent("torrents/ubuntu.torrent")

    print("\n===== TORRENT =====\n")

    print("File Name:")

    print(torrent.file_name)

    print("\nTracker:")

    print(torrent.announce_url)

    print("\nFile Size:")

    print(torrent.file_size)

    print("\nPiece Length:")

    print(torrent.piece_length)

    print("\nPieces:")

    print(torrent.number_of_pieces)

    print("\nInfo Hash:")

    print(torrent.info_hash.hex())


if __name__ == "__main__":
    main()