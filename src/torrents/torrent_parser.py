from bencode_decoder import BencodeDecoder


with open("torrents/ubuntu.torrent", "rb") as file:
    torrent_data = file.read()


decoded_data = torrent_data.decode("latin-1")

decoder = BencodeDecoder(decoded_data)

metadata = decoder.decode()

print(metadata)