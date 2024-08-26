import time


class LightMode:
    """Enumeration of light modes supported by the Light class."""
    PLAIN = 0
    BLINK = 1

    def __init__(self):
        pass


class Light:
    """Handles a single RGB light capable of holding its state and performing either
    instant operations or operations spread over time (blinking, ...).

    The class is designed to be used in a cooperative multitasking environment,
    where the caller is expected to call update() in a timely manner. The implementation
    maintains its state and indicates when a state should be propagated externally
    (on a change), but does NOT update any external hardware.

    It is expected the caller will use the state to update the hardware when needed.
    This is needed to allow multiple lights to be updated using a single call
    to the hardware, as designed by NeoPixel stripe handler."""

    def __init__(self, position, on_color):
        """Initializes light with the operational color, as turned off."""
        self.position = position
        self.on_color = on_color
        self.state = (0, 0, 0)
        self.changed = True
        self.mode = LightMode.PLAIN
        self.blink_frequency_ms = 0
        self.blink_start_time = 0

    def set_color(self, color):
        """Sets the light color, reflects immediately if the light is turned on."""
        self.on_color = color
        if self.state != (0, 0, 0):
            if self.state != color:
                self.changed = True
                self.state = color

    def on(self):
        """Turns the light on using the current on_color."""
        self.mode = LightMode.PLAIN
        if self.state != self.on_color:
            self.state = self.on_color
            self.changed = True

    def off(self):
        """Turns the light off."""
        self.mode = LightMode.PLAIN
        if self.state != (0, 0, 0):
            self.state = (0, 0, 0)
            self.changed = True

    def blink(self, blink_frequency_ms):
        """Blinks the light between black and on_color with the given frequency."""
        self.mode = LightMode.BLINK
        self.blink_frequency_ms = blink_frequency_ms
        self.blink_start_time = time.ticks_ms()

    def update(self):
        """Updates the light state based on the current mode and time."""
        if self.mode == LightMode.BLINK:
            time_delta = time.ticks_diff(time.ticks_ms(), self.blink_start_time)
            if time_delta >= self.blink_frequency_ms:
                self.blink_start_time = time.ticks_ms()
                if self.state == (0, 0, 0):
                    self.state = self.on_color
                else:
                    self.state = (0, 0, 0)
                self.changed = True
        if self.changed is True:
            self.changed = False
            return self.state
        else:
            return None
