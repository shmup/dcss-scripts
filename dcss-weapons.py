#!/usr/bin/env python3
# usage: ./dcss-weapons.py > out.txt
# an attempt to automate http://crawl.chaosforge.org/Weapon_speed

import json
import math
import re
import sys
import datetime
import urllib.request

fight = 'https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/fight.cc'
itemprop = 'https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/itemprop.cc'

# result = urllib.request.urlopen(itemprop).read()
# data = json.loads(result.decode())

fff = 'C:\\Users\\jared.miller\\code\\crawl\\crawl-ref\\source\\itemprop.cc'

f = open(fff, 'r')

weapon_section = False
regex = re.compile('[^a-zA-Z ]')

for line in f:
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
        damage, hit, base_delay = parts[2:5]
    # find weapon sizes
    if re.match('.*SIZE_.*SIZE_', line):
        parts = [x.strip() for x in line.split(',')]
        double_hand, single_hand = parts[1:3]
        print("{} => {} => {} => {}".format(title, [damage, hit, base_delay], single_hand, double_hand))
