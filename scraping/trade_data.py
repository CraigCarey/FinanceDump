#!/usr/bin/env python3

import sys

import pandas as pd


def display_metrics(df: pd.DataFrame):
    total_vol = df.volume.sum()
    total_val = df.tradeValue.sum()
    avg_price = total_val / total_vol * 100
    avg_vol = int(df.volume.mean())
    last_price = df.price.iloc[-1]
    last_vol = df.volume.iloc[-1]
    last_val = df.tradeValue.iloc[-1]
    hi_price = df.price.max()
    lo_price = df.price.min()
    price_range = hi_price - lo_price
    mid_range = lo_price + (price_range / 2)

    largest_vol = df.volume.max()
    largest_vol_idx = df.volume.idxmax()
    largest_vol_val = df.loc[largest_vol_idx, "tradeValue"]
    largest_vol_time = df.loc[largest_vol_idx, "tradeTime"].time()

    largest_val = df.tradeValue.max()
    largest_val_idx = df.tradeValue.idxmax()
    largest_val_vol = df.loc[largest_val_idx, "volume"]
    largest_val_time = df.loc[largest_val_idx, "tradeTime"].time()

    print()
    print(f"\t{'Volume:':15}{total_vol:<15,}\t\t(£{total_val:,})")
    print(
        f"\t{'Largest vol:':15}{largest_vol:<15,}\t\t(£{largest_vol_val:,} @ {largest_vol_val/largest_vol:,.2f} @ {largest_vol_time})"
    )
    print(
        f"\t{'Largest val:':15}£{largest_val:<15,}\t\t({largest_val_vol:,} @ {largest_val/largest_val_vol:,.2f} @ {largest_val_time})"
    )
    print(
        f"\t{'Price range:':15}{lo_price:,.2f} - {hi_price:<10,.2f}\t({price_range:,.2f}, {100*(price_range / mid_range):.1f}%)"
    )
    print(
        f"\t{'Avg trade:':15}{avg_vol:,} @ {avg_price:<15,.2f}\t(£{(avg_vol * avg_price)/100:,.2f})"
    )
    print(f"\t{'Last trade:':15}{last_vol:,} @ {last_price:<15,.2f}\t(£{last_val})")
    print()


def main():

    if len(sys.argv) < 2:
        print("Missing ticker arg")
        exit(1)

    ticker = sys.argv[1]
    ticker = ticker.strip().upper()

    url = f"https://api.londonstockexchange.com/api/gw/lse/download/{ticker}/trades"

    df = pd.read_csv(url).drop(["currency", "venueOfPublication", "micCode"], axis=1)
    df.tradeValue = df.tradeValue.astype(int)
    df.volume = df.volume.astype(int)
    df.tradeTime = pd.to_datetime(df.tradeTime).dt.round("1s")
    df = df[::-1].reset_index().drop(["index"], axis=1)

    df_split_by_dates = []
    for group in df.groupby(df.tradeTime.dt.day):
        df_split_by_dates.append(group[1])

    curr_idx = -1
    prev_idx = -2
    
    # handles new month rollover
    date_ordered = df_split_by_dates[0].iloc[0].tradeTime < df_split_by_dates[1].iloc[0].tradeTime
    if not date_ordered:
        curr_idx, prev_idx = prev_idx, curr_idx

    df_prev = df_split_by_dates[prev_idx].reset_index(drop=True)
    df_curr = df_split_by_dates[curr_idx].reset_index(drop=True)

    print(df_curr.to_markdown())
    print()
    print("Yesterday:")
    display_metrics(df_prev)

    print("Today:")
    display_metrics(df_curr)

    current_price = df_curr.price.iloc[-1]
    close_price = df_prev.price.iloc[-1]
    price_del = current_price - close_price

    print(
        f"\t{'Change:':15}{price_del:<10,.2f}\t\t({100*(price_del / current_price):,.2f}%)"
    )
    print()


if __name__ == "__main__":
    main()
