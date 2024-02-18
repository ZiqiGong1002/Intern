import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import requests
from bs4 import BeautifulSoup
def currency_code_translation(input_currency_code):
    currency_code_url="https://www.11meigui.com/tools/currency"
    response = requests.get(currency_code_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for heading in soup.find_all('tr'):
            cells = heading.find_all('td')
            if len(cells) > 4 and cells[4].get_text(strip=True)==input_currency_code:
                currency_code=cells[1].get_text(strip=True)
                return currency_code

#use driver and get url
driver_path = "G:\Internship\geckodriver-v0.34.0-win32\geckodriver.exe"
service = Service(executable_path=driver_path)
driver = webdriver.Firefox(service=service)
driver.get("https://www.boc.cn/sourcedb/whpj/")
#input the restriction
if len(sys.argv) < 2:
        print("需要两个参数")
        sys.exit()
input_date=sys.argv[1]
date = input_date[:4]+"-"+input_date[4:6]+"-"+input_date[6:]
input_currency_code=sys.argv[2]
currency_code =currency_code_translation(input_currency_code)
#wait time
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//th[text()='发布日期']"))
)

rate_table = driver.find_element(By.XPATH, "//table[.//th[text()='发布日期']]")
rows = driver.find_elements(By.XPATH, f"//tr[td[@class='pjrq'][starts-with(text(), '{date}')]]")

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if currency_code in row.text:
            selling_rate=cols[3].text
            with open("result.txt", "a") as file:
                file.write(selling_rate)
            print(selling_rate)
            break
else:
    print(f"No data found for {input_currency_code} on {input_date}")
driver.quit()


