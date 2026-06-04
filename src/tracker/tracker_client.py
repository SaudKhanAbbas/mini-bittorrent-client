import hashlib
import urllib.parse
import urllib.request

from src.torrent.bencode_decoder import BencodeDecoder
from src.torrent.bencode_encoder import BencodeEncoder

TORRENT_FILE = "torrents/ubuntu.torrent"


def get_info_hash(metadata):

    info_dictionary = metadata["info"]

    encoder = BencodeEncoder()

    bencoded_info = encoder.encode(info_dictionary)

    return hashlib.sha1(
        bencoded_info.encode("latin-1")
    ).digest()


def main():

    with open(TORRENT_FILE, "rb") as file:
        torrent_data = file.read()

    decoded_data = torrent_data.decode("latin-1")

    decoder = BencodeDecoder(decoded_data)

    metadata = decoder.decode()

    announce_url = metadata["announce"]

    info_hash = get_info_hash(metadata)

    peer_id = b"-PC0001-123456789012"

    tracker_url = (
        f"{announce_url}"
        f"?info_hash={urllib.parse.quote_from_bytes(info_hash)}"
        f"&peer_id={peer_id.decode()}"
        f"&port=6881"
        f"&uploaded=0"
        f"&downloaded=0"
        f"&left=0"
        f"&compact=1"
    )

    print("\nConnecting to tracker...\n")

    response = urllib.request.urlopen(tracker_url)

    tracker_response = response.read()

    print("Response received!")

    print("\nResponse Size:")

    print(len(tracker_response))


if __name__ == "__main__":
    main()