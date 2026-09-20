import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8888))

client.sendall(b"Server status: OK")
response = client.recv(1024)
print(f"Ответ сервера: {response.decode("utf-8")}")

client.close()