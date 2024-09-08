from microbit import pin0
from neopixel import NeoPixel
from light import Light
from light_placement import LightPlacement

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
        # controls the shared lights for headlight and beam headlight indication
        # with the following priority: reverse (left only, see placement) > brake > back
        self.head_enabled = False  # keeps headlight on after beam lights go off
        self.beam_enabled = False  # keeps headlight on after beam lights go off
        # controls the shared lights for back, brake and reverse indication
        # with the following priority: reverse (left only, see placement) > brake > back
        self.back_enabled = False
        self.brake_enabled = False
        self.reverse_enabled = False
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

    def head_on(self):
        """Turns the headlights on. If beam headlights are on, lights are unaffected."""
        self.head_enabled = True
        if not self.beam_enabled:
            for light_pos in LightPlacement.headlights:
                self.lights[light_pos].set_color(LightPlacement.WHITE_MILD)
                self.lights[light_pos].on()

    def head_off(self):
        """Turns the headlights off."""
        self.head_enabled = False
        if not self.beam_enabled:
            for light_pos in LightPlacement.headlights:
                self.lights[light_pos].off()

    def beam_on(self):
        """Turns the beam headlights on."""
        self.beam_enabled = True
        for light_pos in LightPlacement.headlights:
            self.lights[light_pos].set_color(LightPlacement.WHITE_BRIGHT)
            self.lights[light_pos].on()

    def beam_off(self):
        """Turns the beam headlights off. If standard headlights are on,
        the shared lights are switched to them."""
        self.beam_enabled = False
        for light_pos in LightPlacement.headlights:
            if self.head_enabled is True:
                self.head_on()
            else:
                self.lights[light_pos].off()

    def blink(self, direction, blink_frequency_ms):
        """Blinks the light(s) indicating the given direction."""
        for position in LightPlacement.blinkers[direction]:
            self.lights[position].blink(blink_frequency_ms)

    def blink_emergency(self, blink_frequency_ms):
        """Blinks all turn-indicating light(s) to signal an emergency."""
        self.blink(LightPlacement.LEFT_DIRECTION, blink_frequency_ms)
        self.blink(LightPlacement.RIGHT_DIRECTION, blink_frequency_ms)

    def blink_off(self):
        """Stops blinking on all blinker lights."""
        for position in LightPlacement.blinkers[LightPlacement.LEFT_DIRECTION]:
            self.lights[position].off()
        for position in LightPlacement.blinkers[LightPlacement.RIGHT_DIRECTION]:
            self.lights[position].off()

    def is_blinking(self, direction):
        """Checks if the light(s) indicating the given direction are blinking."""
        position_first = LightPlacement.blinkers[direction][0]
        return self.lights[position_first].is_blinking()

    def off(self):
        """Turns all the lights off."""
        for light in self.lights:
            light.off()

    def back_on(self):
        """Turns the backlights on. If brake lights are on, shared lights
        are unaffected. Enabled reverse lights is also unaffected."""
        self.back_enabled = True
        self.update_back()

    def back_off(self):
        """Turns the backlights off."""
        self.back_enabled = False
        self.update_back()

    def brake_on(self):
        """Turns the brake lights on."""
        self.brake_enabled = True
        self.update_back()

    def brake_off(self):
        """Turns the brake lights off. If backlights are on,
        the shared lights are switched to them, kept on."""
        self.brake_enabled = False
        self.update_back()

    def reverse_on(self):
        """Turns the reverse light on."""
        self.reverse_enabled = True
        self.update_back()

    def reverse_off(self):
        """Turns the reverse light off."""
        self.reverse_enabled = False
        self.update_back()

    def update_back(self):
        """Updates the backlights based on the current state of shared back,
        brake and reverse lights. The priority is reverse > brake > back.
        If reverse is on, only the reverse light is on."""
        for light_pos in LightPlacement.backlights:
            light_is_reverse = light_pos in LightPlacement.reverse_lights
            if self.reverse_enabled is True and light_is_reverse:
                self.lights[light_pos].set_color(LightPlacement.WHITE_MID)
                self.lights[light_pos].on()
            elif self.brake_enabled is True:
                self.lights[light_pos].set_color(LightPlacement.RED_BRIGHT)
                self.lights[light_pos].on()
            elif self.back_enabled is True:
                self.lights[light_pos].set_color(LightPlacement.RED_MILD)
                self.lights[light_pos].on()
            else:
                self.lights[light_pos].off()
