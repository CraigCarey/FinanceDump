from pathlib import Path

import pandas as pd

securities_db_file = "../data/securities_db.csv"
holdings_db_file = "../data/holdings_db.csv"
id_adjustments_db_file = "../data/id_adjustments_db.csv"


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
    if not Path(securities_db_file).exists():
        return create_securities_db()

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


def get_holdings_db():
    if not Path(holdings_db_file).exists():
        return create_holdings_db()

    holdings_db = pd.read_csv(holdings_db_file, keep_default_na=False)
    return holdings_db


def write_holdings_db(df):
    df.to_csv(holdings_db_file, index=False)


def create_id_adjustments_db():
    cols = [
        "type",
        "trust",
        "id_in",
        "id_out",
        "createdAt",
        "updatedAt",
        "deletedAt",
    ]

    db = pd.DataFrame(columns=cols)

    return db


def get_id_adjustments_db():
    if not Path(id_adjustments_db_file).exists():
        return create_id_adjustments_db()

    id_adjustments_db = pd.read_csv(id_adjustments_db_file, keep_default_na=False)
    return id_adjustments_db


def write_id_adjustments_db(df):
    df.to_csv(id_adjustments_db_file, index=False)
