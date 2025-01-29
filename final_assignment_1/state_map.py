from state import Behavior, SensorHistoryStateMatcher, SensorHasCount, EitherSensorHasCount
from state_generic import StartState, StopState, ErrorState
from state_intersection import IntersectXState, IntersectYState, IntersectTState, IntersectLState, IntersectRState
from state_line import LineState
from state_turn import LeftTurnState, RightTurnState, OffLineLeftTurnState, OffLineRightTurnState
from state_turn import ToLineLeftTurnState, ToLineRightTurnState


class StateMap:
    """States of the robot.
    Each state is defined declaratively, indicating:
     - sensor history matchers for entering the state
     - supported transitions to other states
    """

    def __init__(self, behavior: Behavior, stop_on_non_line_sensors=False, turns=False, intersections=False):
        # if we want basic scenario, we will transition to stop on any non-line sensor change
        stop_matchers = None if not stop_on_non_line_sensors else [
            SensorHistoryStateMatcher(steps=[SensorHasCount(sensor=0b111, min_count=5)]),
            SensorHistoryStateMatcher(steps=[SensorHasCount(sensor=0b011, min_count=5)]),
            SensorHistoryStateMatcher(steps=[SensorHasCount(sensor=0b110, min_count=5)]),
        ]
        self.states = {
            # Generic states
            'START': StartState(symbol='s', matchers=[
                # move to start when line is detected after border states (i.e., after stop)
                SensorHistoryStateMatcher(steps=[SensorHasCount(sensor=0b010, min_count=10)]),
            ]),
            'STOP': StopState(symbol='.', matchers=stop_matchers),
            'ERROR': ErrorState(symbol='x'),

            # Follows the line (no declarative matchers enabled, we transition in and out using advanced conditions)
            'LINE': LineState(symbol='|'),
        }
        line_transitions = ['STOP']
        self.transitions = {
            'START': ['LINE', 'STOP'],
            'LINE': line_transitions,
            'STOP': ['START'],
            'ERROR': ['STOP'],
        }

        vertical_min_count = 5
        horizontal_min_count = behavior.fast_sensor_change_dropped_below_cycle_count + 1
        if turns:
            self.states.update({
                # detects a turn to the left
                'TURN_L': LeftTurnState(
                    symbol='TL', matchers=[
                        # we are detecting disappearing line while last match shows it turning to the left
                        SensorHistoryStateMatcher(steps=[
                            SensorHasCount(sensor=0b000, min_count=vertical_min_count),
                            SensorHasCount(sensor=0b100, min_count=vertical_min_count, optional=True),
                            SensorHasCount(sensor=0b110, min_count=horizontal_min_count),
                            EitherSensorHasCount(sensors=[
                                SensorHasCount(sensor=0b001, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b010, min_count=vertical_min_count)
                            ])
                        ])
                    ]
                ),
                # detects a turn to the right
                'TURN_R': RightTurnState(
                    symbol='TR', matchers=[
                        # we are detecting disappearing line while last match shows it turning to the right
                        SensorHistoryStateMatcher(steps=[
                            SensorHasCount(sensor=0b000, min_count=vertical_min_count),
                            SensorHasCount(sensor=0b001, min_count=vertical_min_count, optional=True),
                            SensorHasCount(sensor=0b011, min_count=horizontal_min_count),
                            EitherSensorHasCount(sensors=[
                                SensorHasCount(sensor=0b001, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b010, min_count=vertical_min_count)
                            ])
                        ])
                    ]
                ),
            })
            line_transitions.extend(['TURN_L', 'TURN_R'])
            self.transitions.update({
                'TURN_L': ['STOP'],
                'TURN_R': ['STOP'],
            })

        if intersections:
            self.states.update({
                # detects a full intersection (+)
                'INTERSECT_X': IntersectXState(
                    symbol='I+', matchers=[
                        # we will be detecting normal line, then a full intersection, then normal line again
                        # we also need to account for the fact that we might be slightly off the line
                        SensorHistoryStateMatcher(steps=[
                            EitherSensorHasCount(sensors=[
                                SensorHasCount(sensor=0b010, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b100, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b001, min_count=vertical_min_count),
                            ]),
                            SensorHasCount(sensor=0b110, min_count=horizontal_min_count, optional=True),
                            SensorHasCount(sensor=0b011, min_count=horizontal_min_count, optional=True),
                            SensorHasCount(sensor=0b111, min_count=horizontal_min_count),
                            SensorHasCount(sensor=0b110, min_count=horizontal_min_count, optional=True),
                            SensorHasCount(sensor=0b011, min_count=horizontal_min_count, optional=True),
                            EitherSensorHasCount(sensors=[
                                SensorHasCount(sensor=0b010, min_count=vertical_min_count),
                                # SensorHasCount(sensor=0b100, min_count=vertical_min_count),
                                # SensorHasCount(sensor=0b001, min_count=vertical_min_count),
                            ]),
                        ])
                    ]
                ),
                # detects an intersection slight to the left and right, not forward (i.e., 'Y')
                'INTERSECT_Y': IntersectYState(
                    symbol='IY', matchers=[
                        SensorHistoryStateMatcher(steps=[
                            SensorHasCount(sensor=0b101, min_count=vertical_min_count),
                            SensorHasCount(sensor=0b110, min_count=horizontal_min_count, optional=True),
                            SensorHasCount(sensor=0b011, min_count=horizontal_min_count, optional=True),
                            SensorHasCount(sensor=0b010, min_count=horizontal_min_count),
                        ])
                    ]
                ),
                # detects an intersection to the left and right, not forward (i.e., 'T')
                'INTERSECT_T': IntersectTState(
                    symbol='IT', matchers=[
                        SensorHistoryStateMatcher(steps=[
                            SensorHasCount(sensor=0b000, min_count=vertical_min_count),
                            EitherSensorHasCount(sensors=[
                                SensorHasCount(sensor=0b010, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b100, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b001, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b110, min_count=horizontal_min_count),
                                SensorHasCount(sensor=0b011, min_count=horizontal_min_count),
                            ], optional=True),
                            SensorHasCount(sensor=0b111, min_count=horizontal_min_count),
                            SensorHasCount(sensor=0b110, min_count=horizontal_min_count, optional=True),
                            SensorHasCount(sensor=0b011, min_count=horizontal_min_count, optional=True),
                            EitherSensorHasCount(sensors=[
                                SensorHasCount(sensor=0b010, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b100, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b001, min_count=vertical_min_count),
                            ]),
                        ])
                    ]
                ),
                # detects an intersection to the left
                'INTERSECT_L': IntersectLState(
                    symbol='IL', matchers=[
                        # we are detecting a blip on the right sensor, it has to last for some time (speed-dependent)
                        SensorHistoryStateMatcher(steps=[
                            EitherSensorHasCount(sensors=[
                                SensorHasCount(sensor=0b010, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b100, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b001, min_count=vertical_min_count),
                            ]),
                            SensorHasCount(sensor=0b110, min_count=horizontal_min_count),
                            EitherSensorHasCount(sensors=[
                                SensorHasCount(sensor=0b100, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b010, min_count=vertical_min_count),
                            ]),
                        ])
                    ]
                ),
                # detects an intersection to the right
                'INTERSECT_R': IntersectRState(
                    symbol='IR', matchers=[
                        # we are detecting a blip on the right sensor, it has to last for some time (speed-dependent)
                        SensorHistoryStateMatcher(steps=[
                            EitherSensorHasCount(sensors=[
                                SensorHasCount(sensor=0b010, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b100, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b001, min_count=vertical_min_count),
                            ]),
                            SensorHasCount(sensor=0b011, min_count=horizontal_min_count),
                            EitherSensorHasCount(sensors=[
                                SensorHasCount(sensor=0b001, min_count=vertical_min_count),
                                SensorHasCount(sensor=0b010, min_count=vertical_min_count),
                            ]),
                        ])
                    ]
                ),
                # extra turn operations needed to go off the intersection in the right sensor order
                'TURN_L_OFF_LINE': OffLineLeftTurnState(symbol='TL'),
                'TURN_R_OFF_LINE': OffLineRightTurnState(symbol='TR'),
                'TURN_L_TO_LINE': ToLineLeftTurnState(symbol='TL'),
                'TURN_R_TO_LINE': ToLineRightTurnState(symbol='TR'),
            })
            line_transitions.extend(['INTERSECT_X', 'INTERSECT_Y', 'INTERSECT_T', 'INTERSECT_L', 'INTERSECT_R'])
            self.transitions.update({
                'INTERSECT_X': ['STOP'],
                'INTERSECT_Y': ['STOP'],
                'INTERSECT_R': ['STOP'],
                'INTERSECT_L': ['STOP'],
                'INTERSECT_T': ['STOP'],
                'TURN_L_OFF_LINE': ['STOP'],
                'TURN_R_OFF_LINE': ['STOP'],
                'TURN_L_TO_LINE': ['STOP'],
                'TURN_R_TO_LINE': ['STOP'],
            })

        print("Working with states:")
        for state in self.states.values():
            print("* " + state.str_full())
        print("Enabled implicit state-to-state transitions:")
        for state, transitions in self.transitions.items():
            print(f"* {state} -> {transitions}")

    def __str__(self):
        return "StateMap(%s)" % self.states
