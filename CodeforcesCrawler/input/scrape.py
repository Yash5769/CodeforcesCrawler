import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime,timezone,timedelta
from dateutil import tz
import pytz
import time
import django.utils.timezone as dt
from .models import time_table,languages,verdicts,level

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

# handle = "Yash57"
def get_submission(handle):
    languages.objects.all().delete()
    verdicts.objects.all().delete()
    level.objects.all().delete()
    page = requests.get("https://codeforces.com/submissions/" + handle)
    soup = BeautifulSoup(page.content,"html.parser")
    div = soup.find_all('div', class_='pagination')[1]
    ul = div.find('ul')
    li = ul.find_all('li')
    t = int(li[-2].text)
    val = pd.Series()
    ver = pd.Series()
    lvl = pd.Series()
    for i in range(t):
        p = pd.read_html("https://codeforces.com/submissions/" + handle + "/page/" + str(i + 1))
        table = p[5]
        table['Verdict'] = [x[:3] for x in table['Verdict']]
        table['Problem'] = [x[0] for x in table['Problem']]
        val = val.combine(table['Lang'].value_counts(), (lambda x1, x2: x1 + x2), fill_value=0)
        ver = ver.combine(table['Verdict'].value_counts(), (lambda x1, x2: x1 + x2), fill_value=0)
        lvl = lvl.combine(table['Problem'].value_counts(),(lambda x1, x2: x1+x2),fill_value =0)
    labels = val.index
    for l in labels:
        a = languages.objects.update_or_create(name = l,val = val[l])[0]
        a.save()
    labels = ver.index
    for l in labels:
        k = l
        a = verdicts.objects.update_or_create(name = k,val = ver[l])[0]
        a.save()
    labels = lvl.index
    for l in labels:
        k = l
        a = level.objects.update_or_create(name = k,val = lvl[l])[0]
        a.save()
