#! /usr/bin/env python3

from polygon import RESTClient

client = RESTClient("BooQ9PENkj9kQmHB4bRpe2lS78KnNKxp")

financials = client.get_ticker_details("NFLX")
print(financials)

for (i, n) in enumerate(client.list_ticker_news("INTC", limit=5)):
    print(i, n)
    if i == 5:
        break
