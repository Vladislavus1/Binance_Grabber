from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import csv

from config import driver

base_url = "https://www.binance.com/markets/overview"


def get_info():
    try:
        current_cryptocurrencies = driver.find_elements(By.CSS_SELECTOR, "[direction='ltr']")
        for cryptocurrency in current_cryptocurrencies:
            short_title = cryptocurrency.find_element(By.CSS_SELECTOR, "[class*='subtitle3']").text
            long_title = cryptocurrency.find_element(By.CSS_SELECTOR, "[class*='line-clamp-1']").text
            values = cryptocurrency.find_elements(By.CSS_SELECTOR, "[data-area='right']")
            price = float(values[0].text.replace("$", "").replace(",", ""))
            capitalization = values[3].text.replace("$", "").replace(" ", "").replace(",", "")
            multiplier = 10 ** 3 if capitalization.endswith('K') else 10 ** 6 if capitalization.endswith(
                'M') else 10 ** 9 if capitalization.endswith('B') else capitalization
            capitalization = int(
                float(capitalization[:-1]) * multiplier) if multiplier != capitalization else capitalization
            writer.writerow(
                {"short_title": short_title, "long_title": long_title, "price": price,
                 "capitalization": capitalization})
    except StaleElementReferenceException:
        get_info()


try:
    driver.get(base_url)
    pagination_elements = driver.find_elements(By.CSS_SELECTOR, "[id*='page-']")
    max_page = int(pagination_elements[-1].text)
    with open("binance_trading_data.csv", "w", newline="", encoding="utf-8") as file:
        header = ["short_title", "long_title", "price", "capitalization"]
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for page_index in range(max_page):
            driver.get(base_url + f"?p={page_index+1}")
            cryptocurrencies = driver.find_elements(By.CSS_SELECTOR, "[direction='ltr']")
            get_info()
finally:
    driver.close()
    driver.quit()