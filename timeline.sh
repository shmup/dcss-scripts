#!/usr/bin/env bash
# usage: ./timeline.sh > out.txt

{
    cd ~/code/crawl
    git pull
} &> /dev/null

echo DCSS tags generated on $(date "+%Y-%m-%d %H:%M:%S")
echo 

git log --date-order --graph --tags --simplify-by-decoration --pretty=format:'%ai %h %d'
