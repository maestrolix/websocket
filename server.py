import asyncio
import logging
import websockets
from websockets import WebSocketClientProtocol


logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, websocket: WebSocketClientProtocol) -> None:
        self.clients.add(websocket)
        logging.info(f'{websocket.remote_address} connects.')

    async def unregister(self, websocket: WebSocketClientProtocol) -> None:
        self.clients.remove(websocket)
        logging.info(f'{websocket.remote_address} disconnects.')

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def ws_handler(self, websocket: WebSocketClientProtocol) -> None:
        await self.register(websocket)
        try:
            await self.distribute(websocket)
        finally:
            await self.unregister(websocket)

    async def distribute(self, websocket: WebSocketClientProtocol) -> None:
        async for message in websocket:
            await self.send_to_clients(message)


if __name__ == '__main__':
    server = Server()
    start_server = websockets.serve(server.ws_handler, 'localhost', 4000)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
