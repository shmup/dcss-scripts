#!/usr/bin/env python3
# usage: ./dcss-tournaments.py > out.txt
# output dates of all tournaments

from bs4 import BeautifulSoup
import urllib.request
import arrow
import datetime

LATEST = 18


def url(version):
    return "http://dobrazupa.org/tournament/0.{}/overview.html".format(version)

output = ''

for x in range(12, LATEST + 1):
    page = urllib.request.urlopen(url(x))
    soup= BeautifulSoup(page.read(), "html.parser")
    links = soup.find(class_='fineprint').find_all('a', href=True)
    isos = [x['href'].split('=')[1] for x in links]
    dates = [arrow.get(datetime.datetime.strptime(i, "20%y%m%dT%H")).format('YYYY-MM-DD') for i in isos]
    output = "v0.{} > {} to {}\r\n".format(x, dates[0], dates[1]) + output

print(output)
