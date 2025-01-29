from state import Behavior, Ctx, Position
from state_map import StateMap
from system import System
from wheel_driver import WheelDriver

if __name__ == "__main__":
    # Navigates through a city of streets based on provided instruction for each intersection (or corner)
    system = System()
    wheels = WheelDriver(
        system=system,
        left_pwm_min=60, left_pwm_multiplier=0.09, left_pwm_shift=-2.5,
        right_pwm_min=60, right_pwm_multiplier=0.09, right_pwm_shift=-2.2
    )

    # see Behavior class for the robot behavior definition and parameter characteristics
    behavior = Behavior(
        fwd_speed=0.2,
        side_speed_dec=0.1, side_speed_min=0.1,
        side_arc_min=0.2, side_arc_inc=0.3, side_arc_max=2,
        # 25ms per cycle x 75 = 1.875s outside the valid line action rules (i.e., searching for line)
        line_cycle_tolerance=50,
        turn_speed=0.5, turn_arc_speed=10,
        # 25ms per cycle x 100 = 2.5s outside the valid turn action rules (i.e., searching for 90° turned line)
        turn_cycle_tolerance=80,
        fast_sensor_change_dropped_below_cycle_count=3,
        cycle_duration_us=25_000,
        # the city navigator behavior has additional parameters
        # Position indicates our last intersection (we are past it and heading to the next one)
        # where EAST signifies X axis increase and NORTH signifies Y axis increase
        city_position=Position(x=1, y=0, orientation=Position.NORTH),  # next intersection will be at (1, 1)
        navigation_directions=[
            # the city is a simple grid of streets with intersections at every corner
            # we navigate with : '^' (forward), '>' (right), '<' (left), S (stop)
            # We assume 5x5 grid (can be larger, but corners are mentioned for 5x5 size)
            '^', '<', '>', '^', '>',  # we should be turning at the Northwest corner (0, 4)
            # >....
            # ^....
            # ^<...
            # .^...
            # .....
            '>', '<', '^', '^', '>',  # we should be turning one line below the Northeast corner (4, 3)
            # .v...
            # .>>>v
            # .....
            # .....
            # .....
            '^', '^', '>',  # we should be turning at the SouthEast corner (4, 0)
            # .....
            # .....
            # ....v
            # ....v
            # ....<
            '^', '>', '<', '^',  # we should be heading to the initial South-east square, heading towards (0, 1)
            # .....
            # .....
            # .....
            # .<<..
            # ..^<.
            '<', '<', '<', 'S'  # we should be circling the initial South-east square, stopping where we started (1, 0)
            # .....
            # .....
            # .....
            # v....
            # >^...
        ],
        line_state_implicit_transition_protection_after_switch_cycle_count=200,
        turn_state_implicit_transition_protection_after_switch_cycle_count=500
    )
    state_map = StateMap(behavior=behavior, stop_on_non_line_sensors=False, turns=True, intersections=True)
    ctx = Ctx(system=system, wheels=wheels, behavior=behavior,
              states=state_map.states, transitions=state_map.transitions, state_key='START')

    try:
        state_cycle_start = system.ticks_us()
        while not system.is_button_a_pressed():
            wheels.update()
            # reads the sensors and builds their history
            ctx.update_sensors()

            time_now = system.ticks_us()
            if system.ticks_diff(time_now, state_cycle_start) > ctx.behavior.cycle_duration_us:
                state_cycle_start = time_now

                # finalize context before evaluation
                # (costly operations are done here like sensor history extension with current sensor)
                ctx.before_evaluation()

                # if our context situation matches one of the states, we switch to that state
                # (this is typically based on sensor history match, but other matchers are possible)
                ctx.switch_to_state_matching_ctx_situation()

                # while being in the state we update it
                ctx.state.on_update(ctx)

    finally:
        try:
            ctx.state.on_exit(ctx)
        finally:
            wheels.stop()
            system.display_off()
            print("Finished")
