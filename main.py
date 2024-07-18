"""
mocopiアプリと 1対1 で接続し、
インターネット(Wi-Fi or L5G)経由で表示側PCに送信するスクリプト

1対多は考慮していません
"""

import datetime
import socket
import os

ENV_PORT = os.environ.get("PORT")
PORT = int(ENV_PORT) or 12351
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
BUFSIZE = 4096


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    try:
        while True:
            print(f"[NEW Connection] {ADDR} connected.")

            client, addr = server.accept()
            msg = str(datetime.datetime.now())
            client.sendall(msg.encode("UTF-8"))
            data = client.recv(BUFSIZE)
            data.decode(FORMAT)

            client.close()

    except KeyboardInterrupt:
        print("Finished!")


if __name__ == "__main__":
    main()
