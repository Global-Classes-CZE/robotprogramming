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
        self.navigation_pause_count = 0
        self.button_press_count = 0

    def get_choice_by_symbol(self, symbol: str):
        # Returns the choice object by looking at the symbol of all choices we have
        for choice in self.choices:
            if choice.symbol == symbol:
                return choice
        return None

    def on_enter(self, ctx: Ctx):
        print("Intersection.on_enter()")
        ctx.wheels.stop()
        ctx.system.display_speed(0, ctx.behavior.fwd_speed, left=True)
        ctx.system.display_speed(0, ctx.behavior.fwd_speed, left=False)
        ctx.system.display_drive_mode(self.symbol)
        self.choice_idx = -1
        self.navigation_pause_count = 0
        self.button_press_count = 0
        if ctx.city_position is not None and ctx.city_position_forward_accounted_for is False:
            # we first move to this intersection and then we will decide where to go (turn)
            ctx.city_position.move_forward()
            ctx.system.display_position(ctx.city_position.x, ctx.city_position.y)
            ctx.city_position_forward_accounted_for = True

    def on_update(self, ctx: Ctx):
        """Chooses the next state based on the user input or the supplied navigation directions.
        When the navigation is active, next command will be taken from the navigation directions.
        When the interactive mode is active, user can cycle through the choices and confirm the choice with long press."""
        if ctx.navigation_directions is not None:
            cycle_count_for_navigation_pause = ctx.behavior.navigation_intersection_pause // ctx.behavior.cycle_duration_us
            if self.navigation_pause_count < cycle_count_for_navigation_pause:
                self.navigation_pause_count += 1
                return
            else:
                self.navigation_pause_count = 0
                choice_symbol = ctx.navigation_directions[0]
                print("Navigating to %s, valid choices are %s" % (choice_symbol, [c.symbol for c in self.choices]))
                choice = self.get_choice_by_symbol(symbol=choice_symbol)
                if choice is not None:
                    # if we are not just going forward, we need to keep direction in the navigation for the next state
                    if choice.target_state == 'LINE':
                        ctx.navigation_directions.pop(0)
                    ctx.transition_to_state(choice.target_state)
                else:
                    # we are in the navigation mode, but the symbol is not recognized for the current situation
                    ctx.transition_to_state('ERROR')
                return

        # we will be switching to the next choice after button press ends
        if ctx.system.is_button_b_pressed():
            self.button_press_count += 1
        elif self.button_press_count > 0:
            # we want at least half a second for long press
            min_cycle_count_for_long_press = 500_000 // ctx.behavior.cycle_duration_us
            if self.button_press_count >= min_cycle_count_for_long_press:
                ctx.system.display_choice(' ')
                choice = self.choices[self.choice_idx]
                ctx.transition_to_state(choice.target_state)
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
