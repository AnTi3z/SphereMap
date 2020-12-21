import logging
import asyncio

logger = logging.getLogger('Timer')
logger.setLevel(logging.INFO)


class Timer:
    def __init__(self, worker, name=""):
        self._task = None
        self._worker = worker
        self._name = name

    def _do_work(self):
        logger.info(f"Timer({self._name}) triggered")
        self._worker()

    def stop(self):
        if self._task:
            self._task.cancel()
            logger.debug(f"Timer({self._name}) stopped: {self._task}")

    def start(self, delay):
        self.stop()
        self._task = asyncio.get_event_loop().call_later(delay, self._do_work)
        logger.info(f"Timer({self._name}) started for {delay} sec")
