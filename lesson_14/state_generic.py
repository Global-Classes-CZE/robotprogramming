from state import Ctx, Action, State


class GenericAction(Action):
    def __init__(self, symbol):
        super().__init__(symbol)


class StartAction(GenericAction):
    """Starts the robot. An action used by start state to wait for a button to be pressed to start moving.
    The action also stops the robot to allow comfortable pressing of the button."""

    def __init__(self):
        super().__init__(symbol='s')

    def on_enter(self, ctx: Ctx):
        ctx.system.display_on()
        ctx.wheels.stop()
        ctx.system.display_speed(0, ctx.fwd_speed_pwm_left_max, left=True)
        ctx.system.display_speed(0, ctx.fwd_speed_pwm_right_max, left=False)

    def on_update(self, ctx: Ctx):
        if ctx.system.is_button_b_pressed():
            print("B pressed, starting")
            ctx.transition_to_state("LINE")


class StopAction(GenericAction):
    """Stops the robot. No further action will be taken."""

    def __init__(self):
        super().__init__(symbol='.')

    def on_enter(self, ctx: Ctx):
        ctx.wheels.stop()

    def on_update(self, ctx: Ctx):
        if ctx.system.is_button_b_pressed():
            ctx.transition_to_state("START")


class StartState(State):
    def __init__(self, symbol: str, matchers=None):
        super().__init__(symbol=symbol, actions=[StartAction()], matchers=matchers)


class StopState(State):
    def __init__(self, symbol: str, matchers=None):
        super().__init__(symbol=symbol, actions=[StopAction()], matchers=matchers)


class ErrorState(State):
    def __init__(self, symbol: str, matchers=None):
        super().__init__(symbol=symbol, actions=[StopAction()], matchers=matchers)
