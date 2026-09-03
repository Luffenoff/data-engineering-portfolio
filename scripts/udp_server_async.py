import asyncio


class TelemetryProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport
        print("UDP-сервер (асинх) запущен")
    
    
    def datagram_received(self, data, addr):
        message = data.decode('utf-8')