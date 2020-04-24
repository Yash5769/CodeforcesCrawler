import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime,timezone,timedelta
from dateutil import tz
import pytz
import time
import django.utils.timezone as dt
from .models import time_table

def get_rating(handle):
    page = requests.get("https://codeforces.com/profile/" + handle)
    soup = BeautifulSoup(page.content, 'html.parser')
    info = soup.find('div', class_='info')
    rating = info.find_all('span')
    p = list(rating[1].children)
    return (p[0])
    
def get_contests(handle):
    page = requests.get("https://codeforces.com/contests/with/" + handle)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find_all('table', class_="tablesorter user-contests-table")[0]
    tbody = content.find('tbody')
    rows = tbody.find_all('tr')
    first = rows[0].find_all('td')
    num_contest = first[0].text
    best_rank = int(first[2].find('a').text)
    worst_rank = int(first[2].find('a').text)
    maxup = int(first[4].find('span').text)
    maxdown = int(first[4].find('span').text)
    for row in rows:
        elements = row.find_all('td')
        rank = int(elements[2].find('a').text)
        delta = int(elements[4].find('span').text)
        best_rank = best_rank if best_rank<rank else rank
        worst_rank = worst_rank if worst_rank > rank else rank
        maxup = maxup if maxup > delta else delta
        maxdown = maxdown if maxdown < delta else delta
    values = {"Number of contests":num_contest,"Max Up": maxup,"Max Down":maxdown,"Best Rank":best_rank,"Worst Rank":worst_rank}
    return values

def get_timetable():
    time_table.objects.all().delete()
    page = requests.get("https://codeforces.com/contests")
    soup = BeautifulSoup(page.content, "html.parser")
    datatable = soup.find('div', class_="datatable")
    rows = datatable.find_all('tr')
    del rows[0]
    for row in rows:
        elements = row.find_all('td')
        name = elements[0].text
        writers = elements[1].text
        d = (elements[2].text.strip()+" +0300")
        date = datetime.strptime(d, "%b/%d/%Y %H:%M %z")
        date = date.astimezone(tz.UTC)
        a = time_table.objects.update_or_create(name = name, writers = writers, time = date)[0]
        print(a.time)
        a.save()

