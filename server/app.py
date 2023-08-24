#!/usr/bin/python3

# Importing python standard modules and packages.
import asyncio
import signal
import os
import json


# Import websocket package (3rd party).
import websockets

# Importing local modules and libraries.
from type_handlers import init_handler, start_handler
from connection_manager import add_connection, remove_connection, \
    get_update, get_raffle


consumer_handlers = {
    "init": init_handler,
    "start": start_handler,
}


async def consumer_handler(websocket):
    """
    """
    async for message in websocket:
        opdata = json.loads(message)
        type = opdata["type"]
        data = opdata["body"]
        print(f"[MESSAGE RECIEVED]\nType: {type}\nMessage: {data}")
        consumer_handlers[type](websocket, data)


async def producer_handler(websocket):
    """
    """
    while True:
        await asyncio.sleep(10)
        raffle = get_raffle(websocket)
        if raffle and raffle.tiktok_client.client.connected:
            if raffle.delay:
                raffle.delay = False
                await asyncio.sleep(25)

            opdata = {
                "type": "update",
                "body": get_update(websocket)
            }
            await websocket.send(json.dumps(opdata))


async def handler(websocket):
    """
    """
    add_connection(websocket)
    try:
        consumer_task = asyncio.create_task(consumer_handler(websocket))
        producer_task = asyncio.create_task(producer_handler(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
    finally:
        remove_connection(websocket)

async def main():
    """
    """
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        handler,
        host="",
        port=int(os.environ.get("PORT", 8001)),
    ):
        await stop



if __name__ == "__main__":
    asyncio.run(main())
