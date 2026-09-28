import socket


HOST = "127.0.0.1"
PORT = 8888


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM TCP
server.bind((HOST, PORT))
server.listen(5) # max 5 соединений в очереди ожидания


print(f"TCP-сервер слушает {HOST}:{PORT}")

while True:
    conn, addr = server.accept() # блокирующий вызов - ожидание
    print(f"Подключился клиент: {addr}")
    
    
    data = conn.recv(1024) # считка данных от клиента
    print(f"Получено: {data.decode('utf-8')}")
    
    
    conn.sendall(b"Message received!") # отправка ответа
    conn.close() # закрытие коннекта