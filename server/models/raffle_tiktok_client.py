#!/usr/bin/python3
"""
raffle_tiktok_client.py: contains the defination of RaffleTikTokClient class.
"""
from models.base_model import BaseModel
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import GiftEvent, \
    CommentEvent, DisconnectEvent, JoinEvent, ViewerUpdateEvent


class RaffleTikTokClient(BaseModel):
    """
    RaffleTikTokClient: A model that is used to manage raffle game
        tiktok clients.
    """

    raffle = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.update(**kwargs)
        self.client: TikTokLiveClient = \
            TikTokLiveClient(unique_id=self.raffle.unique_id)
        
        print(f"""\
Client instance created
Unique id: {self.raffle.unique_id}\
""")
        
        self.client.add_listener("connect", self.on_connect)
        self.client.add_listener("gift", self.on_gift)
        self.client.add_listener("disconnect", self.on_disconnect)
        self.client.add_listener("viewer_update", self.on_viewer_update)

    async def on_connect(self, _):
        """
        on_connect: called when the server connects with the live
            tiktok client.
        """
        print("Connected to Room ID:", self.client.room_id)

    async def on_viewer_update(self, event: ViewerUpdateEvent):
        """
        on_viewer_update: called when a there is an update in the number of
            viewer of the live streame.
        """
        print(f"New Viewer Count: {event.viewer_count}")
        self.raffle.viewers = event.viewer_update


    async def on_gift(self, event: GiftEvent):
        """
        on_gift: executes when gift are sent. Checks if the sent gift is
            eligible for Raffle if eligible adds the user as a participant
        Args:
            event (:obj:): The GiftEvent object generated when the
                event occured.
        """
        game = self.raffle.current_game
        if game.is_gift_eligible(event):
            if game.state == "ACTIVE":
                if event.gift.info.type == 1 and event.gift.streaking:
                    print(f"{event.user.unique_id} sent {event.gift.count}x (in a streak) \
\"{event.gift.info.name}\"",
                          "RAFFLE Already Started")
                elif event.gift.streakable and event.gift.streaking:
                    print(f"{event.user.unique_id} sent {event.gift.count}x (in a streak) \
\"{event.gift.info.name}\"",
                          "RAFFLE Already Started")
                else:
                    print(f"{event.user.unique_id} sent \"{event.gift.info.name}\"",
                          "RAFFLE Already Started")
                return
            
            if event.gift.info.type == 1 and event.gift.streaking:
                print(f"{event.user.unique_id} sent {event.gift.count}x (in a streak) \
\"{event.gift.info.name}\"", "GIFT FOR ENTRY")
            elif event.gift.streakable and event.gift.streaking:
                print(f"{event.user.unique_id} sent {event.gift.count}x (in a streak) \
\"{event.gift.info.name}\"", "GIFT FOR ENTRY")
            else:
                print(f"{event.user.unique_id} sent \"{event.gift.info.name}\"",
                      "GIFT FOR ENTRY")
            game.add_participant(event.user.unique_id, event.gift.count)
            game.if_ready_start()

    async def on_disconnect(self, event: DisconnectEvent):
        """
        on_disconnect: executed when clinte stops live stream.
            or when the server disconnects from the client.
        
        Args:
            event (:obj:): The DisconnectEvent object generated when the
                event occured.
        """
        self.raffle.stop = True
        print("Client disconnected Raffle terminated")

