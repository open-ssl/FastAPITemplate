import aiohttp
import asyncio
import time


async def main():
    async with aiohttp.ClientSession() as session:
        client_id = int(time.time() * 1000)
        async with session.ws_connect(f"http://localhost:8000/chat/ws/{client_id}") as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print("Receive text msg")
                    with open("ws_messages.txt", "a") as file:
                        file.write(f"{msg.data}\n")


if __name__ == '__main__':
    print("Start to write messages locally")
    asyncio.run(main())
