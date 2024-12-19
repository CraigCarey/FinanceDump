import pandas as pd

securities_db_file = "../data/securities_db.csv"


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


def get_securities_db():
    securities_db = pd.read_csv(securities_db_file, keep_default_na=False)
    return securities_db


def write_securities_db(df):
    df.to_csv(securities_db_file, index=False)


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
