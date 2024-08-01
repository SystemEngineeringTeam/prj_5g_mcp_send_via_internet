"""
mocopiアプリと 1対1 で接続し、
インターネット(Wi-Fi or L5G)経由で表示側PCに送信するスクリプト

1対多は考慮していません
"""

import os
import sys
import socket
import requests
from urllib.parse import urljoin

ENV_PORT = os.environ.get("PORT")
PORT = int(ENV_PORT or 12351)
SERVER = os.environ.get("SERVER") or "127.0.0.1"
API_URL = os.environ.get("API_URL")
SEND_ID = sys.argv[1] if len(sys.argv) > 1 else None

if not API_URL:
    raise ValueError("API_URL is required. set to env file.")
if not SEND_ID:
    raise ValueError("send_id is required. (python main.py <send_id>)")


def send2api(data):
    res = requests.post(urljoin(API_URL, SEND_ID), data=data)
    return res


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((SERVER, PORT))
        print(f"[Start] {SERVER}:{PORT}")

        try:
            while True:
                data, address = s.recvfrom(8192)
                print(f"[Received] {address}")
                res = send2api(data)
                print(f"[{res.status_code}]: {res.text}")

        except KeyboardInterrupt:
            print("Finished!")


if __name__ == "__main__":
    main()
