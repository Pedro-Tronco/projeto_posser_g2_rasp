from __future__ import annotations

from threading import Event
from time import sleep
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mfrc522 import SimpleMFRC522


class MFRC522Reader:
    def __init__(self) -> None:
        self._reader: SimpleMFRC522 | None = None
        self._stop_event = Event()

    def read(self) -> int | None:
        if self._reader is None:
            from mfrc522 import SimpleMFRC522

            self._reader = SimpleMFRC522()

        while not self._stop_event.is_set():
            tag = self._reader.read_id_no_block()
            if tag is not None:
                return tag
            sleep(0.1)

        return None

    def stop(self) -> None:
        self._stop_event.set()

    def close(self) -> None:
        self.stop()
        if self._reader is None:
            return

        import RPi.GPIO as GPIO

        GPIO.cleanup()
        self._reader = None
