import hashlib

from bencode_decoder import BencodeDecoder
from bencode_encoder import BencodeEncoder

TORRENT_FILE = "torrents/ubuntu.torrent"


def main():

    with open(TORRENT_FILE, "rb") as file:
        torrent_data = file.read()

    decoded_data = torrent_data.decode("latin-1")

    decoder = BencodeDecoder(decoded_data)

    metadata = decoder.decode()

    info_dictionary = metadata["info"]

    encoder = BencodeEncoder()

    bencoded_info = encoder.encode(info_dictionary)

    info_hash = hashlib.sha1(
        bencoded_info.encode("latin-1")
    ).hexdigest()

    print("\n===== INFO HASH =====\n")

    print(info_hash)


if __name__ == "__main__":
    main()