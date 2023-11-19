#!/usr/bin/env python3

from openbb_terminal.sdk import openbb


def main():
    print(openbb.economy.events())


if __name__ == "__main__":
    main()
