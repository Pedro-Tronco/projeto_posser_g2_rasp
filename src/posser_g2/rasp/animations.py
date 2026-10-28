from __future__ import annotations

from threading import Event, Lock, Thread, current_thread
from time import sleep


class AnimationService:
    """Controls status LEDs and an active buzzer using BCM GPIO pin numbers."""

    def __init__(
        self,
        green_led_pin: int = 17,
        red_led_pin: int = 27,
        buzzer_pin: int = 18,
    ) -> None:
        pins = (green_led_pin, red_led_pin, buzzer_pin)
        if any(
            isinstance(pin, bool) or not isinstance(pin, int) or pin < 0
            for pin in pins
        ):
            raise ValueError("GPIO pins must be non-negative integers")
        if len(set(pins)) != len(pins):
            raise ValueError("Each animation must use a different GPIO pin")

        self._green_led_pin = green_led_pin
        self._red_led_pin = red_led_pin
        self._buzzer_pin = buzzer_pin
        self._gpio_initialized = False
        self._gpio_lock = Lock()
        self._animation_lock = Lock()
        self._waiting_stop_event: Event | None = None
        self._waiting_thread: Thread | None = None

    def show_open(self) -> None:
        self._stop_waiting_animation()
        self._set_leds(green=True, red=False)
        self._play_pattern((0.15,))

    def show_closed(self) -> None:
        self._stop_waiting_animation()
        self._set_leds(green=False, red=True)
        self._play_pattern((0.12, 0.12, 0.12))

    def show_waiting(self) -> None:
        self._stop_waiting_animation()
        self._set_leds(green=False, red=False)
        self._play_pattern((0.05,))

        stop_event = Event()
        thread = Thread(
            target=self._blink_green,
            args=(stop_event,),
            name="rfid-waiting-animation",
            daemon=True,
        )
        with self._animation_lock:
            self._waiting_stop_event = stop_event
            self._waiting_thread = thread
            thread.start()

    def beep_rfid_read(self) -> None:
        self._play_pattern((0.08,))

    def stop(self) -> None:
        self._stop_waiting_animation()
        if not self._gpio_initialized:
            return
        self._set_leds(green=False, red=False)
        self._write_output(self._buzzer_pin, False)

    def close(self) -> None:
        self.stop()
        if not self._gpio_initialized:
            return

        import RPi.GPIO as GPIO

        with self._gpio_lock:
            GPIO.cleanup(
                [self._green_led_pin, self._red_led_pin, self._buzzer_pin]
            )
            self._gpio_initialized = False

    def _blink_green(self, stop_event: Event) -> None:
        while not stop_event.is_set():
            self._write_output(self._green_led_pin, True)
            if stop_event.wait(0.5):
                break
            self._write_output(self._green_led_pin, False)
            stop_event.wait(0.5)
        self._write_output(self._green_led_pin, False)

    def _stop_waiting_animation(self) -> None:
        with self._animation_lock:
            stop_event = self._waiting_stop_event
            thread = self._waiting_thread
            self._waiting_stop_event = None
            self._waiting_thread = None
            if stop_event is not None:
                stop_event.set()

        if thread is not None and thread is not current_thread():
            thread.join()

    def _set_leds(self, *, green: bool, red: bool) -> None:
        self._write_output(self._green_led_pin, green)
        self._write_output(self._red_led_pin, red)

    def _play_pattern(self, durations: tuple[float, ...]) -> None:
        for index, duration in enumerate(durations):
            self._write_output(self._buzzer_pin, True)
            sleep(duration)
            self._write_output(self._buzzer_pin, False)
            if index < len(durations) - 1:
                sleep(0.1)

    def _write_output(self, pin: int, value: bool) -> None:
        self._ensure_gpio_setup()

        import RPi.GPIO as GPIO

        with self._gpio_lock:
            GPIO.output(pin, GPIO.HIGH if value else GPIO.LOW)

    def _ensure_gpio_setup(self) -> None:
        if self._gpio_initialized:
            return

        import RPi.GPIO as GPIO

        with self._gpio_lock:
            if self._gpio_initialized:
                return

            mode = GPIO.getmode()
            if mode is None:
                GPIO.setmode(GPIO.BCM)
            elif mode != GPIO.BCM:
                raise RuntimeError(
                    "AnimationService requires GPIO.BCM pin numbering"
                )

            GPIO.setup(
                [self._green_led_pin, self._red_led_pin, self._buzzer_pin],
                GPIO.OUT,
                initial=GPIO.LOW,
            )
            self._gpio_initialized = True
