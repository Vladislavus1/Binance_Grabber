from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument(f"user-agent={headers['User-Agent']}")
options.add_argument(f"accept-language={headers['Accept-Language']}")

driver = webdriver.Chrome(service=service, options=options)