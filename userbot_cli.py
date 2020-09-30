import logging

from telethon import TelegramClient

# import mapper
import walker
import config

logging.basicConfig(
    format='[%(asctime)s.%(msecs)d] %(levelname)s:%(name)s:%(funcName)s [lineno %(lineno)d] %(message)s',
    datefmt='%H:%M:%S', level=logging.WARNING)

if __name__ == "__main__":
    api = config.load_config('api')
    client = TelegramClient('AnTi3z', api['id'], api['hash'])
    client.start()
    # mapper.activate(client)
    walker.activate(client)
    client.run_until_disconnected()
