from telethon import TelegramClient
import logging
from config import API_ID, API_HASH
import mapper
import walker

logging.basicConfig(format='[%(asctime)s.%(msecs)d] %(levelname)s:%(name)s:%(funcName)s [lineno %(lineno)d] %(message)s',
                    datefmt='%H:%M:%S', level=logging.WARNING)

if __name__ == "__main__":
    client = TelegramClient('AnTi3z', API_ID, API_HASH)
    client.start()
    mapper.activate(client)
    # walker.activate(client)
    client.run_until_disconnected()
