from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions as Options
from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_rating(handle):
    opts = Options()
    opts.add_argument('--headless')
    assert opts.headless
    browser = Chrome(options=opts)
    browser.get('https://codeforces.com/profile/'+handle)
    info = browser.find_element_by_class_name('info')
    rating = info.find_element_by_xpath("//ul/li/span")
    return rating.text

# def get_contest(handle):
handle = 'Yash57'
page = requests.get("https://codeforces.com/contests/with/" + handle)
soup = BeautifulSoup(page.content, 'html.parser')
content = soup.find('table')
df = pd.read_html(str(content))
print(df)
# def get_contest_info(handle):
# print(rating.text)