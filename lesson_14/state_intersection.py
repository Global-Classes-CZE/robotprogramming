from state import Ctx, Action, State, SensorHistoryStateMatcher


class Choice:
    def __init__(self, symbol: str, target_state: str):
        self.symbol = symbol
        self.target_state = target_state


class InteractiveIntersectAction(Action):
    def __init__(self, symbol: str, choices: list[Choice]):
        super().__init__(symbol)
        self.choices = choices
        self.choice_idx = -1
        self.button_press_count = 0

    def on_enter(self, ctx: Ctx):
        ctx.wheels.stop()
        ctx.system.display_speed(0, ctx.behavior.fwd_speed, left=True)
        ctx.system.display_speed(0, ctx.behavior.fwd_speed, left=False)
        ctx.system.display_drive_mode(self.symbol)
        self.choice_idx = -1
        self.button_press_count = 0

    def on_update(self, ctx: Ctx):
        # we will be switching to the next choice after button press ends
        if ctx.system.is_button_b_pressed():
            self.button_press_count += 1
        elif self.button_press_count > 0:
            # we want at least half a second for long press
            min_cycle_count_for_long_press = 500_000 // ctx.behavior.cycle_duration_us
            if self.button_press_count >= min_cycle_count_for_long_press:
                ctx.system.display_choice(' ')
                ctx.transition_to_state(self.choices[self.choice_idx].target_state)
            else:
                self.choice_idx += 1
                if self.choice_idx >= len(self.choices):
                    self.choice_idx = 0
                ctx.system.display_choice(self.choices[self.choice_idx].symbol)
                self.button_press_count = 0


class InteractiveIntersectState(State):
    """User-interactive intersection state.
    The state stops the car, displays the intersection type and asks the user for the choice.
    User can cycle through the options (an arrow will be displayed in that direction),
    then confirms the choice with long-pressing 'B' button."""


class IntersectXState(State):
    def __init__(self, symbol: str, matchers: list[SensorHistoryStateMatcher]):
        actions = [InteractiveIntersectAction(symbol=symbol, choices=[
            Choice(symbol='<', target_state='TURN_L_OFF_LINE'),
            Choice(symbol='^', target_state='LINE'),
            Choice(symbol='>', target_state='TURN_R_OFF_LINE'),
        ])]
        super().__init__(symbol=symbol, actions=actions, matchers=matchers)


class IntersectYState(State):
    def __init__(self, symbol: str, matchers: list[SensorHistoryStateMatcher]):
        actions = [InteractiveIntersectAction(symbol=symbol, choices=[
            Choice(symbol='<', target_state='TURN_L_TO_LINE'),
            Choice(symbol='>', target_state='TURN_R_TO_LINE'),
        ])]
        super().__init__(symbol=symbol, actions=actions, matchers=matchers)


class IntersectLState(State):
    def __init__(self, symbol: str, matchers: list[SensorHistoryStateMatcher]):
        actions = [InteractiveIntersectAction(symbol=symbol, choices=[
            Choice(symbol='<', target_state='TURN_L_OFF_LINE'),
            Choice(symbol='^', target_state='LINE'),
        ])]
        super().__init__(symbol=symbol, actions=actions, matchers=matchers)


class IntersectRState(State):
    def __init__(self, symbol: str, matchers: list[SensorHistoryStateMatcher]):
        actions = [InteractiveIntersectAction(symbol=symbol, choices=[
            Choice(symbol='^', target_state='LINE'),
            Choice(symbol='>', target_state='TURN_R_OFF_LINE'),
        ])]
        super().__init__(symbol=symbol, actions=actions, matchers=matchers)


class IntersectTState(State):
    def __init__(self, symbol: str, matchers: list[SensorHistoryStateMatcher]):
        actions = [InteractiveIntersectAction(symbol=symbol, choices=[
            Choice(symbol='<', target_state='TURN_L'),
            Choice(symbol='>', target_state='TURN_R'),
        ])]
        super().__init__(symbol=symbol, actions=actions, matchers=matchers)
