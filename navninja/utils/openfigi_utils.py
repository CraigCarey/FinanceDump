import requests


def read_api_key(file_path):
    try:
        with open(file_path, "r") as file:
            api_key = file.read().strip()
            return api_key
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def query_openfigi(api_key, id_type, id_val):
    url = "https://api.openfigi.com/v3/mapping"
    headers = {"Content-Type": "application/json", "X-OPENFIGI-APIKEY": api_key}
    payload = [{"idType": f"ID_{id_type}", "idValue": id_val}]
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        if "warning" in data[0] or "error" in data[0]:
            return None

        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def query_openfigi_by_sedol(api_key, sedol):
    return query_openfigi(api_key, "SEDOL", sedol)


def query_openfigi_by_isin(api_key, isin):
    return query_openfigi(api_key, "ISIN", isin)


def figi_to_security(figi_data, sedol):
    sedol_data = figi_data[0]["data"][0]
    security = {
        "sedol": sedol,
        "figi": sedol_data["figi"],
        "name": sedol_data["name"],
        "ticker": sedol_data["ticker"],
        "exchange": sedol_data["exchCode"],
        "type": sedol_data["securityType"],
        "sector": sedol_data["marketSector"],
    }

    return security
