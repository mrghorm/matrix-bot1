from importlib import util
import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText)

async_client = AsyncClient(
        "https://matrix.mrghorm.com", "mrghorm3"
)


async def main():
    response = await async_client.login("uouLsvgVKQ7YWn87hiZt")
    print(response)

    response_string = "!replybot"

    #### Read token from "next_batch" to figure out where the bot left off from last run ###
    # we read the previously-written token...
    with open ("next_batch","r") as next_batch_token:
        # ... and well async_client to use it
        async_client.next_batch = next_batch_token.read()

    while (True):
        ### Wait for response from server
        sync_response = await async_client.sync(30000)

        # Sync response
        print(sync_response)

        invites = sync_response.rooms.invite
        for room_id in invites:
            await async_client.join(room_id)

        joins = sync_response.rooms.join
        for room_id in joins:
            for event in joins[room_id].timeline.events:
                if hasattr(event, 'body') and event.body.startswith(response_string):
                    response_body = event.body.replace(response_string, "").strip()
                    content = {
                        "body": response_body,
                        "msgtype": "m.text"
                    }
                    await async_client.room_send(room_id, 'm.room.message', content)


        # Write next_batch to file so we can pick up where we left off from last run
        with open("next_batch", "w") as next_batch_token:
            next_batch_token.write(sync_response.next_batch)

asyncio.run(main())

