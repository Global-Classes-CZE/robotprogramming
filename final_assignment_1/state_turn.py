from state import Action, Ctx, SensorMatchingAction, State, SensorHistoryStateMatcher


class CityNavigationTurnAction(Action):
    # the symbol indicates the direction we are going to take (navigation must match it or we enter ERROR state)
    def __init__(self, symbol: str):
        super().__init__(symbol)

    def on_enter(self, ctx: Ctx):
        ctx.wheels.stop()
        ctx.system.display_speed(0, ctx.fwd_speed_pwm_left_max, left=True)
        ctx.system.display_speed(0, ctx.fwd_speed_pwm_right_max, left=False)
        ctx.state_action_cycle = 0
        if ctx.city_position is not None and ctx.city_position_forward_accounted_for is False:
            # we first move to this intersection and then we will decide where to go (turn)
            ctx.city_position.move_forward()
            ctx.system.display_position(ctx.city_position.x, ctx.city_position.y)
            ctx.city_position_forward_accounted_for = True

    def on_update(self, ctx: Ctx):
        ctx.state_action_cycle += 1
        if ctx.navigation_directions is not None:
            cycle_count_for_navigation_pause = ctx.behavior.navigation_intersection_pause // ctx.behavior.cycle_duration_us
            if ctx.state_action_cycle < cycle_count_for_navigation_pause:
                ctx.state_action_cycle += 1
                return False
            else:
                ctx.state_action_cycle = 0
                navigation_direction = ctx.navigation_directions.pop(0)
                turn_type = self.navigation_direction_to_turn_type(navigation_direction)
                print("Navigating to %s (turn type %s), valid choice is %s" % (navigation_direction, turn_type, self.symbol))
                if turn_type == self.symbol:
                    if ctx.city_position is not None:
                        ctx.city_position.move_by_choice(navigation_direction)
                        ctx.system.display_position(ctx.city_position.x, ctx.city_position.y)
                        return True
                else:
                    # we are in the navigation mode, but the symbol is not recognized for the current situation
                    ctx.transition_to_state('ERROR')
                    return False
        else:
            # in non-interactive mode we just turn based on our only choice
            if ctx.city_position is not None:
                ctx.city_position.move_by_choice(self.get_position_symbol())
                ctx.system.display_position(ctx.city_position.x, ctx.city_position.y)
            return True

    def navigation_direction_to_turn_type(self, direction: str):
        if direction == '^':
            return '^'
        elif direction == '<':
            return 'TL'
        elif direction == '>':
            return 'TR'

    def get_position_symbol(self):
        if self.symbol == '^':
            return '^'
        elif self.symbol == 'TL':
            return '<'
        elif self.symbol == 'TR':
            return '>'


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
        self.action_idx = 0  # current action index

    def set_default_action(self, ctx: Ctx):
        if ctx.behavior.navigation_directions is not None:
            # we are in the navigation mode, we will turn based on the navigation directions
            # but our only choice is driven by our first normal turn action's direction
            self.action = CityNavigationTurnAction(symbol=self.symbol)
            self.action_idx = -1  # we are not part of standard actions and need to make sure we move the index
        else:
            self.action_idx = 0
            self.action = self.actions[self.action_idx]

    def on_update(self, ctx: Ctx):
        """Updates the current state: we just go through both actions we have and wait until we match the sensors."""
        if self.action_idx == -1:
            # we are in the navigation mode, we will turn based on the navigation directions
            if self.action.on_update(ctx):
                self.action_idx += 1
                self.action = self.actions[self.action_idx]
                self.action.on_enter(ctx)
            else:
                return

        # standard turn actions
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
