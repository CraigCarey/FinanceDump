from datetime import datetime

import fa_mods as famods
import fundamentalanalysis as fa
import pandas as pd


def get_income_statements(ticker: str, api_key: str, data):

    data["income_statement"] = fa.income_statement(ticker, api_key, period="annual")

    if not data["income_statement"].empty:
        data["income_statement"].drop(
            labels=["calendarYear", "period", "link", "finalLink"], axis=0, inplace=True
        )
    else:
        data["income_statement"] = None

    data["income_statement_quarterly"] = fa.income_statement(
        ticker, api_key, period="quarter"
    )

    if not data["income_statement_quarterly"].empty:
        data["income_statement_quarterly"].drop(
            labels=["calendarYear", "period", "link", "finalLink"], axis=0, inplace=True
        )
    else:
        data["income_statement_quarterly"] = None

    data["income_statement_growth"] = famods.income_statement_growth(ticker, api_key)

    if data["income_statement_growth"].empty:
        data["income_statement_growth"] = None


def get_cashflow_statements(ticker: str, api_key: str, data):

    data["cashflow_statement"] = fa.cash_flow_statement(
        ticker, api_key, period="annual"
    )

    if not data["cashflow_statement"].empty:
        data["cashflow_statement"].drop(
            labels=["calendarYear", "period", "link", "finalLink"], axis=0, inplace=True
        )
    else:
        data["cashflow_statement"] = None

    data["cashflow_statement_quarterly"] = fa.cash_flow_statement(
        ticker, api_key, period="quarter"
    )

    if not data["cashflow_statement_quarterly"].empty:
        data["cashflow_statement_quarterly"].drop(
            labels=["calendarYear", "period", "link", "finalLink"], axis=0, inplace=True
        )
    else:
        data["cashflow_statement_quarterly"] = None

    data["cashflow_statement_growth"] = famods.cash_flow_statement_growth(
        ticker, api_key
    )

    if data["cashflow_statement_growth"].empty:
        data["cashflow_statement_growth"] = None


def get_balance_sheet_statements(ticker: str, api_key: str, data):

    data["balance_sheet_statement"] = fa.balance_sheet_statement(
        ticker, api_key, period="annual"
    )

    if not data["balance_sheet_statement"].empty:
        data["balance_sheet_statement"].drop(
            labels=["calendarYear", "period", "link", "finalLink"], axis=0, inplace=True
        )
    else:
        data["balance_sheet_statement"] = None

    data["balance_sheet_statement_quarterly"] = fa.balance_sheet_statement(
        ticker, api_key, period="quarter"
    )

    if not data["balance_sheet_statement_quarterly"].empty:
        data["balance_sheet_statement_quarterly"].drop(
            labels=["calendarYear", "period", "link", "finalLink"], axis=0, inplace=True
        )
    else:
        data["balance_sheet_statement_quarterly"] = None

    data["balance_sheet_statement_growth"] = famods.balance_sheet_statement_growth(
        ticker, api_key
    )

    if data["balance_sheet_statement_growth"].empty:
        data["balance_sheet_statement_growth"] = None


def get_key_metrics(ticker: str, api_key: str, data):

    data["key_metrics"] = fa.key_metrics(ticker, api_key, period="annual")

    if not data["key_metrics"].empty:
        data["key_metrics"].drop(["period"])
    else:
        data["key_metrics"] = None

    data["key_metrics_quarterly"] = fa.key_metrics(ticker, api_key, period="quarter")

    if not data["key_metrics_quarterly"].empty:
        data["key_metrics_quarterly"].drop(["period"])
    else:
        data["key_metrics_quarterly"] = None

    data["key_metrics_ttm"] = fa.key_metrics(ticker, api_key, period="annual", TTM=True)

    if data["key_metrics_ttm"].empty:
        data["key_metrics_ttm"] = None


def get_financial_ratios(ticker: str, api_key: str, data):

    data["financial_ratios"] = fa.financial_ratios(ticker, api_key, period="annual")

    if not data["financial_ratios"].empty:
        data["financial_ratios"].drop(["period"])
    else:
        data["financial_ratios"] = None

    data["financial_ratios_quarterly"] = fa.financial_ratios(
        ticker, api_key, period="quarter"
    )

    if not data["financial_ratios_quarterly"].empty:
        data["financial_ratios_quarterly"].drop(["period"])
    else:
        data["financial_ratios_quarterly"] = None

    data["financial_ratios_ttm"] = fa.financial_ratios(
        ticker, api_key, period="annual", TTM=True
    )

    if data["financial_ratios_ttm"].empty:
        data["financial_ratios_ttm"] = None


def get_ticker_data(ticker: str, api_key: str):
    """
    income_statement
    income_statement_quarterly
    income_statement_growth
    cashflow_statement
    cashflow_statement_quarterly
    cashflow_statement_growth
    balance_sheet_statement
    balance_sheet_statement_quarterly
    balance_sheet_statement_growth
    discounted_cash_flow
    advanced_discounted_cash_flow
    advanced_levered_discounted_cash_flow
    key_metrics
    key_metrics_quarterly
    key_metrics_ttm
    financial_ratios
    financial_ratios_quarterly
    financial_ratios_ttm
    financial_statement_growth
    owner_earnings
    enterprise_values
    dividends
    scores
    """
    data = {}

    data["timestamp"] = datetime.timestamp(datetime.now())

    get_income_statements(ticker, api_key, data)

    get_cashflow_statements(ticker, api_key, data)

    get_balance_sheet_statements(ticker, api_key, data)

    data["discounted_cash_flow"] = famods.discounted_cash_flow(ticker, api_key)

    data["advanced_discounted_cash_flow"] = famods.advanced_discounted_cash_flow(
        ticker, api_key
    )

    data[
        "advanced_levered_discounted_cash_flow"
    ] = famods.advanced_levered_discounted_cash_flow(ticker, api_key)

    get_key_metrics(ticker, api_key, data)

    data["growth"] = fa.financial_statement_growth(ticker, api_key, period="annual")

    if not data["growth"].empty:
        data["growth"].drop(["period"])
    else:
        data["growth"] = None

    data["owner_earnings"] = famods.owner_earnings(ticker, api_key)

    if data["owner_earnings"].empty:
        data["owner_earnings"] = None

    data["enterprise_values"] = famods.enterprise_values(ticker, api_key)

    if data["enterprise_values"].empty:
        data["enterprise_values"] = None

    try:
        data["dividends"] = fa.stock_dividend(ticker, api_key)
        if not data["dividends"].empty:
            data["dividends"].drop(["recordDate", "declarationDate"], axis=1)
        else:
            data["dividends"] = None
    except:
        data["dividends"] = None

    data["scores"] = famods.score(ticker, api_key)

    if data["scores"].empty:
        data["scores"] = None

    return data

def get_ticker_mf_am_data(ticker: str, api_key: str):
    """
    income_statement
    key_metrics_ttm
    """
    data = {}

    data["timestamp"] = datetime.timestamp(datetime.now())

    data["income_statement"] = fa.income_statement(ticker, api_key, period="annual", limit=1).iloc[:, 0]

    if not data["income_statement"].empty:
        data["income_statement"].drop(
            labels=["period", "link", "finalLink"], axis=0, inplace=True
        )
    else:
        data["income_statement"] = None

    data["key_metrics_ttm"] = fa.key_metrics(ticker, api_key, period="annual", TTM=True)

    return data

def fmp_request(api: str, ticker: str, api_key, v4: bool = False):
    """
    Sends an API request to financialmodelingprep.com, converting the response to a df

        Parameters:
            api (str):     The API to query, e.g. 'income-statement'
            ticker (str):  The tickername to query, e.g 'MSFT'
            api_key (str): Your fmp API key

        Returns:
            dataframe
    """
    if v4:
        url = f"https://financialmodelingprep.com/api/v4/{api}?symbol={ticker}&apikey={api_key}"
    else:
        url = (
            f"https://financialmodelingprep.com/api/v3/{api}/{ticker}?apikey={api_key}"
        )
    return pd.read_json(url)
