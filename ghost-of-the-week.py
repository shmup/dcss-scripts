#!/usr/bin/env python3
# https://github.com/crawl/sequell/blob/master/docs/api.md
# usage: ./ghost_of_the_week.py > out.txt

import json
import math
import datetime
import urllib.request

term='https://loom.shalott.org/api/sequell/ldb?term='
learndb='https://loom.shalott.org/api/sequell/ldb?search='
listgame='https://loom.shalott.org/api/sequell/game?q='
query = '!lg * week !boring s=killer killer=~ghost'
params = '+'.join(query.split(' '))
result = urllib.request.urlopen(listgame + params).read()
data = json.loads(result.decode())

motd = """
                       _______           _______  _______ _________
                      (  ____ \\|\\     /|(  ___  )(  ____ \\\\__   __/
                      | (    \\/| )   ( || (   ) || (    \\/   ) (
                      | |      | (___) || |   | || (_____    | |
                      | | ____ |  ___  || |   | |(_____  )   | |
                      | | \\_  )| (   ) || |   | |      ) |   | |
                      | (___) || )   ( || (___) |/\\____) |   | |
                      (_______)|/     \\|(_______)\\_______)   )_(

 _______  _______   _________          _______             _______  _______  _
(  ___  )(  ____ \\  \\__   __/|\\     /|(  ____ \\  |\\     /|(  ____ \\(  ____ \\| \\    /\\
| (   ) || (    \\/     ) (   | )   ( || (    \\/  | )   ( || (    \\/| (    \\/|  \\  / /
| |   | || (__         | |   | (___) || (__      | | _ | || (__    | (__    |  (_/ /
| |   | ||  __)        | |   |  ___  ||  __)     | |( )| ||  __)   |  __)   |   _ (
| |   | || (           | |   | (   ) || (        | || || || (      | (      |  ( \\ \\
| (___) || )           | |   | )   ( || (____/\\  | () () || (____/\\| (____/\\|  /  \\ \\
(_______)|/            )_(   |/     \\|(_______/  (_______)(_______/(_______/|_/    \\/
"""

gotw = data['data'][0]

player = gotw[0].split("'")[0].strip()

congrats = "Congratulations " + player + "! " + str(gotw[1]) + " kills!"

motd += "\r\n\r\n\r\n\r\n"
motd += congrats.center(85, ' ')
motd += "\r\n\r\n"
motd += ('http://crawl.akrasiac.org/scoring/players/' + player + '.html').center(85, ' ')
motd += "\r\n\r\n"
motd += ('!lg * week !boring s=killer killer=~ghost').center(85, ' ')
motd += "\r\n\r\n"
motd += ('Generated on {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())).center(85, ' ')

print(motd)
