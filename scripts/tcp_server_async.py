import asyncio


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Подключился клиент: {addr}")
    
    
    data = await reader.read(1024)
    message = data.decode()
    print(f"Получено: {message}")
    
    writer.write("Message received!".encode())
    await writer.drain()
    
    writer.close()
    await writer.wait_closed()
    
    
async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    print(f"TCP-сервер (asyncio) слушает 127.0.0.1:8888")
    async with server:
        await server.serve_forever()
        
asyncio.run(main())