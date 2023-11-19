#!/usr/bin/env python3

import pandas as pd


def main():
    markets = [
        "ftse-100",
        "ftse-250",
        "ftse-350",
        "ftse-aim-100",
        "ftse-all-share",
        "ftse-small-cap",
        "ftse-techmark-100",
    ]

    df_all = pd.read_csv(f"{markets[0]}.csv", sep=";", header=0)

    for market in markets:
        print(f"{market}.csv")
        df = pd.read_csv(f"{market}.csv", sep=";", header=0)
        print(df)

        # print(df.describe())

        df_all = pd.concat([df_all, df], ignore_index=True, sort=False).drop_duplicates(
            ["epic"], keep="last"
        )
        # pd.concat([df_all, df])

    print(df_all.describe())


if __name__ == "__main__":
    main()
