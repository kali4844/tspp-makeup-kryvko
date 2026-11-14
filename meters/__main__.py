"""Запуск з консолі: python -m meters <команда> ..."""
import sys

from meters import readings

USAGE = (
    "python -m meters add <лічильник> <значення> <YYYY-MM-DD>\n"
    "python -m meters consumption <лічильник> <YYYY-MM>"
)


def main(argv):
    match argv:
        case ["add", counter, value, date]:
            readings.add(counter, float(value), date)
            print("OK")
        case ["consumption", counter, month]:
            print(readings.consumption(counter, month))
        case _:
            print(USAGE)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
