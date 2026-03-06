import os
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantsRequests

# Environment Variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Userbot client (required to approve pending members)
client = TelegramClient('userbot', API_ID, API_HASH)

# Bot client
from telethon import TelegramClient as BotClient
bot = BotClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def approve_pending():
    pending = await client.get_participants(CHANNEL_ID, filter=ChannelParticipantsRequests)
    count = 0
    for user in pending:
        try:
            await client(EditBannedRequest(
                CHANNEL_ID,
                user.id,
                ChatBannedRights(until_date=None, view_messages=False)
            ))
            count += 1
        except:
            continue
    return count

# Bot event handler
@bot.on(events.NewMessage(pattern="/addMember"))
async def handler(event):
    await event.reply("Starting to approve all pending members...")
    count = await approve_pending()
    await event.reply(f"✅ Total {count} pending members approved and added to the channel.")

async def main():
    await client.start()
    print("Userbot logged in...")
    await bot.run_until_disconnected()

asyncio.run(main())
