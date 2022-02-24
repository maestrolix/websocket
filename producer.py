import asyncio
import websockets


async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as websocket:
        await websocket.send(message)
        await websocket.recv()

asyncio.run(produce(message='hello', host='localhost', port=4000))
