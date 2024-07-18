import socket

HOST = '127.0.0.1'
PORT = 1234
BUFSIZE = 4096

#01. Preparing Socket : socket()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.AF_INET : IPv4
#socket.SOCK_STREAM : TCP

#02. Configuring Soccket and Connect to the Server : connect()
client.connect((HOST,PORT))

#03. Data　Yaritori : send(), recv()
data = client.recv(BUFSIZE)
print(data.decode('UTF-8'))

#04. Closing the connection : close()
client.close()
