import time
import random
import logging
from typing import Optional

from telethon import errors
from telethon.tl.custom.messagebutton import MessageButton

logger = logging.getLogger('ButtonClicker')
logger.setLevel(logging.INFO)


class ButtonClicker:
    _instances = {}

    @classmethod
    def get_clicker(cls, chat_id) -> 'ButtonClicker':
        if chat_id not in cls._instances:
            cls._instances[chat_id] = cls()
        return cls._instances[chat_id]

    def __init__(self):
        self._last_button = None

    @staticmethod
    def find_button(msg, i=None, j=None, *, text=None, filter=None, data=None) -> Optional[MessageButton]:
        # See telethon.tl.custom.message.Message.click:
        # https://docs.telethon.dev/en/latest/modules/custom.html#telethon.tl.custom.message.Message.click

        buttons_flat = [x for row in msg.buttons for x in row]

        if data is not None:
            for button in buttons_flat:
                if button.data.decode() == data:
                    return button
            return None

        if sum(int(x is not None) for x in (i, text, filter)) >= 2:
            raise ValueError('You can only set either of i, text or filter')

        if text is not None:
            if callable(text):
                for button in buttons_flat:
                    if text(button.text):
                        return button
            else:
                for button in buttons_flat:
                    if button.text == text:
                        return button
            return

        if filter is not None:
            for button in buttons_flat:
                if filter(button):
                    return button
            return

        if i is None:
            return None
        if j is None:
            return buttons_flat[i]
        else:
            return msg.buttons[i][j]

    async def click_cb_data(self, msg, data):
        button = self.find_button(msg, data=data)
        if button:
            await self.click(button)

    async def click(self, button: MessageButton):
        if not button:
            return

        self._last_button = button
        time.sleep(random.uniform(1.1, 2.5))
        btn_data = self._last_button.data.decode()
        try:
            await self._last_button.click()
            self._last_button = None
            logger.debug(f"Button {btn_data} click success")
        except errors.BotResponseTimeoutError:
            logger.warning(f"Button {btn_data} answer timeout")
        except errors.MessageIdInvalidError:
            self._last_button = None
            logger.warning(f"Message with {btn_data} was deleted")

    async def reclick(self):
        if self._last_button:
            logger.info(f"Retry {self._last_button.data.decode()} click")
            await self.click(self._last_button)
