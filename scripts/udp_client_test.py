import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = "CPU usage: 45%"
sock.sendto(message.encode('utf-8'), ("127.0.0.1", 9999))
print("Сообщение отправлено")
sock.close