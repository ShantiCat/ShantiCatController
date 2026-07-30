"""ShantiCat Controller command-line entry point."""

from .controller import Controller


def main() -> None:
    """Start ShantiCat Controller."""

    Controller().run()


if __name__ == "__main__":
    main()