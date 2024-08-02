"""
mocopiアプリと 1対1 で接続し、
インターネット(Wi-Fi or L5G)経由で表示側PCに送信するスクリプト

1対多は考慮していません
"""

import sys
import socket
import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

RECV_PORT = 12350
SEND_PORT = 12351
API_URL = "https://prj-5g-with-mocopi.sysken.net/api/raw/"
SEND_ID = sys.argv[1] if len(sys.argv) > 1 else None
SERVER = sys.argv[2] if len(sys.argv) > 2 else None

if not API_URL:
    raise ValueError("API_URL is required. set to env file.")
if not SEND_ID:
    raise ValueError("send_id is required. (python main.py <send_id>)")


def send_with_udp(data):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(data, (SERVER, SEND_PORT))
        s.close()


def send2api(data):
    res = requests.post(urljoin(API_URL, SEND_ID), data=data)
    print(f"[{res.status_code}]: {res.text}")
    return res


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((SERVER, RECV_PORT))
        print(f"[Start] {SERVER}:{RECV_PORT}")

        with ThreadPoolExecutor() as executor:
            try:
                while True:
                    data, address = s.recvfrom(8192)
                    print(f"[Received] {address}")
                    executor.submit(send2api, data)
                    executor.submit(send_with_udp, data)

            except KeyboardInterrupt:
                print("Finished!")

        executor.shutdown(wait=True)


if __name__ == "__main__":
    main()
