import socket

PORT = 12351
ADDRESS = "192.168.101.72"
# ADDRESS = "127.0.0.1"

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    while True:
        msg = input("> ")
        if msg == "exit":
            break

        # 送信
        s.sendto(msg.encode(), (ADDRESS, PORT))
