#!/bin/bash
if [ "$1" = "" ]; then
start_date=`date -d "-0 day" +%Y-%m-%d`
else
start_date=`date -d "$1" +%Y-%m-%d`
fi

cd /opt/bishe


if [ $? -ne 0 ];then
    exit 255
fi

python3 /opt/bishe/spider_plus.py
if [ $? -ne 0 ];then
    exit 255
fi


git add --all

git commit -m "推送文件备份"

git push -u origin --all


if [ $? -ne 0 ];then
    exit 255
fi





