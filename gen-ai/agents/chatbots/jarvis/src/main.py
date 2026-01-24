"""Main entry point for the Jarvis CLI."""

import argparse


def main():
    """Main entry point for the jarvis CLI command."""
    parser = argparse.ArgumentParser(
        prog="jarvis",
        description="Jarvis - A Python CLI application",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    args = parser.parse_args()

    print("Hello from Jarvis!")


if __name__ == "__main__":
    main()
