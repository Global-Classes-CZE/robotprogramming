from microbit import button_a, button_b
from utime import ticks_us, ticks_diff

from system import System
from wheel_driver import WheelDriver


class Action:
    def __init__(self, name, while_sensor, until_sensor):
        self.name = name
        self.while_sensor = while_sensor
        self.until_sensor = until_sensor

    def __str__(self):
        return self.name


class State:
    def __init__(self, name, symbol, actions):
        self.name = name
        self.symbol = symbol
        self.actions = actions

    def __str__(self):
        return self.name


# Actions of the robot
ACTIONS = dict(
    #  waits with wheels.stop() for button to be pressed to start moving
    START=Action("Start", -1, -1),
    # moves forward, no rotation
    FWD=Action("Fwd", 0b010, -1),
    #  moves forward with slight turn from the left to right (left sensor triggered)
    FWD_L=Action("Fwd-L", 0b100, 0b010),
    #  moves forward with slight turn from the right to left (right sensor triggered)
    FWD_R=Action("Fwd-R", 0b001, 0b010),
    STOP=Action("Stop", -1, -1),  # stops the robot
)

# States of the robot
# Each state is defined declaratively, indicating:
# - sensor state for entering the state
# - commands to execute and sensor state (series) to expect for transition from command to command
# - sensor state for leaving the state
# - supported transitions to other states
STATES = dict(
    #  waits with wheels.stop() for button to be pressed to start moving
    START=State("Start", '.', [ACTIONS["START"]]),
    #  follows the line
    LINE=State("Line", '|', [ACTIONS["FWD"], ACTIONS["FWD_L"], ACTIONS["FWD_R"]]),
    #  stops the robot
    STOP=State("stop", 's', [ACTIONS["STOP"]]),
    #  error state
    ERROR=State("error", 'x', [ACTIONS["STOP"]]),
)

STATE_TRANSITIONS = {
    STATES["START"]: [STATES["LINE"]],
    STATES["LINE"]: [STATES["STOP"]],
    STATES["STOP"]: [STATES["START"]],
    STATES["ERROR"]: [STATES["START"]],
}


def transition_to_state(state_now, action_now, state):
    """Transitions to state, a one-liner helper for main code."""
    state_new = STATES[state]
    action_new = state_new.actions[0]
    system.display_drive_mode(state_new.symbol)
    print("Transitioning state %s (action %s) to state %s (action %s)" % (state_now, action_now, state_new, action_new))
    return state_new, action_new, 0


def transition_state_action(state, action_now, lcr):
    """Transitions within the state based on the line sensor readings."""
    # print("Trans state %s action %s, %s" % (state, action_now, bin(lcr)))
    print("Transitioning from state %s action %s, %s" % (state, action_now, bin(lcr)))
    action_idx = 0
    for action in state.actions:
        if action.while_sensor == lcr:
            print("Transitioning state %s action %s to %s" % (state, action_now, action))
            return state, action, action_idx
        action_idx += 1
    return state, action_now, action_idx


if __name__ == "__main__":
    # Tries to track a line, stop at first indecision (no line for 3 secs, intersection).
    system = System()
    wheels = WheelDriver(
        system=system,
        left_pwm_min=80, left_pwm_multiplier=0.08944848, left_pwm_shift=-2.722451,
        right_pwm_min=80, right_pwm_multiplier=0.08349663, right_pwm_shift=-2.0864
    )
    wheels.stop()

    # Well working configurations:
    # Lenient slow:
    # tolerance = 45, fwd_speed = 6, losing_start = 1, increment_per_cycle = 20, max = start * 20
    # Aggressive slow:
    # tolerance = 45, fwd_speed = 6, losing_start = 3, increment_per_cycle = 15, max = start * 7
    # Recorded:
    # tolerance = 45, fwd_speed = 9, losing_start = 2, increment_per_cycle = 4, max = start * 8

    # base forward speed (rad)
    forward_speed = 9
    # how much to decrement each cycle when on side sensor (too low = lazy reaction)
    side_speed_dec_per_cycle = 3
    # the minimum rotation speed to maintain to not go too low
    # and unnecessarily slow down turning (it turns no matter what as long as rotation speeds are correct)
    side_speed_min = forward_speed * 0.5
    # starting rotation (rad) when side sensor picks up the line instead of center one
    side_rotation_init = 2
    # how fast we'll be increasing rotation speed each cycle we are out of center
    # this continues even if we are out of side sensor due to tolerance cycles (see below)
    side_rotation_inc_per_cycle = 6
    # maximum rotation we can perform (to not get too crazy and take our time when turning)
    side_rotation_max = side_rotation_init * 8

    # tolerance before declaring we're out of line (time-dependent)
    # (if turning too slow, we might not catch the line again if too low)
    line_cycle_tolerance = 45
    # tolerance before assuming we are in error (hence stop, then start)
    error_cycle_tolerance = 2

    state = STATES["START"]
    action_idx = 0
    action = state.actions[action_idx]
    system.display_on()
    system.display_drive_mode(state.symbol)
    out_of_state_cycle = 0
    line_losing_cycle = 0

    try:
        regulation_cycle_length = 50_000
        regulation_cycle_start = ticks_us()
        ll, lc, lr, li, ri = system.get_sensors()

        while not button_a.is_pressed():
            wheels.update()
            ll_old, lc_old, lr_old, li_old, ri_old = ll, lc, lr, li, ri
            ll, lc, lr, li, ri = system.get_sensors()
            if (ll, lc, lr, li, ri) != (ll_old, lc_old, lr_old, li_old, ri_old):
                system.display_sensors(ll, lc, lr, li, ri)

            time_now = ticks_us()
            if ticks_diff(time_now, regulation_cycle_start) > regulation_cycle_length:
                regulation_cycle_start = time_now
                lcr = (ll << 2) | (lc << 1) | lr
                # special actions w/o sensor dependency
                if action.while_sensor == -1 and action.until_sensor == -1:
                    if action == ACTIONS["START"]:
                        wheels.stop()
                        if button_b.is_pressed():
                            print("B pressed, starting")
                            state, action, action_idx = transition_to_state(state, action, "LINE")
                    elif action == ACTIONS["STOP"]:
                        wheels.stop()
                        if button_b.is_pressed():
                            state, action, action_idx = transition_to_state(state, action, "START")

                # stop immediately (no tolerance in existing state) and return to the start
                # intentionally done to not resolve more advanced situations (so we can move the robot somewhere else)
                elif lcr == 0b111:
                    out_of_state_cycle += 1
                    if out_of_state_cycle > error_cycle_tolerance:
                        state, action, action_idx = transition_to_state(state, action, "START")

                # keeping the current action within state if its while_sensor matches
                elif (((action.while_sensor == -1 or lcr == action.while_sensor) and
                      (action.until_sensor == -1 or lcr != action.until_sensor))) \
                        or out_of_state_cycle < line_cycle_tolerance:
                    if lcr == action.while_sensor:
                        if out_of_state_cycle > 0:
                            out_of_state_cycle = 0
                            print("Back in state")
                    else:
                        state, action, action_idx = transition_state_action(state, action, lcr)
                    if action == ACTIONS["FWD"]:
                        print("FWD, rad %s" % forward_speed)
                        wheels.move(speed_rad=forward_speed, rotation_rad=0)
                        line_losing_cycle = 1  # set to 1 to immediately start with the first increment if we lose line
                    elif action == ACTIONS["FWD_L"]:
                        line_losing_cycle += 1
                        rotation_rad = side_rotation_init + side_rotation_inc_per_cycle * line_losing_cycle
                        rotation_rad = min(rotation_rad, side_rotation_max)
                        align_speed = forward_speed - line_losing_cycle * side_speed_dec_per_cycle
                        align_speed = max(align_speed, side_speed_min)
                        wheels.move(speed_rad=align_speed, rotation_rad=rotation_rad)
                        print(
                            "FWD_L, rotation_rad %d, init %s + inc_per_cycle %s * cycle %s" %
                            (rotation_rad, side_rotation_init, side_rotation_inc_per_cycle, line_losing_cycle))
                    elif action == ACTIONS["FWD_R"]:
                        line_losing_cycle += 1
                        rotation_rad = side_rotation_init + side_rotation_inc_per_cycle * line_losing_cycle
                        rotation_rad = min(rotation_rad, side_rotation_max)
                        print(
                            "FWD_R, rotation_rad %d, init %s + inc_per_cycle %s * cycle %s" %
                            (rotation_rad, side_rotation_init, side_rotation_inc_per_cycle, line_losing_cycle))
                        align_speed = forward_speed - line_losing_cycle * side_speed_dec_per_cycle
                        align_speed = max(align_speed, side_speed_min)
                        wheels.move(speed_rad=align_speed, rotation_rad=-rotation_rad)
                    elif action == ACTIONS["STOP"]:
                        wheels.stop()

                # transition to another action while waiting to reach until_sensor (i.e., during turning)

                else:
                    print("Out of state exceeded %d cycles tolerance" % line_cycle_tolerance)
                    state, action, action_idx = transition_to_state(state, action, "STOP")

    finally:
        wheels.stop()
        system.display_off()
        print("Finished")
