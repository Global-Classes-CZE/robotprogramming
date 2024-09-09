from utime import ticks_ms, ticks_diff
from lights_controller import LightsController

controller = LightsController()

last_action_time = ticks_ms()
state = 0
blinker_state = "no"

def main_sequence(controller):
    global state, last_action_time, blinker_state
    current_time = ticks_ms()
    controller.indikuj(blinker_state)

    if state == 0:  # Lights ON
        controller.turn_on_lights()
        last_action_time = current_time
        blinker_state = "no"
        state = 1

    elif state == 1 and ticks_diff(current_time, last_action_time) >= 1000:  # Brake lights ON
        controller.start_breaking()
        last_action_time = current_time
        state = 2

    elif state == 2 and ticks_diff(current_time, last_action_time) >= 1000:  # Brake lights OFF
        controller.stop_breaking()
        last_action_time = current_time
        state = 3

    elif state == 3 and ticks_diff(current_time, last_action_time) >= 1000:  # Reverse lights ON
        controller.start_reverse_light()
        last_action_time = current_time
        state = 4

    elif state == 4 and ticks_diff(current_time, last_action_time) >= 1000:  # Reverse lights OFF
        controller.stop_reverse_light()
        last_action_time = current_time
        state = 5

    elif state == 5 and ticks_diff(current_time, last_action_time) >= 1000:  # Lights OFF
        controller.turn_off_lights()
        last_action_time = current_time
        state = 6

    elif state == 6 and ticks_diff(current_time, last_action_time) >= 1000:  # Indicate left direction
        blinker_state = "left"
        last_action_time = current_time
        state = 7

    elif state == 7 and ticks_diff(current_time, last_action_time) >= 4000:  # Indicate right direction
        blinker_state = "right"
        last_action_time = current_time
        state = 8
    elif state == 8 and ticks_diff(current_time, last_action_time) >= 4000:
        state = 0



# Code in a 'while True:' loop repeats forever
while True:
    main_sequence(controller)

