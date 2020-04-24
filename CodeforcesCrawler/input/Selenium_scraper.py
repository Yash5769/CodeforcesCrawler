from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions as Options
from bs4 import BeautifulSoup
import requests
from dateutil import tz
from datetime import datetime
import pandas as pd
from .models import time_table

def get_rating(handle):
    opts = Options()
    opts.add_argument('--headless')
    assert opts.headless
    browser = Chrome(options=opts)
    browser.get('https://codeforces.com/profile/'+handle)
    info = browser.find_element_by_class_name('info')
    rating = info.find_element_by_xpath("//ul/li/span")
    return rating.text

def get_timetable():
    opts = Options()
    opts.add_argument('--headless')
    assert opts.headless
    browser = Chrome(options=opts)
    browser.get("https://codeforces.com/contests")
    info = browser.find_element_by_class_name('datatable')
    table = info.find_element_by_tag_name("table")
    tbody = table.find_element_by_tag_name("tbody")
    rows = table.find_elements_by_tag_name("tr")
    del rows[0]
    for row in rows:
        elements = row.find_elements_by_tag_name('td')
        name = elements[0].text
        writers = elements[1].text
        z = elements[2].find_element_by_tag_name('sup').text
        print(elements[2].text)
        d = elements[2].text.replace(z, '')
        d = d.strip()
        print(z)
        z = z.replace('UTC', '')
        z = float(z)
        z *= 60
        z = int(z)
        z = str((z // 60)).zfill(2) + str(z % 60)
        print(d)
        date = datetime.strptime(d, "%b/%d/%Y %H:%M")
        date = date.astimezone(tz.UTC)
        a = time_table.objects.update_or_create(name = name, writers = writers, time = date)[0]
        print(a.time)
        a.save()