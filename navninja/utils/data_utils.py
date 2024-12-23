import requests
import hashlib


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
