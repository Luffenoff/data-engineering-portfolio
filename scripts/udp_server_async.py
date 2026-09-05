import asyncio


class TelemetryProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport
        print("UDP-сервер (асинх) запущен")
    
    
    def datagram_received(self, data, addr):
        message = data.decode('utf-8')
        print(f"Получено от {addr}: {message}")
        # Асинх
        asyncio.create_task(self.process_message(message, addr))
        
        
    async def process_message(self, message, addr):
        await asyncio.sleep(0.1)
        print(f" -> Обработано сообщение от {addr}")
        
    
async def main():
    loop = asyncio.get_event_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: TelemetryProtocol(),
        local_addr=("127.0.0.1", 9999)
    )
    try:
        await asyncio.sleep(3600)
    finally:
        transport.close()
        
asyncio.run(main())
        