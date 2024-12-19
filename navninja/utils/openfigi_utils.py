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


def query_openfigi_by_sedol(api_key, sedol):
    url = "https://api.openfigi.com/v3/mapping"
    headers = {"Content-Type": "application/json", "X-OPENFIGI-APIKEY": api_key}
    payload = [{"idType": "ID_SEDOL", "idValue": sedol}]
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def query_openfigi_by_isin(api_key, isin):
    url = "https://api.openfigi.com/v3/mapping"
    headers = {"Content-Type": "application/json", "X-OPENFIGI-APIKEY": api_key}
    payload = [{"idType": "ID_ISIN", "idValue": isin}]
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
