from microbit import pin0
from neopixel import NeoPixel
from Light import Light


class LightPlacement:
    """Defines the color scheme and placement used in the Joy-Car Robot."""
    LEFT_DIRECTION = 0
    RIGHT_DIRECTION = 1

    blinkers = {
        LEFT_DIRECTION: [1, 4],
        RIGHT_DIRECTION: [2, 7]
    }
    front_lights = [0, 3]
    back_lights = [5, 6]

    WHITE_BRIGHT = (255, 255, 255)
    WHITE_MILD = (30, 30, 30)
    ORANGE = (255, 165, 0)
    RED_BRIGHT = (255, 0, 0)
    RED_MILD = (30, 0, 0)

    initial_color_for_position = [
        WHITE_MILD, ORANGE, ORANGE, WHITE_MILD,
        ORANGE, RED_MILD, RED_MILD, ORANGE
    ]

    def __init__(self):
        pass


class LightDriver:
    """Handles the light subsystem of Joy-Car Robot, utilizing NeoPixel light strip.
    Each light is represented by a Light object, which is capable of maintaining
    its state and providing it when an update is needed on the hardware side."""

    def __init__(self):
        """Initializes the light driver with all lights initially switched off."""
        self.lights = [
            Light(idx, on_color=LightPlacement.initial_color_for_position[idx])
            for idx in range(8)
        ]
        self.neopixel = NeoPixel(pin0, 8)
        self.light_front_enabled = False  # keeps front on after beam lights go off
        self.light_back_enabled = False  # keeps back on after brake lights go off
        self.update()

    def update(self):
        """Updates the light driver, propagating the changes to the hardware.
        Each light provides its state only if a state propagation is needed,
        otherwise it is skipped. If all lights are up-to-date, no-op is performed."""
        write_required = False
        for light in self.lights:
            light_state = light.update()
            if light_state is not None:
                self.neopixel[light.position] = light_state
                write_required = True
        if write_required:
            self.neopixel.write()

    def front_on(self):
        """Turns the front lights on."""
        for light_pos in LightPlacement.front_lights:
            self.lights[light_pos].set_color(LightPlacement.WHITE_MILD)
            self.lights[light_pos].on()
        self.light_front_enabled = True

    def front_off(self):
        """Turns the front lights off."""
        for light_pos in LightPlacement.front_lights:
            self.lights[light_pos].off()
        self.light_front_enabled = False

    def front_beam_on(self):
        """Turns the front beam lights on."""
        for light_pos in LightPlacement.front_lights:
            self.lights[light_pos].set_color(LightPlacement.WHITE_BRIGHT)
            self.lights[light_pos].on()

    def front_beam_off(self):
        """Turns the front beam lights off. If standard front lights are on,
        the shared lights are switched to them."""
        for light_pos in LightPlacement.front_lights:
            if self.light_front_enabled is True:
                self.front_on()
            else:
                self.lights[light_pos].off()

    def blink(self, direction, blink_frequency_ms):
        """Blinks the light(s) indicating the given direction."""
        for position in LightPlacement.blinkers[direction]:
            self.lights[position].blink(blink_frequency_ms)

    def blink_off(self):
        """Stops blinking on all blinker lights."""
        for position in LightPlacement.blinkers[LightPlacement.LEFT_DIRECTION]:
            self.lights[position].off()
        for position in LightPlacement.blinkers[LightPlacement.RIGHT_DIRECTION]:
            self.lights[position].off()

    def off(self):
        """Turns all the lights off."""
        for light in self.lights:
            light.off()

    def back_on(self):
        """Turns the backlights on."""
        for light_pos in LightPlacement.back_lights:
            self.lights[light_pos].set_color(LightPlacement.RED_MILD)
            self.lights[light_pos].on()
        self.light_back_enabled = True

    def back_off(self):
        """Turns the backlights off."""
        for light_pos in LightPlacement.back_lights:
            self.lights[light_pos].off()
        self.light_back_enabled = False

    def brake_on(self):
        """Turns the brake lights on."""
        for light_pos in LightPlacement.back_lights:
            self.lights[light_pos].set_color(LightPlacement.RED_BRIGHT)
            self.lights[light_pos].on()

    def brake_off(self):
        """Turns the brake lights off. If backlights are on,
        the shared lights are switched to them, kept on."""
        for light_pos in LightPlacement.back_lights:
            if self.light_back_enabled is True:
                self.back_on()
            else:
                self.lights[light_pos].off()

