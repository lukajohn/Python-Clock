"""Readable ASCII digital clock for the terminal.

Run with:
    python digital_clock.py

Press Ctrl+C to exit.
"""

import time


DIGITS = {
    "0": ["###", "# #", "# #", "# #", "###"],
    "1": ["  #", "  #", "  #", "  #", "  #"],
    "2": ["###", "  #", "###", "#  ", "###"],
    "3": ["###", "  #", "###", "  #", "###"],
    "4": ["# #", "# #", "###", "  #", "  #"],
    "5": ["###", "#  ", "###", "  #", "###"],
    "6": ["###", "#  ", "###", "# #", "###"],
    "7": ["###", "  #", "  #", "  #", "  #"],
    "8": ["###", "# #", "###", "# #", "###"],
    "9": ["###", "# #", "###", "  #", "###"],
}


def render_time(value: str) -> str:
    """Render HH:MM:SS as large, readable ASCII digits."""
    rows = []

    for row in range(5):
        parts = []
        for character in value:
            if character == ":":
                parts.append(" # " if row in (1, 3) else "   ")
            else:
                parts.append(DIGITS[character][row])
        rows.append("  ".join(parts))

    return "\n".join(rows)


def clear_screen() -> None:
    print("\033[2J\033[H", end="")


def main() -> None:
    try:
        while True:
            now = time.strftime("%H:%M:%S")
            clear_screen()
            print("ASCII DIGITAL CLOCK")
            print("=" * 19)
            print()
            print(render_time(now))
            print()
            print("Press Ctrl+C to exit")
            time.sleep(0.2)
    except KeyboardInterrupt:
        clear_screen()
        print("Digital clock stopped.")


if __name__ == "__main__":
    main()
