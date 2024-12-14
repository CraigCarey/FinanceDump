#! /usr/bin/env bash

set -eux

./get_hl_trusts.py

# Takes the list from above and obtains the nav etc for each entry
# Writes to ../data/investment_trust_data_240905.csv
./get_hl_trust_data.py

# Takes the list above and appends audit information
./hl_trust_data_augment.py