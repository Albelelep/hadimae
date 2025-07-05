from telethon import TelegramClient
from telethon.tl.types import PeerChannel
import time
import json

api_id = 'ISI_API_ID'
api_hash = 'ISI_API_HASH'
group_chat_id = ISI_CHAT_ID  # tanpa tanda kutip, contoh: -1001234567890

client = TelegramClient('session_name', api_id, api_hash)
client.start()

group = client.get_entity(PeerChannel(int(group_chat_id)))

with open("dump.json", "w", encoding="utf-8") as file1:
    file1.write("[")  # Awal array JSON
    c = 0
    m = 0
    first = True
    for event in client.iter_admin_log(group):
        if event.deleted_message:
            print("Dumping message", c, "(", event.old.id, event.old.date,")")
            if not first:
                file1.write(",")
            file1.write(event.old.to_json())
            first = False
            c += 1
            if event.old.media:
                m += 1
                client.download_media(event.old.media, str(event.old.id))
                print(" Dumped media", m)
            time.sleep(0.1)
    file1.write("]")  # Akhir array JSON 