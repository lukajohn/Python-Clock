"""ASCII analog-style clock for the terminal.

The dial uses plain ASCII characters so it works in simple terminals.
The hand positions are calculated from the current local time.

Run with:
    python analog_clock.py

Press Ctrl+C to exit.
"""

import math
import time


WIDTH = 49
HEIGHT = 23
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
RADIUS = 9


def clear_screen() -> None:
    print("\033[2J\033[H", end="")


def hand_endpoint(angle: float, length: float) -> tuple[int, int]:
    """Convert a clock angle to terminal coordinates."""
    x = CENTER_X + round(math.sin(angle) * length)
    # Terminal rows are taller than they are wide, so compensate vertically.
    y = CENTER_Y - round(math.cos(angle) * length * 0.5)
    return x, y


def render(now: time.struct_time) -> str:
    """Draw the clock face and its hour/minute/second hands."""
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # Clock face.
    for step in range(360):
        angle = math.radians(step)
        x = CENTER_X + round(math.sin(angle) * RADIUS)
        y = CENTER_Y - round(math.cos(angle) * RADIUS * 0.5)
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[y][x] = "o"

    # Hour markers.
    markers = {
        12: "12",
        3: "3",
        6: "6",
        9: "9",
    }
    for hour, label in markers.items():
        angle = math.radians(hour * 30)
        distance = RADIUS - 1
        x = CENTER_X + round(math.sin(angle) * distance)
        y = CENTER_Y - round(math.cos(angle) * distance * 0.5)
        for offset, char in enumerate(label):
            px = x + offset - (len(label) // 2)
            if 0 <= px < WIDTH and 0 <= y < HEIGHT:
                grid[y][px] = char

    # Hands are drawn longest first so the shorter hands remain visible.
    second_angle = math.radians(now.tm_sec * 6)
    minute_angle = math.radians((now.tm_min + now.tm_sec / 60) * 6)
    hour_angle = math.radians(((now.tm_hour % 12) + now.tm_min / 60) * 30)

    for angle, length, char in (
        (second_angle, RADIUS - 2, "."),
        (minute_angle, RADIUS - 3, "-"),
        (hour_angle, RADIUS - 5, "#"),
    ):
        x_end, y_end = hand_endpoint(angle, length)
        steps = max(abs(x_end - CENTER_X), abs(y_end - CENTER_Y), 1)
        for step in range(1, steps + 1):
            x = round(CENTER_X + (x_end - CENTER_X) * step / steps)
            y = round(CENTER_Y + (y_end - CENTER_Y) * step / steps)
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                grid[y][x] = char

    grid[CENTER_Y][CENTER_X] = "O"
    return "\n".join("".join(row).rstrip() for row in grid)


def main() -> None:
    try:
        while True:
            now = time.localtime()
            clear_screen()
            print("ASCII ANALOG CLOCK")
            print("==================")
            print()
            print(render(now))
            print()
            print(time.strftime("%H:%M:%S"))
            print("Press Ctrl+C to exit")
            time.sleep(0.1)
    except KeyboardInterrupt:
        clear_screen()
        print("Analog clock stopped.")


if __name__ == "__main__":
    main()
