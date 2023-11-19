#! /usr/bin/env python3

import pickle
import pandas as pd
from datetime import datetime
import queue
import threading
import time

import fundamentalanalysis as fa
import fa_mods as famods
import fa_utils


class FmpGatherer:

    def __init__(self):

        with open('/home/craigc/.keys/financialmodelingprep.txt', 'r') as file:
            self.api_key = file.read()

        self.thread_lock = threading.Lock()

        self.datestamp = datetime.now().strftime('%y%m%d')

        self.symbols_filepath = f'../data/all_mf_am_symbols_{self.datestamp}.pkl'

    def fetch_tradable_stock_symbols(self, target_exchanges):

        tradeable_companies = famods.tradable_companies(self.api_key)

        available_companies = tradeable_companies.drop(
            columns=['name', 'price', 'exchange'])
        available_companies = available_companies.rename(
            columns={'exchangeShortName': 'exchange'})

        available_companies_exch_filtered = available_companies[available_companies.exchange.isin(
            target_exchanges)]

        available_companies_exch_stock_filtered = available_companies_exch_filtered[(
            available_companies_exch_filtered.type == 'stock')]
        available_companies_exch_stock_filtered = available_companies_exch_stock_filtered.drop(columns=[
            'type'])

        symbols = available_companies_exch_stock_filtered.reset_index()

        with open(self.symbols_filepath, 'wb') as file:
            pickle.dump(symbols, file)

        return symbols

    def fetch_symbols(self, target_exchanges):
        available_companies_raw = fa.available_companies(self.api_key)

        available_companies = available_companies_raw.drop(
            columns=['name', 'price', 'exchange'])
        available_companies = available_companies.rename(
            columns={'exchangeShortName': 'exchange'})

        available_companies_exch_filtered = available_companies[available_companies.exchange.isin(
            target_exchanges)]

        available_companies_exch_stock_filtered = available_companies_exch_filtered[(
            available_companies_exch_filtered.type == 'stock')]
        available_companies_exch_stock_filtered = available_companies_exch_stock_filtered.drop(columns=[
            'type'])

        symbols = available_companies_exch_stock_filtered.reset_index()

        with open(self.symbols_filepath, 'wb') as file:
            pickle.dump(symbols, file)

        return symbols

    def load_symbols(self):

        with open(self.symbols_filepath, 'rb') as file:
            symbols = pickle.load(file)

            return symbols

    def get_mf_am_data(self, symbols):

        stock_data = {}
        failed = []
        num_stocks = len(symbols)
        cnt = 0

        symbol_queue = queue.Queue()
        [symbol_queue.put(s) for s in symbols]
        # symbol_queue.qsize()

        def worker():
            nonlocal cnt
            nonlocal stock_data
            nonlocal failed
            while True:

                time.sleep(1)

                with self.thread_lock:
                    cnt += 1
                    symbol = symbol_queue.get()
                    print(
                        f'[{cnt}/{num_stocks}]: getting {symbol} - f[{len(failed)}], s[{len(stock_data)}]')

                if symbol in stock_data:
                    print(f"Already have {symbol}, skipping")
                    continue

                try:
                    data = fa_utils.get_ticker_mf_am_data(symbol, self.api_key)
                    data['exchange'] = symbols[symbol]
                    stock_data[symbol] = data
                    print(f"{symbol} SUCCESS")
                except:
                    print(f"{symbol} FAILED")
                    failed.append(symbol)

                symbol_queue.task_done()

        for x in range(4):
            name = "Thread_" + str(x)
            t = threading.Thread(name=name, target=worker, daemon=True).start()

        symbol_queue.join()

        print(len(failed))
        print(len(stock_data))

        with open(f'../data/all_mf_am_{self.datestamp}.pkl', 'wb') as file:
            pickle.dump(stock_data, file)

        with open(f'../data/all_mf_am_{self.datestamp}_failed.pkl', 'wb') as file:
            pickle.dump(failed, file)


def main():

    gatherer = FmpGatherer()

    target_exchanges = [
        "AMEX",    # NYSE ARCA
        "AMS",     # Amsterdam
        "XETRA",   # Deutsche Boerse Exchange, Frankfurt
        "CPH",     # Copenhagen
        "STO",     # Stockholm
        "HEL",     # Helsinki
        "OSE",     # Oslo
        "EURONEXT",
        "NASDAQ",
        "NYSE",
        "LSE",
        "TLV",     # Tel Aviv
        "TSX",     # Toronto
    ]

    symbols = gatherer.fetch_tradable_stock_symbols(target_exchanges)

    symbols = gatherer.load_symbols()

    # symbols = symbols.head()

    symbols_dict = {}

    for _, row in symbols.iterrows():
        symbols_dict[row.symbol] = row.exchange

    print(len(symbols_dict))

    gatherer.get_mf_am_data(symbols_dict)


if __name__ == "__main__":
    main()
