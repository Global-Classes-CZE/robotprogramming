class LightPlacement:
    """Defines the color scheme and placement used in the Joy-Car Robot."""
    LEFT_DIRECTION = 0
    RIGHT_DIRECTION = 1

    blinkers = {
        LEFT_DIRECTION: [1, 4],
        RIGHT_DIRECTION: [2, 7]
    }
    headlights = [0, 3]
    backlights = [5, 6]
    # Only one light is used for reverse, other stays as back or brake light
    reverse_lights = [5]

    WHITE_BRIGHT = (255, 255, 255)
    WHITE_MID = (128, 128, 128)
    WHITE_MILD = (60, 60, 60)
    ORANGE = (100, 35, 0)
    RED_BRIGHT = (255, 0, 0)
    RED_MILD = (60, 0, 0)

    initial_color_for_position = [
        WHITE_MILD, ORANGE, ORANGE, WHITE_MILD,
        ORANGE, RED_MILD, RED_MILD, ORANGE
    ]
