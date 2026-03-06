import os
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest, EditBannedRequest
from telethon.tl.types import ChannelParticipantsRequests, ChatBannedRights
from flask import Flask, jsonify

# Environment Variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Optional, can use bot instead of user
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Numeric ID of your channel

# Telegram client (Userbot)
client = TelegramClient('userbot', API_ID, API_HASH)

app = Flask(__name__)

@app.route("/approve", methods=["GET"])
def approve_pending():
    with client:
        pending_users = client.get_participants(CHANNEL_ID, filter=ChannelParticipantsRequests)
        count = 0
        for user in pending_users:
            try:
                # Approve by removing restrictions (if any)
                client(EditBannedRequest(
                    CHANNEL_ID,
                    user.id,
                    ChatBannedRights(
                        until_date=None,
                        view_messages=False  # Remove ban
                    )
                ))
                count += 1
            except:
                continue
    return jsonify({"status": "success", "approved_count": count})

if __name__ == "__main__":
    client.start()
    app.run(host="0.0.0.0", port=5000)
