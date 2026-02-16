#!/usr/bin/env python3

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://www.lse.co.uk/profiles/peoplepower1/?page=1"
OUTPUT_FILE = "page1.html"

driver = webdriver.Chrome()

try:
    driver.get(URL)

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Accept All']")
            )
        ).click()
    except Exception:
        pass

    time.sleep(5)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
finally:
    driver.quit()

print(f"Saved HTML to {OUTPUT_FILE}")
