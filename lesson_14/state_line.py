from state import Ctx, SensorMatchingAction, State


class LineAction(SensorMatchingAction):
    def __init__(self, symbol: str, matching_sensor: int):
        super().__init__(symbol=symbol, matching_sensor=matching_sensor)


class FwdLineAction(LineAction):
    """Moves the robot forward."""

    def __init__(self, symbol: str, matching_sensor: int):
        super().__init__(symbol=symbol, matching_sensor=matching_sensor)

    def on_enter(self, ctx: Ctx):
        super().on_enter(ctx)
        ctx.wheels.move(speed_rad=ctx.behavior.fwd_speed, rotation_rad=0)
        ctx.fwd_speed_pwm_left = ctx.wheels.left.speed_pwm
        ctx.fwd_speed_pwm_right = ctx.wheels.right.speed_pwm
        ctx.system.display_speed(ctx.behavior.fwd_speed, ctx.behavior.fwd_speed, left=True)
        ctx.system.display_speed(ctx.behavior.fwd_speed, ctx.behavior.fwd_speed, left=False)
        ctx.state_action_cycle = 0

    def on_update(self, ctx: Ctx):
        """When going just forward, we don't do any recalculations."""
        ctx.state_action_cycle += 1


class SideFwdLineAction(LineAction):
    """Moves the robot forward with slight turn to the side on which we captured the non-center sensor."""

    def __init__(self, symbol: str, matching_sensor: int, direction: int):
        super().__init__(symbol=symbol, matching_sensor=matching_sensor)
        self.direction = direction

    def on_enter(self, ctx: Ctx):
        super().on_enter(ctx)
        ctx.wheels.move(speed_rad=ctx.behavior.fwd_speed, rotation_rad=-ctx.behavior.side_arc_max)
        ctx.fwd_speed_pwm_left = ctx.wheels.left.speed_pwm
        ctx.fwd_speed_pwm_right = ctx.wheels.right.speed_pwm
        ctx.system.display_speed(ctx.wheels.left.speed_pwm, ctx.behavior.fwd_speed, left=True)
        ctx.system.display_speed(ctx.wheels.left.speed_pwm, ctx.behavior.fwd_speed, left=False)
        ctx.state_action_cycle = 0

    def on_update(self, ctx: Ctx):
        """When side-stepping line while going forward, we are slowing down progressively while increasing arc speed."""
        ctx.state_action_cycle += 1
        rotation_rad = ctx.behavior.side_arc_min + ctx.behavior.side_arc_inc * ctx.state_action_cycle
        rotation_rad = min(rotation_rad, ctx.behavior.side_arc_max)
        align_speed = ctx.behavior.fwd_speed - ctx.state_action_cycle * ctx.behavior.side_speed_dec
        align_speed = max(align_speed, ctx.behavior.side_speed_min)
        ctx.wheels.move(speed_rad=align_speed, rotation_rad=rotation_rad * self.direction)
        ctx.system.display_speed(ctx.wheels.left.speed_pwm, ctx.fwd_speed_pwm_left_max, left=True)
        ctx.system.display_speed(ctx.wheels.right.speed_pwm, ctx.fwd_speed_pwm_right_max, left=False)
        print(
            "%s, rotation_rad %d, init %s + inc_per_cycle %s * cycle %s" %
            (self, rotation_rad, ctx.behavior.side_arc_min, ctx.behavior.side_arc_inc, ctx.state_action_cycle))


class LeftFwdLineAction(SideFwdLineAction):
    """Moves the robot forward with slight turn to the left when left sensor is captured."""

    def __init__(self, symbol: str, matching_sensor: int):
        super().__init__(symbol=symbol, matching_sensor=matching_sensor, direction=1)


class RightFwdLineAction(SideFwdLineAction):
    """Moves the robot forward with slight turn to the right when right sensor is captured."""

    def __init__(self, symbol: str, matching_sensor: int):
        super().__init__(symbol=symbol, matching_sensor=matching_sensor, direction=-1)


class LineState(State):
    def __init__(self, symbol: str, matchers=None):
        actions: list[LineAction] = [
            FwdLineAction(symbol='|', matching_sensor=0b010),
            LeftFwdLineAction(symbol='\\', matching_sensor=0b100),
            RightFwdLineAction(symbol='/', matching_sensor=0b001)
        ]
        super().__init__(symbol=symbol, actions=actions, matchers=matchers)
        self.actions = actions # type-cast for IDE support

    def transition_action(self, ctx: Ctx):
        """Transitions from action to action within the state based on the line sensor readings."""
        # print("Trans state %s action %s, %s" % (state, action_now, bin(lcr)))
        for action in self.actions:
            if action.matching_sensor == ctx.sensor:
                print("Transitioning state %s action %s to %s" % (self, self.action, action))
                self.action.on_exit(ctx)
                self.action = action
                action.on_enter(ctx)
                return True
        return False

    def on_update(self, ctx: Ctx):
        """Updates the current state."""
        if ctx.sensor != self.action.matching_sensor:
            # print(f"Transitioning Line: sensor={ctx.sensor:05b} no longer matches while_sensor={self.action.matching_sensor:05b} (current state {self} action {self.action})")
            ctx.state_out_of_bounds_cycle += 1
            if self.transition_action(ctx):
                ctx.state_out_of_bounds_cycle = 0
            else:
                if ctx.state_out_of_bounds_cycle > ctx.behavior.line_cycle_tolerance:
                    print("Line cycle tolerance exceeded, switching to error state")
                    ctx.transition_to_state("STOP")
                    return
        else:
            if ctx.state_out_of_bounds_cycle > 0:
                ctx.state_out_of_bounds_cycle = 0
                print("Back in state")
        self.action.on_update(ctx)
