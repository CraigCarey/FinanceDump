#!/usr/bin/env python3

import finnhub

finnhub_client = finnhub.Client(api_key="c5k5j3qad3ie96ef67kg")

fin = finnhub_client.financials_reported(symbol="POYYF", freq="quarterly")
pass
