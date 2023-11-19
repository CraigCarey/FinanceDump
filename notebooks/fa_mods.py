import json
from urllib.error import HTTPError
from urllib.request import urlopen

import pandas as pd


def tradable_companies(api_key):
    """
    Description
    ----
    Gives all tradable tickers, company names, current price and stock exchange that are available
    for retrieval for financial statements, ratios and extended stock data. General stock
    data can be retrieved for any company or financial instrument.

    Input
    ----
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/

    Output
    ----
    data (dataframe)
        Data with the ticker as the index and the company name, price and
        stock exchange in the columns.
    """
    try:
        response = urlopen(
            f"https://financialmodelingprep.com/api/v3/available-traded/list?apikey={api_key}"
        )
        data = json.loads(response.read().decode("utf-8"))
    except HTTPError:
        raise ValueError(
            "This endpoint is only for premium members. Please visit the subscription page to upgrade the "
            "plan (Starter or higher) at https://financialmodelingprep.com/developer/docs/pricing"
        )

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if len(data) == 0:
        return pd.DataFrame

    df = pd.DataFrame(data)
    df.loc[df["name"].isna(), "name"] = df["symbol"]
    df = df.set_index("symbol")

    return df


def income_statement_growth(ticker, api_key, limit=0, period="annual"):
    """
    Description
    ----
    Gives information about the growth of the income statement of a company over time
    which includes i.a. revenue, operating expenses, profit margin and ETBIDA.

    Input
    ----
    ticker (string)
        The company ticker (for example: "GOOGL")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/
    limit (integer)
        The limit for the years of data

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """

    URL = (
        f"https://financialmodelingprep.com/api/v3/income-statement-growth/{ticker}"
        f"?period={period}&limit={limit}&apikey={api_key}"
    )

    try:
        response = urlopen(URL)
        data = json.loads(response.read().decode("utf-8"))
    except HTTPError:
        raise ValueError(
            "This endpoint is only for premium members. Please visit the subscription page to upgrade the "
            "plan (Starter or higher) at https://financialmodelingprep.com/developer/docs/pricing"
        )

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if len(data) == 0:
        return pd.DataFrame

    data_formatted = {}
    for value in data:
        date = int(value["date"][:4])

        data_formatted[date] = value

    return pd.DataFrame(data_formatted).drop(["symbol", "period"])


def balance_sheet_statement_growth(ticker, api_key, limit=0):
    """
    Description
    ----
    Gives information about the growth of the balance sheet statement of a company over time
    which includes i.a. total assets, payables, tax liabilities and investments.

    Input
    ----
    ticker (string)
        The company ticker (for example: "GOOGL")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/
    limit (integer)
        The limit for the years of data

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """

    URL = (
        f"https://financialmodelingprep.com/api/v3/balance-sheet-statement-growth/{ticker}"
        f"?limit={limit}&apikey={api_key}"
    )

    try:
        response = urlopen(URL)
        data = json.loads(response.read().decode("utf-8"))
    except HTTPError:
        raise ValueError(
            "This endpoint is only for premium members. Please visit the subscription page to upgrade the "
            "plan (Starter or higher) at https://financialmodelingprep.com/developer/docs/pricing"
        )

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if len(data) == 0:
        return pd.DataFrame

    data_formatted = {}
    for value in data:
        date = int(value["date"][:4])

        data_formatted[date] = value

    return pd.DataFrame(data_formatted).drop(["symbol", "period"])


def cash_flow_statement_growth(ticker, api_key, limit=0):
    """
    Description
    ----
    Gives information about the growth of the cash flow statement of a company over time
    which includes i.a. operating cash flow, dividend payments and capital expenditure.

    Input
    ----
    ticker (string)
        The company ticker (for example: "GOOGL")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/
    limit (integer)
        The limit for the years of data

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """

    URL = (
        f"https://financialmodelingprep.com/api/v3/cash-flow-statement-growth/{ticker}"
        f"?limit={limit}&apikey={api_key}"
    )

    try:
        response = urlopen(URL)
        data = json.loads(response.read().decode("utf-8"))
    except HTTPError:
        raise ValueError(
            "This endpoint is only for premium members. Please visit the subscription page to upgrade the "
            "plan (Starter or higher) at https://financialmodelingprep.com/developer/docs/pricing"
        )

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if len(data) == 0:
        return pd.DataFrame

    data_formatted = {}
    for value in data:
        date = int(value["date"][:4])

        data_formatted[date] = value

    df = pd.DataFrame(data_formatted)

    try:
        df = df.drop(["symbol", "period"])
    except:
        pass

    return df


def discounted_cash_flow(ticker, api_key, period="annual", limit=0):
    """
    Description
    ----
    Gives information about the discounted cash flow (DCF) of a company which includes
    i.a. the (current) stock price and DCF and over time.

    Input
    ----
    ticker (string)
        The company ticker (for example: "UBER")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/
    period (string)
        Data period, this can be "annual" or "quarter".
    limit (integer)
        The limit for the years of data

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """
    try:
        # response = urlopen(f"https://financialmodelingprep.com/api/v3/discounted-cash-flow/{ticker}"
        #                    f"?period={period}&limit={limit}&apikey={api_key}")
        URL = f"https://financialmodelingprep.com/api/v3/discounted-cash-flow/{ticker}?apikey={api_key}"
        response = urlopen(URL)
        data = json.loads(response.read().decode("utf-8"))
    except HTTPError:
        raise ValueError(
            "This endpoint is only for premium members. Please visit the subscription page to upgrade the "
            "plan (Starter or higher) at https://financialmodelingprep.com/developer/docs/pricing"
        )

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if len(data) == 0:
        return pd.DataFrame

    data_json_current = data[0]

    try:
        data_json_current["price"] = data_json_current.pop("Stock Price")
        data_json_current["dcf"] = data_json_current.pop("DCF")
    except KeyError:
        pass

    try:
        response = urlopen(
            f"https://financialmodelingprep.com/api/v3/"
            f"historical-discounted-cash-flow/{ticker}?apikey={api_key}"
        )
        data = json.loads(response.read().decode("utf-8"))
        data_json = data[0]["historicalDCF"]
    except HTTPError:
        raise ValueError(
            "This endpoint is only for premium members. Please visit the subscription page to upgrade the "
            "plan (Starter or higher) at https://financialmodelingprep.com/developer/docs/pricing"
        )
    except KeyError:
        try:
            response = urlopen(
                f"https://financialmodelingprep.com/api/v3/"
                f"historical-discounted-cash-flow-statement/{ticker}?period={period}&apikey={api_key}"
            )
            data = json.loads(response.read().decode("utf-8"))
            data_json = data
        except HTTPError:
            raise ValueError(
                "This endpoint is only for premium members. Please visit the subscription page to upgrade the "
                "plan (Starter or higher) at https://financialmodelingprep.com/developer/docs/pricing"
            )
        except IndexError:
            raise ValueError(
                f"No information available for the ticker {ticker}. Please check if this ticker is actually a stock "
                f"with the available_companies function."
            )

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if len(data) == 0:
        return pd.DataFrame

    data_formatted = {}

    if period == "quarter":
        current_year = data_json_current["date"][:7]
    else:
        current_year = data_json_current["date"][:4]
    data_formatted[current_year] = data_json_current

    for data in data_json:
        if period == "quarter":
            date = data["date"][:7]
        else:
            date = data["date"][:4]
        data_formatted[date] = data

    return pd.DataFrame(data_formatted).drop(["symbol"])


def advanced_discounted_cash_flow(ticker, api_key):
    """
    Description
    ----
    Gives advanced Discounted Cash Flow projection including WACC

    Input
    ----
    ticker (string)
        The company ticker (for example: "GOOGL")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """

    URL = f"https://financialmodelingprep.com/api/v4/advanced_discounted_cash_flow?symbol={ticker}&apikey={api_key}"

    try:
        response = urlopen(URL)
        data = json.loads(response.read().decode("utf-8"))
    except HTTPError:
        raise ValueError(
            "This endpoint is only for premium members. Please visit the subscription page to upgrade the "
            "plan (Starter or higher) at https://financialmodelingprep.com/developer/docs/pricing"
        )

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if len(data) == 0:
        return pd.DataFrame

    data_formatted = {}
    for value in data:
        date = int(value["year"])

        data_formatted[date] = value

    return pd.DataFrame(data_formatted).drop(["symbol", "year"])


def advanced_levered_discounted_cash_flow(ticker, api_key):
    """
    Description
    ----
    Gives Advanced Levered Discounted Cash Flow projection including WACC

    Input
    ----
    ticker (string)
        The company ticker (for example: "GOOGL")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """

    URL = f"https://financialmodelingprep.com/api/v4/advanced_levered_discounted_cash_flow?symbol={ticker}&apikey={api_key}"

    try:
        response = urlopen(URL)
        data = json.loads(response.read().decode("utf-8"))
    except HTTPError:
        raise ValueError(
            "This endpoint is only for premium members. Please visit the subscription page to upgrade the "
            "plan (Starter or higher) at https://financialmodelingprep.com/developer/docs/pricing"
        )

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if len(data) == 0:
        return pd.DataFrame

    data_formatted = {}
    for value in data:
        date = int(value["year"])

        data_formatted[date] = value

    return pd.DataFrame(data_formatted).drop(["symbol", "year"])


def score(ticker, api_key):
    """
    Description
    ----
    Gives Stock Financial scores

    Input
    ----
    ticker (string)
        The company ticker (for example: "GOOGL")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """

    URL = f"https://financialmodelingprep.com/api/v4/score?symbol={ticker}&apikey={api_key}"

    try:
        response = urlopen(URL)
        data = json.loads(response.read().decode("utf-8"))

    except HTTPError:
        raise ValueError(
            "This endpoint is only for premium members. Please visit the subscription page to upgrade the "
            "plan (Starter or higher) at https://financialmodelingprep.com/developer/docs/pricing"
        )

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if len(data) == 0:
        return pd.DataFrame

    del data[0]["symbol"]

    df = pd.DataFrame(data)

    try:
        df = df.drop(["symbol"])
    except:
        pass

    return df


def enterprise_values(ticker, api_key):
    """
    Description
    ----
    Gives Company annual enterprise value

    Input
    ----
    ticker (string)
        The company ticker (for example: "GOOGL")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """

    URL = f"https://financialmodelingprep.com/api/v3/enterprise-values/{ticker}?apikey={api_key}"

    try:
        response = urlopen(URL)
        data = json.loads(response.read().decode("utf-8"))
    except HTTPError:
        raise ValueError(
            "This endpoint is only for premium members. Please visit the subscription page to upgrade the "
            "plan (Starter or higher) at https://financialmodelingprep.com/developer/docs/pricing"
        )

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if len(data) == 0:
        return pd.DataFrame

    del data[0]["symbol"]

    data_formatted = {}
    for value in data:
        date = int(value["date"][:4])
        data_formatted[date] = value

    df = pd.DataFrame(data_formatted)

    try:
        df = df.drop(["symbol"])
    except:
        pass

    return df


def owner_earnings(ticker, api_key):
    """
    Description
    ----
    Gives Company owner earnings

    Input
    ----
    ticker (string)
        The company ticker (for example: "GOOGL")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """

    URL = f"https://financialmodelingprep.com/api/v4/owner_earnings?symbol={ticker}&apikey={api_key}"

    try:
        response = urlopen(URL)
        data = json.loads(response.read().decode("utf-8"))
    except HTTPError:
        raise ValueError(
            "This endpoint is only for premium members. Please visit the subscription page to upgrade the "
            "plan (Starter or higher) at https://financialmodelingprep.com/developer/docs/pricing"
        )

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if len(data) == 0:
        return pd.DataFrame

    data_formatted = {}
    for value in data:
        date = int(value["date"][:4])
        data_formatted[date] = value

    df = pd.DataFrame(data_formatted)

    try:
        df = df.drop(["symbol"])
    except:
        pass

    return df
