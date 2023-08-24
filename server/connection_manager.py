#!/usr/bin/python3

import uuid

# Temporary connection manager

connections = {}

def add_connection(websocket, raffle=None):
    websocket.id = uuid.uuid4()
    print(f"New connection initiated ID: {websocket.id}")
    connections[websocket.id] = raffle


def remove_connection(websocket):
    print(f"Connection Closed ID: {websocket.id}")
    raffle = get_raffle(websocket)
    if raffle and raffle.tiktok_client:
        raffle.tiktok_client.client.stop()
    connections.pop(websocket.id)


def set_raffle(websocket, raffle):
    print(f"""
Raffle has been set for Connection ID: {websocket.id}
Raffle ID: {raffle.id}
""")
    connections[websocket.id] = raffle


def get_raffle(websocket):
    return(connections[websocket.id])


def get_update(websocket):
    raffle = connections[websocket.id]
    update = {}

    update["newParticipants"] = raffle.current_game.get_new_participants()
    update["totalAmount"] = raffle.current_game.total_amount
    update["totalParticipants"] = len(raffle.current_game.participants)
    update["lastWinner"] = raffle.last_winner if raffle.last_winner else "No Winner Yet"
    update["minParticipant"] = raffle.min_participant
    update["go"] = raffle.current_game.go
    update["stop"] = raffle.stop
    return(update)
