#! /usr/bin/env python3

import investpy


def main():
    search_result = investpy.search_quotes(
        text="apple", products=["stocks"], countries=["united states"], n_results=1
    )
    print(search_result)


if __name__ == "__main__":
    main()
