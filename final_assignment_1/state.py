from system import System
from wheel_driver import WheelDriver
from math import sin, cos, pi


class Position:
    """A position in the city."""
    EAST = 0
    NORTH = pi / 2
    WEST = pi
    SOUTH = 3 * pi / 2

    def __init__(self, x: float, y: float, orientation: float):
        self.x = x
        self.y = y
        self.orientation = orientation

    def turn_left(self):
        self.orientation = (self.orientation + pi / 2) % (2 * pi)
        print("TURNED_TO: %s" % self)

    def turn_right(self):
        self.orientation = (self.orientation - pi / 2) % (2 * pi)

    def move_forward(self):
        x_old = self.x
        y_old = self.y
        self.x += round(cos(self.orientation))
        self.y += round(sin(self.orientation))
        print("MOVING_FORWARD: (%s, %s) -> (%s, %s)" % (x_old, y_old, self.x, self.y))

    def move_backward(self):
        self.x -= round(cos(self.orientation))
        self.y -= round(sin(self.orientation))

    def move_by_choice(self, choice: str, forward_accounted_for=False):
        if choice == '^':
            if not forward_accounted_for:
                self.move_forward()
        elif choice == '<':
            self.turn_left()
        elif choice == '>':
            self.turn_right()

    def copy(self):
        return Position(x=self.x, y=self.y, orientation=self.orientation)

    def str_orientation(self):
        if self.orientation == Position.EAST:
            return "EAST"
        elif self.orientation == Position.NORTH:
            return "NORTH"
        elif self.orientation == Position.WEST:
            return "WEST"
        elif self.orientation == Position.SOUTH:
            return "SOUTH"
        else:
            return str(self.orientation)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.str_orientation()})"

    def __repr__(self):
        return f"Position(x={self.x}, y={self.y}, orientation={self.str_orientation()})"


class Behavior:
    """The behavior of the robot."""

    def __init__(self,
                 # base forward speed (rad)
                 fwd_speed: float,
                 # how much to decrement each cycle when on side sensor (too low = lazy reaction)
                 side_speed_dec: float,
                 # the minimum rotation speed to maintain to not go too low
                 # and unnecessarily slow down turning (it turns no matter what as long as rotation speeds are correct)
                 side_speed_min: float,
                 # starting arc speed (rotation) when side sensor picks up the line instead of center one
                 side_arc_min: float,
                 # how fast we'll be increasing arc speed each cycle we are out of center
                 # this continues even if we are out of side sensor due to tolerance cycles (see below)
                 side_arc_inc: float,
                 # maximum arc speed we can perform (to not get too crazy and take our time when turning)
                 side_arc_max: float,
                 # tolerance before declaring we're out of line (time-dependent)
                 # (if turning too slow, we might not catch the line again if too low)
                 line_cycle_tolerance: int,
                 # base turn speed (rad)
                 turn_speed: float,
                 # base turn arc speed (rad)
                 turn_arc_speed: float,
                 # tolerance before declaring we're out of turn (time-dependent)
                 # (if turning too slow, we might not catch the line again if too low)
                 turn_cycle_tolerance: int,
                 # we disregard sensor transitions which last very short time
                 fast_sensor_change_dropped_below_cycle_count: int,
                 # how long the cycle is (in microseconds)
                 cycle_duration_us: int,
                 # Starting position in the city (after we reach the first intersection (i.e., we can be a bit off).
                 # If specified, we run in the city mode and the robot starts drawing the position on the screen.
                 # If not specified, we don't run in the city mode.
                 city_position: Position = None,
                 # navigation directions to take on the intersections
                 # (this includes also the turns which otherwise have no other option, just to fine-map the orientation)
                 # if not specified, the robot will not run in the interactive mode
                 navigation_directions: list[str] = None,
                 # Pause time between each intersection (in microseconds)
                 navigation_intersection_pause: int = 1_000_000,
                 # On a city grid, we compensate for flukes by protecting the state from implicit transitions
                 # in case the state is too short (we assume the grid has a minimum street distance we can utilize to avoid flukes)
                 line_state_implicit_transition_protection_after_switch_cycle_count: int = 0,
                 turn_state_implicit_transition_protection_after_switch_cycle_count: int = 0
                 ):
        self.fwd_speed = fwd_speed
        self.side_speed_dec = side_speed_dec
        self.side_speed_min = side_speed_min
        self.side_arc_min = side_arc_min
        self.side_arc_inc = side_arc_inc
        self.side_arc_max = side_arc_max
        self.line_cycle_tolerance = line_cycle_tolerance
        self.turn_speed = turn_speed
        self.turn_arc_speed = turn_arc_speed
        self.turn_cycle_tolerance = turn_cycle_tolerance
        self.fast_sensor_change_dropped_below_cycle_count = fast_sensor_change_dropped_below_cycle_count
        self.cycle_duration_us = cycle_duration_us
        self.city_position = city_position
        self.navigation_directions = navigation_directions
        self.navigation_intersection_pause = navigation_intersection_pause
        self.line_state_implicit_transition_protection_cycle_count = line_state_implicit_transition_protection_after_switch_cycle_count
        self.turn_state_implicit_transition_protection_cycle_count = turn_state_implicit_transition_protection_after_switch_cycle_count


class SensorMatcher:
    """A sensor matcher."""

    def __init__(self, optional: bool = False):
        self.optional = optional

    def matches(self, sensor, count) -> bool:
        pass


class SensorHasCount(SensorMatcher):
    """A sensor and how many times it needs to match."""

    def __init__(self, sensor: int, min_count: int, max_count: int = None, optional: bool = False):
        super().__init__(optional=optional)
        self.sensor = sensor
        self.min_count = min_count
        self.max_count = max_count

    def matches(self, sensor, count):
        if sensor != self.sensor:
            # print("Sensor mismatch: %s != %s" % (sensor, self.sensor))
            return False
        if self.max_count is not None:
            return self.min_count <= count <= self.max_count
        result = count >= self.min_count
        # print(f"Sensor {sensor:05b} ({count}x) match to {self.sensor:05b} ({count}x) -> result: %s" % result)
        return count >= self.min_count

    # let's print binary representation of the sensor and how many times it needs to match
    def __str__(self):
        return f"{self.sensor:0{5}b} ({self.min_count}x)"


class EitherSensorHasCount(SensorMatcher):
    """Multiple variants of a sensor, either of them must have count."""

    def __init__(self, sensors: list[SensorHasCount], optional: bool = False):
        super().__init__(optional=optional)
        self.sensors = sensors

    def matches(self, sensor, count):
        for sensor_has_count in self.sensors:
            # print(f"Matching {sensor_has_count} to {sensor:05b} ({count}x): {sensor_has_count.matches(sensor, count)}")
            if sensor_has_count.matches(sensor, count):
                # print("Matched")
                return True
        # print("Unmatched")
        return False

    def __str__(self):
        return f"Either{[str(sensor) for sensor in self.sensors]}"


class Ctx:
    """Carries the current operating context of the robot."""

    def __init__(self, system: System, wheels: WheelDriver, behavior: Behavior,
                 states: dict[str, 'State'], transitions: dict[str, list[str]], state_key: str):
        self.system = system
        self.wheels = wheels
        self.behavior = behavior
        self.states = states
        self.transitions = transitions
        self.state_key = None
        self.state = None
        self.sensor = None
        self.sensor_count = 0
        self.sensor_last = None
        self.state_action_cycle = 0
        self.state_out_of_bounds_cycle = 0
        self.state_cycle_since_transition = 0
        # history of sensor changes: [(lcr, count), ...]
        # we keep track of the last several sensor changes and use that to determine situation underneath us
        # this feeds to a sudden main state change if we detect different behavior than expected
        # each state has the ability to override other states if it thinks it should rule the car
        self.sensor_history = []
        # the history with extra element pertaining the current sensor and cycle count (updated just before state eval)
        self.sensor_history_with_current = []
        # Our history needs to be able to house at least 4 transitions
        # (going to intersection might be preceded by a single sensor if the car is going sideways)
        self.sensor_history_length = 10
        # carries max speed for each wheel (for display purposes)
        # will be updated on forward to correct values
        self.fwd_speed_pwm_left_max = 255
        self.fwd_speed_pwm_right_max = 255
        # runtime navigation directions (will be consumed as we go, we have backup in behavior if needed)
        self.navigation_directions = None
        # We will be using the city mode if the position is specified (and we will update position based on intersections)
        self.city_position = None
        # we need a flag to account for multi-state navigation at the same intersection (i.e., intersection enter + turn)
        self.city_position_forward_accounted_for = False
        self.reset_navigation_and_position()
        # initialize the state
        self.transition_to_state(state_key=state_key)
        self.print_add_to_history_count = 0

    def reset_navigation_and_position(self):
        """Resets navigation and position to the initial state."""
        self.navigation_directions = None
        if self.behavior.navigation_directions is not None:
            self.navigation_directions = self.behavior.navigation_directions.copy()
            print("Using navigation directions: %s" % self.navigation_directions)
        self.city_position = None
        if self.behavior.city_position is not None:
            self.city_position = self.behavior.city_position.copy()
            print("Starting at the initial city position: %s" % self.city_position)
            self.system.display_position(self.city_position.x, self.city_position.y)
        self.city_position_forward_accounted_for = False

    def update_sensors(self):
        """Updates sensor readings and counts."""
        self.state_cycle_since_transition += 1
        self.sensor_last = self.sensor
        li, ri, ll, lc, lr = self.system.get_sensors()
        self.sensor = li << 4 | ri << 3 | ll << 2 | lc << 1 | lr
        if self.sensor != self.sensor_last:
            if self.sensor_count > 0:
                # we eliminate fluke transitions (short ones) from the history
                if self.sensor_count >= self.behavior.fast_sensor_change_dropped_below_cycle_count:
                    # print(f"Last sensor into history: {self.sensor_last:05b} ({self.sensor_count}x) -> change to {self.sensor:05b}")
                    self.sensor_history.append((self.sensor_last, self.sensor_count))
                    if self.sensor_last == 0b111 or self.print_add_to_history_count > 0:
                        if self.sensor_last == 0b111:
                            self.print_add_to_history_count = 3
                        else:
                            self.print_add_to_history_count -= 1
                    if len(self.sensor_history) >= self.sensor_history_length:
                        self.sensor_history.pop(0)
                    self.switch_to_state_matching_ctx_situation()
                else:
                    print(f"Fluke transition eliminated: {self.sensor_last:05b} ({self.sensor_count}x)")
            self.system.display_sensors(li, ri, ll, lc, lr)
            self.sensor_count = 1
        else:
            self.sensor_count += 1

    def transition_to_state(self, state_key):
        """Transitions to state, a one-liner helper for main code."""
        if state_key != self.state_key:
            action_now = self.state.action if self.state is not None else None
            state_new = self.states[state_key]
            state_new.set_default_action(ctx=self)
            action_new = state_new.action
            if self.state is not None:
                self.state.on_exit(ctx=self)
                print("Transitioning: state %s (action %s) -> state %s (action %s)"
                      % (self.state, action_now, state_new, action_new))
            else:
                print("Transitioning to state %s (action %s)" % (state_new, action_new))
            self.system.display_drive_mode(action_new.symbol)
            self.state = state_new
            self.state_key = state_key
            self.state_cycle_since_transition = 0
            # reset the sensor history to start fresh within the state and not bring historical baggage
            print("Resetting sensor history")
            self.sensor_history = []
            self.state.on_enter(ctx=self)

    def switch_to_state_matching_ctx_situation(self):
        """Switches the state matching the sensor history + current sensor state (car behavior in the recent past)."""
        state_transitions = self.transitions.get(self.state_key)
        if state_transitions is None:
            print("ERROR: No state transitions for state %s" % self.state_key)
            return
        for state_key in state_transitions:
            state = self.states[state_key]
            if state == self.state or state.matchers is None:
                continue
            for matcher in state.matchers:
                if matcher.matches(self):
                    if 'TURN' in self.state_key and self.state_cycle_since_transition < self.behavior.turn_state_implicit_transition_protection_cycle_count:
                        print("Protecting from implicit state transition to TURN state, removing sensor history just to be sure")
                        self.sensor_history_with_current = [(self.sensor, self.sensor_count)]
                        self.sensor_history = []
                        return
                    if 'LINE' in self.state_key and self.state_cycle_since_transition < self.behavior.line_state_implicit_transition_protection_cycle_count:
                        print("Protecting from implicit state transition to LINE state, removing sensor history just to be sure")
                        self.sensor_history_with_current = [(self.sensor, self.sensor_count)]
                        self.sensor_history = []
                        return
                    print("Switching to state %s (%s) due to match of state matcher, sensor history %s"
                          % (state_key, state, Ctx.str_sensor_history(self.sensor_history_with_current)))
                    self.transition_to_state(state_key)
                    return
                # else:
                #     if self.sensor == 0b111 or self.is_intersection_in_history():
                #         print(
                #             f"Sensor {self.sensor:03b}, count {self.sensor_count}, history {self.str_sensor_history(self.sensor_history)} - no match by {matcher}")

    def add_sensor_to_history(self, sensor):
        if len(self.sensor_history) >= self.sensor_history_length:
            self.sensor_history.pop(0)
        self.sensor_history.append(sensor)

    def is_intersection_in_history(self):
        for sensor, count in self.sensor_history:
            if sensor == 0b111:
                return True
        return False

    def before_evaluation(self):
        """Called when the context changes are finished, before all evaluations."""
        # we need to update the sensor history with the current sensor and count
        self.sensor_history_with_current = self.sensor_history.copy()
        self.sensor_history_with_current.append((self.sensor, self.sensor_count))

    @staticmethod
    def str_sensor_history(sensor_history):
        """Converts the sensor history to a string."""
        return ", ".join([str(SensorHasCount(s, c)) for s, c in sensor_history])


class Action:
    def __init__(self, symbol: str):
        self.name = type(self).__name__.replace('Action', '')
        self.symbol = symbol

    def __str__(self):
        return self.name

    def matches(self, ctx: Ctx) -> bool:
        """Returns True if the action matches the context. Used for intra-state transitions."""
        return False

    def on_enter(self, ctx: Ctx):
        """Called when the action is entered. Can return new action or indicate state switch."""
        ctx.system.display_drive_mode(self.symbol)

    def on_update(self, ctx: Ctx):
        """Called when the action is updated. Can return new action or indicate state switch."""
        pass

    def on_exit(self, ctx: Ctx):
        """Called when the action is exited. Can return new action or indicate state switch."""
        pass


class SensorMatchingAction(Action):
    def __init__(self, symbol: str, matching_sensor: int):
        super().__init__(symbol=symbol)
        self.matching_sensor = matching_sensor

    def matches(self, ctx: Ctx) -> bool:
        return ctx.sensor == self.matching_sensor


class StateMatcher:
    def __init__(self):
        self.name = type(self).__name__.replace('StateMatcher', '')

    def __str__(self):
        return self.name

    def matches(self, ctx: Ctx) -> bool:
        """Returns True if the state matches the current context situation."""
        pass


class SensorHistoryStateMatcher(StateMatcher):
    def __init__(self, steps: list[SensorMatcher]):
        super().__init__()
        self.steps = steps

    def __str__(self):
        return f"{self.name}(steps=[{', '.join([str(step) for step in self.steps])}])"

    def matches(self, ctx: Ctx) -> bool:
        # we go through sensor history from the end to the beginning
        # (we are interested in the last steps, not the first ones)
        # we match the sensor history to all steps (in reverse), disregarding optional steps if missing
        for sensor_history_view in (ctx.sensor_history_with_current, ctx.sensor_history):
            if self.matches_sensor_history(sensor_history_view):
                return True
        return False

    def matches_sensor_history(self, sensor_history_view):
        for start_index in range(len(sensor_history_view) - 1, -1, -1):
            if self.match_from_index(sensor_history_view, start_index):
                return True
        return False

    def match_from_index(self, sensor_history_view, start_index):
        step_index = 0
        history_index = start_index

        while step_index < len(self.steps) and history_index >= 0:
            step: SensorMatcher = self.steps[step_index]
            sensor, count = sensor_history_view[history_index]
            if step.matches(sensor, count):
                step_index += 1
                history_index -= 1
            elif step.optional:
                step_index += 1
            else:
                break

        # Ensure all non-optional steps are matched
        while step_index < len(self.steps):
            if not self.steps[step_index].optional:
                return False
            step_index += 1

        return step_index == len(self.steps)


class State:
    def __init__(self, symbol: str, actions: list[Action], matchers: list[StateMatcher] = None):
        # Our name is the class name without the State suffix
        self.name = type(self).__name__.replace('State', '')
        self.symbol = symbol
        self.matchers = matchers
        self.actions = actions
        self.action = None

    def __str__(self):
        return self.name

    def str_full(self):
        matchers = ', '.join([str(matcher) for matcher in self.matchers]) if self.matchers else 'None'
        actions = ', '.join([str(action) for action in self.actions])
        return f"{self.name}(matchers=[{matchers}], actions=[{actions}])"

    def on_enter(self, ctx: Ctx):
        """Called when the state is entered."""
        print("Entering state %s" % self)
        ctx.system.display_drive_mode(self.symbol)
        if self.action is not None:
            self.action.on_enter(ctx)

    def on_update(self, ctx: Ctx):
        """Called when the state is updated."""
        if self.action is not None:
            self.action.on_update(ctx)

    def on_exit(self, ctx: Ctx):
        """Called when the state is exited."""
        if self.action is not None:
            self.action.on_exit(ctx)

    def set_default_action(self, ctx: Ctx):
        self.action = self.actions[0]
        ctx.system.display_drive_mode(self.action.symbol)
