#! /usr/bin/env python3

from datetime import datetime

import pandas as pd

pd.set_option("future.no_silent_downcasting", True)


def get_audit_df():
    audit_data_filename = "../navninja/data/investment_trust_data_audit.csv"

    audit_df = pd.read_csv(audit_data_filename).drop(["isin"], axis=1)
    audit_df["winding_down"] = audit_df["winding_down"].fillna(False)
    # audit_df['auditable'] = audit_df['auditable'].fillna(False)
    audit_df["audit_link"] = audit_df["audit_link"].fillna("")

    return audit_df


def main():

    audit_df = get_audit_df()

    datestamp = datetime.now().strftime("%y%m%d")
    inv_trusts_filename = f"../data/investment_trust_data_{datestamp}.csv"

    trust_data_df = pd.read_csv(inv_trusts_filename)
    trust_data_df = trust_data_df.drop(columns=["Unnamed: 0"], axis=1)

    trusts_with_audit = pd.merge(trust_data_df, audit_df, on="symbol", how="inner")
    trusts_with_audit.to_csv(f"../data/investment_trust_data_audit_{datestamp}.csv")


if __name__ == "__main__":
    main()
