import requests
import hashlib
import re

import pandas as pd

from pandas.api.types import is_string_dtype, is_numeric_dtype


cols = ["SEDOL", "Name", "Holding", "Value", "Weight"]


def calculate_md5(file_path):
    try:
        # Open the file in binary read mode
        with open(file_path, "rb") as file:
            # Create an MD5 hash object
            md5_hash = hashlib.md5()
            # Read the file in chunks to handle large files
            for chunk in iter(lambda: file.read(4096), b""):
                md5_hash.update(chunk)
        # Return the hexadecimal digest
        return md5_hash.hexdigest()
    except FileNotFoundError:
        return "File not found. Please check the path."
    except Exception as e:
        return f"An error occurred: {e}"


def download_pdf(url, save_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Write the content to a file
            with open(save_path, "wb") as file:
                file.write(response.content)
            print(f"PDF downloaded successfully and saved to {save_path}")
        else:
            print(f"Failed to download PDF. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


def lines_to_df(lines):

    df = pd.DataFrame(columns=cols)

    for line in lines:
        sections = line.split(" ")

        sedol = sections[0]
        weight = sections[-1]
        weight = float(weight.strip("%")) / 100

        value = sections[-2]
        value = clean_float_str(value)

        holding = sections[-3]
        holding = clean_float_str(holding)

        name = " ".join(sections[1:-3])

        entry = {
            cols[0]: sedol,
            cols[1]: name,
            cols[2]: holding,
            cols[3]: value,
            cols[4]: weight,
        }

        entry_df = pd.DataFrame([entry])
        df = pd.concat([df, entry_df], ignore_index=True)

    return df


def check_df_types(df):
    assert is_string_dtype(df[cols[0]]), f"{cols[0]} is not of type string"
    assert is_string_dtype(df[cols[1]]), f"{cols[1]} is not of type string"
    assert is_numeric_dtype(df[cols[2]]), f"{cols[2]} is not numeric"
    assert is_numeric_dtype(df[cols[3]]), f"{cols[3]} is not numeric"
    assert is_numeric_dtype(df[cols[4]]), f"{cols[4]} is not numeric"


# Function to clean and convert the values
def clean_float_str(value):
    value = value.replace(",", "")  # Remove commas
    if re.match(r"^\(.*\)$", value):  # Check if the value is in parentheses
        value = "-" + value.strip("()")  # Remove parentheses and prepend '-'
    value = value.replace("–", "0")
    return float(value)
