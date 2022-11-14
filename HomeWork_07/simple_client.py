import socket

HOST, PORT = "localhost", 5005
# HOST, PORT = "192.168.1.152", 5005


def start_client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
        except (ConnectionError, ConnectionRefusedError, OSError):
            print("Connection not established because the destination computer\nrejected the connection request")
            return
        while True:
            data = input("Type the message to send: ")
            data_bytes = data.encode("utf8")

            try:
                sock.sendall(data_bytes)
            except (ConnectionError, ConnectionAbortedError, OSError):
                print(f"Server unavailable, unable to send")
                break

            try:
                data = sock.recv(1024).decode("utf8")
            except (ConnectionError, ConnectionAbortedError, OSError):
                print(f"Server unavailable, unable to read")
                break

            if data == "close":
                print("The program was shut down")
                break
            print("Received:", data)


if __name__ == '__main__':
    try:
        start_client(HOST, PORT)
    except KeyboardInterrupt:
        print("\nThe program was shut down")
