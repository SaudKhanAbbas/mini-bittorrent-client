import socket
import threading

HOST = "127.0.0.1"
PORT = 5555


def handle_client(client_socket, client_address):
    print(f"\nConnection established with {client_address}")

    while True:
        message = client_socket.recv(1024)

        if not message:
            print(f"Client {client_address} disconnected.")
            break

        decoded_message = message.decode()

        print(f"{client_address}: {decoded_message}")

        response = f"Echo -> {decoded_message}"

        client_socket.send(response.encode())

    client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()

    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )

    client_thread.start()