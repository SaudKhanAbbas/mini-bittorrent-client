import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

connected_clients = []
client_lock = threading.Lock()


def broadcast(message, sender_socket):
    with client_lock:
        clients_snapshot = connected_clients.copy()

    for client in clients_snapshot:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                pass


def handle_client(client_socket, client_address):
    print(f"\nConnection established with {client_address}")

    while True:
        try:
            message = client_socket.recv(1024)

            if not message:
                break

            decoded_message = message.decode()

            print(f"{client_address}: {decoded_message}")

            broadcast(
                f"{client_address}: {decoded_message}",
                client_socket
            )

        except:
            break

    print(f"Client {client_address} disconnected.")

    with client_lock:
        if client_socket in connected_clients:
            connected_clients.remove(client_socket)

    client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()

    with client_lock:
        connected_clients.append(client_socket)

    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )

    client_thread.start()