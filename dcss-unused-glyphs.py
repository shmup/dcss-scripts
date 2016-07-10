#!/usr/bin/env python3
# usage: ./unused_monster_glyphs.py > out.txt

import urllib.request
import datetime
import re

monster_url = 'https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/mon-data.h'
monster_data = urllib.request.urlopen(monster_url)
used_glyphs = set()

for line in monster_data:
    line = line.decode()
    if re.match('\s+MONS_.*', line):
        parts = line.strip().split(',')
        used_glyphs.add(parts[1][2:-1])

ords = [ord(x) for x in used_glyphs]
ords.sort()


def find_missing(glyphs, start=None, limit=None):
    start = start if start is not None else glyphs[0]
    limit = limit if limit is not None else glyphs[-1]
    return [chr(i) for i in range(start, limit + 1) if i not in glyphs]

output = find_missing(ords, 48, 57) + find_missing(ords, 97, 122) + find_missing(ords, 65, 90)

print('Unused DCSS alphanumeric glyphs last generated on {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
print('\r\n' + ' '.join(output))
