import socket


HOST = "127.0.0.1"
PORT = 9999


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4 и UDP
sock.bind((HOST, PORT))


print(f"UDP-сервер слушает {HOST}:{PORT}")


while True:
    data, addr = sock.recvfrom(1024)
    print(f"Получено от {addr}: {data.decode('utf-8')}")