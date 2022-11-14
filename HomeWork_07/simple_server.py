import asyncio
import socket

HOST = ""
PORT = 5005


async def handle_connection(loop, sock, addr):
    print(f"Start {addr}")
    with sock:
        while True:
            try:
                data = (await loop.sock_recv(sock, 1024)).decode('utf8')
                if not data or data.lower() == "exit":
                    await loop.sock_sendall(sock, b"close")
                    break
                print(f"Message from client {addr}: {data}")
            except (ConnectionError, ConnectionAbortedError):
                print(f"Client {addr} suddenly closed while receiving")
                break

            try:
                # await asyncio.sleep(10)  # for client disconnect test
                await loop.sock_sendall(sock, b"OK")
            except (ConnectionError, ConnectionAbortedError):
                print(f"Client {addr} suddenly closed, cannot send")
                break

    print(f"Disconnected by {addr}")


async def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen()
        serv_sock.setblocking(False)

        serv_loop = asyncio.get_event_loop()

        while True:
            sock, addr = await serv_loop.sock_accept(serv_sock)
            print(sock, addr)
            cor_con = handle_connection(serv_loop, sock, addr)
            serv_loop.create_task(cor_con)


if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("\nThe server was shut down")
