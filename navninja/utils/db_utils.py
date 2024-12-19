import pandas as pd


def create_securities_db():
    securities_db_cols = [
        "sedol",
        "isin",
        "figi",
        "name",
        "ticker",
        "exchange",
        "type",
        "sector",
    ]

    securities_db = pd.DataFrame(columns=securities_db_cols)

    return securities_db


def create_holdings_db():

    holdings_db_cols = [
        "sedol",
        "quantity",
        "createdAt",
        "updatedAt",
        "deletedAt",
    ]

    holdings_db = pd.DataFrame(columns=holdings_db_cols)

    return holdings_db
