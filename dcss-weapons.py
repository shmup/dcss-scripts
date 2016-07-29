#!/usr/bin/env python3
# usage: ./dcss-weapons.py > out.txt
# an attempt to automate http://crawl.chaosforge.org/Weapon_speed

import json
import math
import re
import sys
import datetime
import urllib.request
from terminaltables import AsciiTable

fight = 'https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/fight.cc'

itemprop = 'https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/itemprop.cc'
table_title = 'DCSS weapon min delay'

# itemprop = 'https://raw.githubusercontent.com/crawl/crawl/stone_soup-0.18/crawl-ref/source/itemprop.cc'
# table_title = 'DCSS 0.18 weapon min delay'

result = urllib.request.urlopen(itemprop)

def parse_1h_size(size):
    if 'num' in size[:3].lower():
        return ''
    return size.split('_')[1].lower()

def parse_2h_size(size, one_hand, weapon_type):
    if one_hand == '' or 'stave' in weapon_type.lower():
        return size.split('_')[1].lower()
    return ''

def calc_min_delay(base_delay, weapon=''):
    min_delay = int(base_delay) / 2
    weapon = weapon.lower()

    if weapon == 'sk_short_blades' and min_delay > 5:
        min_delay = 5

    if weapon == 'sk_crossbows' and min_delay < 10:
        min_delay = 10

    if min_delay > 7:
        min_delay = 7

    if min_delay < 3:
        min_delay = 3

    return str(math.floor(min_delay))

def calc_skill_required(base_delay, min_delay):
    return str((int(base_delay) - int(min_delay)) * 2)

weapon_section = False
regex = re.compile('[^a-zA-Z ]')
header = ['Name', 'Damage', 'Hit', 'Base Delay', 'Min Delay', 'Skill Required', 'Min 2H Size']
table_data = []

for line in result:
    line = line.decode()
    # wait till we're in the weapons section
    if not weapon_section:
        if re.match('.*static const weapon_def Weapon_prop.*', line):
            weapon_section = True
        continue
    # find weapon stats
    if re.match('.*{ WPN_', line):
        parts = [x.strip() for x in line.split(',')]
        enum = re.sub('[^a-zA-Z_]', '', parts[0]).strip()
        title = re.sub('[\'"]', '', parts[1]).strip()
        # if title == 'demon blade':
        #     break
        damage, hit, base_delay = parts[2:5]

    # find weapon sizes
    if re.match('.*SIZE_.*SIZE_', line):
        # skip long gone items
        if 'old ' in title[0:4]:
            continue
        parts = [x.strip() for x in line.split(',')]
        double_hand, single_hand = parts[1:3]
        min_delay = calc_min_delay(base_delay)
        skill_required = calc_skill_required(base_delay, min_delay)
        th = parse_2h_size(double_hand, parse_1h_size(single_hand), parts[0])
        table_data.append([title, damage, hit, base_delay, min_delay, skill_required, th])

# table_data = sorted(table_data, key=lambda x: x[0])
table_data.insert(0, header)
table_data.append(header)

table = AsciiTable(table_data)
table.title = table_title
table.inner_footing_row_border = True
table.justify_columns[1] = 'right'
table.justify_columns[2] = 'right'
table.justify_columns[3] = 'right'
table.justify_columns[4] = 'right'
table.justify_columns[5] = 'right'

print(table.table)
print('\r')
print('Last generated on {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
