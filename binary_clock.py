"""Readable ASCII binary clock for the terminal.

Each row represents one bit. The columns are:
    H H H H H H M M M M M M S S S S S S

A '#' means the bit is on and '.' means it is off.

Run with:
    python binary_clock.py

Press Ctrl+C to exit.
"""

import time


LABELS = ("H", "M", "S")


def bits(value: int, width: int = 6) -> str:
    """Return value as a fixed-width binary string."""
    return format(value, f"0{width}b")


def render(hour: int, minute: int, second: int) -> str:
    """Render hours, minutes and seconds as readable binary columns."""
    values = [bits(hour), bits(minute), bits(second)]

    lines = [
        "       " + " ".join(f"{label}" for label in LABELS),
        "       " + "-" * 17,
        "       " + " ".join("1 2 3 4 5 6".split()),
    ]

    for row in range(6):
        cells = []
        for value in values:
            bit = value[row]
            cells.append("#" if bit == "1" else ".")
        lines.append(f"bit {5 - row}   " + "   ".join(cells))

    return "\n".join(lines)


def clear_screen() -> None:
    print("\033[2J\033[H", end="")


def main() -> None:
    try:
        while True:
            now = time.localtime()
            clear_screen()
            print("ASCII BINARY CLOCK")
            print("==================")
            print()
            print(render(now.tm_hour, now.tm_min, now.tm_sec))
            print()
            print("# = 1 / on    . = 0 / off")
            print("Columns: H = hours, M = minutes, S = seconds")
            print("Press Ctrl+C to exit")
            time.sleep(0.2)
    except KeyboardInterrupt:
        clear_screen()
        print("Binary clock stopped.")


if __name__ == "__main__":
    main()
