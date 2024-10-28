from state import Ctx, SensorMatchingAction, State, SensorHistoryStateMatcher


class TurnAction(SensorMatchingAction):
    def __init__(self, symbol: str, matching_sensor: int, direction: int):
        super().__init__(symbol=symbol, matching_sensor=matching_sensor)
        self.direction = direction

    def on_enter(self, ctx: Ctx):
        super().on_enter(ctx)
        ctx.wheels.move(speed_rad=ctx.behavior.turn_speed, rotation_rad=ctx.behavior.turn_arc_speed * self.direction)
        ctx.system.display_speed(ctx.wheels.left.speed_pwm, ctx.fwd_speed_pwm_left_max, left=True)
        ctx.system.display_speed(ctx.wheels.right.speed_pwm, ctx.fwd_speed_pwm_right_max, left=False)
        ctx.state_action_cycle = 0

    def on_update(self, ctx: Ctx):
        ctx.state_action_cycle += 1


class SideSeekTurnAction(TurnAction):
    def __init__(self, symbol: str, matching_sensor: int, direction: int):
        super().__init__(symbol=symbol, matching_sensor=matching_sensor, direction=direction)

    def on_enter(self, ctx: Ctx):
        print("Turning to catch side line..")
        super().on_enter(ctx)
        ctx.wheels.move(speed_rad=ctx.behavior.turn_speed, rotation_rad=ctx.behavior.turn_arc_speed * self.direction)
        ctx.system.display_speed(ctx.wheels.left.speed_pwm, ctx.fwd_speed_pwm_left_max, left=True)
        ctx.system.display_speed(ctx.wheels.right.speed_pwm, ctx.fwd_speed_pwm_right_max, left=False)
        ctx.state_action_cycle = 0


class CenterSeekTurnAction(TurnAction):
    def __init__(self, symbol: str, matching_sensor: int, direction: int):
        super().__init__(symbol=symbol, matching_sensor=matching_sensor, direction=direction)

    def on_enter(self, ctx: Ctx):
        print("Turning to catch center line..")
        super().on_enter(ctx)
        ctx.transition_to_state('LINE')


class NoCenterSeekTurnAction(TurnAction):
    def __init__(self, symbol: str, matching_sensor: int, direction: int):
        super().__init__(symbol=symbol, matching_sensor=matching_sensor, direction=direction)

    def on_enter(self, ctx: Ctx):
        print("Turning off center line..")
        super().on_enter(ctx)
        ctx.wheels.move(speed_rad=ctx.behavior.turn_speed, rotation_rad=ctx.behavior.turn_arc_speed * self.direction)
        ctx.system.display_speed(ctx.wheels.left.speed_pwm, ctx.fwd_speed_pwm_left_max, left=True)
        ctx.system.display_speed(ctx.wheels.right.speed_pwm, ctx.fwd_speed_pwm_right_max, left=False)
        ctx.state_action_cycle = 0


class TurnState(State):
    def __init__(self, symbol: str, actions: list[TurnAction], matchers: list[SensorHistoryStateMatcher]):
        super().__init__(symbol=symbol, actions=actions, matchers=matchers)
        self.actions = actions  # type-cast for IDE support

    def set_default_action(self, ctx: Ctx):
        self.action = self.actions[0]
        self.action.on_enter(ctx)

    def on_update(self, ctx: Ctx):
        """Updates the current state: we just go through both actions we have and wait until we match the sensors."""
        if ctx.sensor != self.action.matching_sensor:
            print(
                f"Turning and seeking sensor {self.action.matching_sensor:05b}, current sensor={ctx.sensor:05b} (current state {self} action {self.action})")
            ctx.state_out_of_bounds_cycle += 1
            if ctx.state_out_of_bounds_cycle > ctx.behavior.turn_cycle_tolerance:
                print("Turn cycle tolerance exceeded, switching to error state")
                ctx.transition_to_state('STOP')
                return
        else:
            ctx.state_out_of_bounds_cycle = 0
            if self.action == self.actions[0]:
                print("Transitioning state %s action %s to %s" % (self, self.action, self.actions[1]))
                self.action.on_exit(ctx)
                self.action = self.actions[1]
                self.action.on_enter(ctx)
            else:
                print("Finished turning")
                ctx.transition_to_state('LINE')
        self.action.on_update(ctx)


class LeftTurnState(TurnState):
    """Turns the car to the left from an empty space, first catching the left side sensor, then the center one."""
    def __init__(self, symbol: str, matchers: list[SensorHistoryStateMatcher]):
        actions = [
            SideSeekTurnAction(symbol=symbol, matching_sensor=0b100, direction=1),
            CenterSeekTurnAction(symbol=symbol, matching_sensor=0b010, direction=1)
        ]
        super().__init__(symbol=symbol, actions=actions, matchers=matchers)


class RightTurnState(TurnState):
    """Turns the car to the right from an empty space, first catching the right side sensor, then the center one."""
    def __init__(self, symbol: str, matchers: list[SensorHistoryStateMatcher]):
        actions = [
            SideSeekTurnAction(symbol=symbol, matching_sensor=0b001, direction=-1),
            CenterSeekTurnAction(symbol=symbol, matching_sensor=0b010, direction=-1)
        ]
        super().__init__(symbol=symbol, actions=actions, matchers=matchers)


class OffLineLeftTurnState(TurnState):
    """Turns the car to the left from a center line, first waiting for an empty space on all sensors, then left side sensor, then the center one."""
    def __init__(self, symbol: str):
        actions = [
            NoCenterSeekTurnAction(symbol=symbol, matching_sensor=0b000, direction=1),
            SideSeekTurnAction(symbol=symbol, matching_sensor=0b100, direction=1),
            CenterSeekTurnAction(symbol=symbol, matching_sensor=0b010, direction=1)
        ]
        super().__init__(symbol=symbol, actions=actions, matchers=[])


class OffLineRightTurnState(TurnState):
    """Turns the car to the right from a center line, first waiting for an empty space on all sensors, then right side sensor, then the center one."""
    def __init__(self, symbol: str):
        actions = [
            NoCenterSeekTurnAction(symbol=symbol, matching_sensor=0b000, direction=-1),
            SideSeekTurnAction(symbol=symbol, matching_sensor=0b001, direction=-1),
            CenterSeekTurnAction(symbol=symbol, matching_sensor=0b010, direction=-1)
        ]
        super().__init__(symbol=symbol, actions=actions, matchers=[])

class ToLineLeftTurnState(TurnState):
    """Turns the car to the left just waiting for the center sensor to catch the line (disregarding side sensor)."""
    def __init__(self, symbol: str):
        actions = [
            CenterSeekTurnAction(symbol=symbol, matching_sensor=0b010, direction=1)
        ]
        super().__init__(symbol=symbol, actions=actions, matchers=[])


class ToLineRightTurnState(TurnState):
    """Turns the car to the right just waiting for the center sensor to catch the line (disregarding side sensor)."""
    def __init__(self, symbol: str):
        actions = [
            CenterSeekTurnAction(symbol=symbol, matching_sensor=0b010, direction=-1)
        ]
        super().__init__(symbol=symbol, actions=actions, matchers=[])
