#!/usr/bin/python3

# Importing python standard modules and packages.
import json
import asyncio

# Importing TikTokLive API modules and packages.
from TikTokLive.types.errors import LiveNotFound


# Importing local modules and libraries.
from models.raffle import Raffle
from models.raffle_game import RaffleGame
from models.raffle_tiktok_client import RaffleTikTokClient
from connection_manager import set_raffle, get_raffle


def init_handler(websocket, data):
    opdata = {}
    try:
        unique_id = data["uniqueId"]
        raffle = get_raffle(websocket)
        if (not raffle):
            raffle = Raffle(**{"unique_id":unique_id})
            raffle.websocket = websocket
            raffle.tiktok_client = RaffleTikTokClient(**{"raffle": raffle})
        elif (raffle and not raffle.tiktok_client.client.connected):
            raffle.tiktok_client.client.start()

        if (raffle and not raffle.current_game):
            raffle.set_game(RaffleGame(**{"raffle": raffle}))

        if (not get_raffle(websocket)):
            set_raffle(websocket, raffle)

        asyncio.create_task(raffle.tiktok_client.client.start())
        
        opdata["type"] = "success"
        opdata["body"] = {
            "requiredGift": raffle.required_gift,
            "minGiftAmount": raffle.required_gift_amount,
            "minParticipant": raffle.min_participant
        }
    except Exception as e:
        opdata["type"] = "error"
        opdata["body"] = {
            "message": str(e)
        }
    asyncio.create_task(websocket.send(json.dumps(opdata)))

def start_handler(websocket, data):
    raffle = get_raffle(websocket)
    raffle.current_game.start()
    raffle.set_game(RaffleGame(**{"raffle": raffle}))
    
    print(f"Raffle winner {raffle.winner}")

    opdata = {
        "type": "winner",
        "body": {
            "winner" : raffle.winner
        }
    }
    asyncio.create_task(websocket.send(json.dumps(opdata)))
