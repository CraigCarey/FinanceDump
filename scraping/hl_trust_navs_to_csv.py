#! /usr/bin/env python3

import pickle

import pandas as pd

inv_trusts_nav_filename = 'investment_trusts_with_nav_231003_162641.pkl'
with open(inv_trusts_nav_filename, "rb") as handle:
    investment_trusts = pickle.load(handle)

print(investment_trusts)

investment_trusts.to_csv(path_or_buf=f"trusts.csv")
