import time
import random
import logging

from telethon import errors

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
    def find_button(msg, i=None, j=None, *, text=None, filter=None, data=None):
        # See telethon.tl.custom.message.Message.click:
        # https://docs.telethon.dev/en/latest/modules/custom.html#telethon.tl.custom.message.Message.click

        buttons_flat = [x for row in msg.buttons for x in row]

        for button in buttons_flat:
            if button.data.decode() == data:
                return button

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
            i = 0
        if j is None:
            return buttons_flat[i]
        else:
            return msg.buttons[i][j]

    async def click_cb_data(self, msg, data):
        btn = self.find_button(msg, data=data)
        if btn:
            await self.click(btn)

    async def click(self, button):
        self._last_button = button
        await self.reclick()

    async def reclick(self):
        if not self._last_button:
            return

        time.sleep(random.uniform(1.1, 2.5))
        btn_data = self._last_button.data.decode()
        try:
            await self._last_button.click()
            self._last_button = None
            logger.info(f"Button {btn_data} click success")
        except errors.BotResponseTimeoutError:
            logger.warning(f"Button {btn_data} answer timeout")
        except errors.MessageIdInvalidError:
            self._last_button = None
            logger.warning(f"Message with {btn_data} was deleted")