from system import System
from wheel_driver import WheelDriver


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
                 cycle_duration_us: int
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


class SensorHasCount:
    """A sensor and how many times it needs to match."""

    def __init__(self, sensor, min_count, max_count=None, optional=False):
        self.sensor = sensor
        self.min_count = min_count
        self.max_count = max_count
        self.optional = optional

    def matches(self, sensor, count):
        if sensor != self.sensor:
            return False
        if self.max_count is not None:
            return self.min_count <= count <= self.max_count
        return count >= self.min_count

    # let's print binary representation of the sensor and how many times it needs to match
    def __str__(self):
        return f"{self.sensor:0{5}b} ({self.min_count}x)"


class Ctx:
    """Carries the current operating context of the robot."""

    def __init__(self, system: System, wheels: WheelDriver, behavior: Behavior,
                 states: dict[str, 'State'], transitions: dict[str, list[str]], state_key: str):
        self.system = system
        self.wheels = wheels
        self.behavior = behavior
        self.states = states
        self.transitions = transitions
        self.state_key = state_key
        self.state = states[state_key]
        self.sensor = None
        self.sensor_count = 0
        self.sensor_last = None
        self.state_action_cycle = 0
        self.state_out_of_bounds_cycle = 0
        # history of sensor changes: [(lcr, count), ...]
        # we keep track of the last several sensor changes and use that to determine situation underneath us
        # this feeds to a sudden main state change if we detect different behavior than expected
        # each state has the ability to override other states if it thinks it should rule the car
        self.sensor_history = []
        # the history with extra element pertaining the current sensor and cycle count (updated just before state eval)
        self.sensor_history_with_current = []
        # Our history needs to be able to house at least 4 transitions
        # (going to intersection might be preceded by a single sensor if the car is going sideways)
        self.sensor_history_length = 5
        # carries max speed for each wheel (for display purposes)
        # will be updated on forward to correct values
        self.fwd_speed_pwm_left_max = 255
        self.fwd_speed_pwm_right_max = 255
        # initialize the state
        self.state.on_enter(self)
        self.state.set_default_action(self)

    def update_sensors(self):
        """Updates sensor readings and counts."""
        self.sensor_last = self.sensor
        li, ri, ll, lc, lr = self.system.get_sensors()
        self.sensor = li << 4 | ri << 3 | ll << 2 | lc << 1 | lr
        if self.sensor != self.sensor_last:
            if self.sensor_count > 0:
                # we eliminate fluke transitions (short ones) from the history
                if self.sensor_count >= self.behavior.fast_sensor_change_dropped_below_cycle_count:
                    # print(f"Last sensor into history: {self.sensor_last:05b} ({self.sensor_count}x) -> change to {self.sensor:05b}")
                    self.sensor_history.append((self.sensor_last, self.sensor_count))
                    if len(self.sensor_history) >= self.sensor_history_length:
                        self.sensor_history.pop(0)
                else:
                    print(f"Fluke transition eliminated: {self.sensor_last:05b} ({self.sensor_count}x)")
            self.system.display_sensors(li, ri, ll, lc, lr)
            self.sensor_count = 1
        else:
            self.sensor_count += 1

    def transition_to_state(self, state_key):
        """Transitions to state, a one-liner helper for main code."""
        if state_key != self.state_key:
            action_now = self.state.action
            state_new = self.states[state_key]
            state_new.set_default_action(ctx=self)
            action_new = state_new.action
            self.state.on_exit(ctx=self)
            print("Transitioning: state %s (action %s) -> state %s (action %s)"
                  % (self.state, action_now, state_new, action_new))
            self.system.display_drive_mode(action_new.symbol)
            self.state = state_new
            self.state_key = state_key
            # reset the sensor history to start fresh within the state and not bring historical baggage
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
                    print("Switching to state %s (%s) due to match of state matcher, sensor history %s"
                          % (state_key, state, Ctx._str_history(self.sensor_history_with_current)))
                    self.transition_to_state(state_key)
                    return

    def add_sensor_to_history(self, sensor):
        if len(self.sensor_history) >= self.sensor_history_length:
            self.sensor_history.pop(0)
        self.sensor_history.append(sensor)

    def before_evaluation(self):
        """Called when the context changes are finished, before all evaluations."""
        # we need to update the sensor history with the current sensor and count
        self.sensor_history_with_current = self.sensor_history.copy()
        self.sensor_history_with_current.append((self.sensor, self.sensor_count))

    @staticmethod
    def _str_history(sensor_history):
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
    def __init__(self, steps: list[SensorHasCount]):
        super().__init__()
        self.steps = steps

    def __str__(self):
        return f"{self.name}(steps=[{', '.join([str(step) for step in self.steps])}])"

    def matches(self, ctx: Ctx):
        # we go through sensor history from the end to the beginning
        # (we are interested in the last steps, not the first ones)
        # we match the sensor history to all steps (in reverse), disregarding optional steps if missing
        sensor_history_view = ctx.sensor_history_with_current
        step_index = 0
        history_index = len(sensor_history_view) - 1

        while step_index < len(self.steps) and history_index >= 0:
            step = self.steps[step_index]
            sensor, count = sensor_history_view[history_index]
            if step.matches(sensor, count):
                step_index += 1
                history_index -= 1
            elif step.optional:
                step_index += 1
            else:
                return False

        # Ensure all non-optional steps are matched
        while step_index < len(self.steps):
            if not self.steps[step_index].optional:
                return False
            step_index += 1

        return True

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
        self.action.on_enter(ctx)


class NoOpState(State):
    def __init__(self, symbol: str, matchers: list[StateMatcher] = None):
        super().__init__(symbol=symbol, actions=[], matchers=matchers)

    def on_enter(self, ctx: Ctx):
        print("NoOpState entered - stopping the robot")
        ctx.wheels.stop()
        super().on_enter(ctx=ctx)
