import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime


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
