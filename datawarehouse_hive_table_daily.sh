#!/bin/env bash

source ./environment.sh
[ $# -ne 1 -o ! -f "$1" ] && { echo "usage: $0 [INPUT_HQL file]";exit;}
YESTERDAY=$(date +%Y-%m-%d --date '1 days ago')
TDB_YESTERDAY=$(date +%Y-%m-%d --date '2 days ago')
YESTERDAY1=$(date +%Y%m --date '1 days ago')
LAST3MONTH=$(date +%Y-%m --date '3 months ago')
hive_run_timeout=1200
hive_run_count=None
INPUT_HQL="$1"

#main

hive -S --hivevar YESTERDAY=${YESTERDAY} --hivevar YESTERDAY1=${YESTERDAY1} \
        --hivevar LAST3MONTH=${LAST3MONTH} --hivevar TDB_YESTERDAY=${TDB_YESTERDAY} -f $INPUT_HQL > hive_run_count_$$ &
hive_run_pid=$!

( sleep ${hive_run_timeout} && \
  kill -9 ${hive_run_pid}   && \
  send_mail "[error] zabbix check count" "$INPUT_HQL" && \
  rm -f hive_run_count_$$ ) &
watch_dog_pid=$!
watch_dog_ppid=$PPID

wait $hive_run_pid
wait_rev=$?

if [ "$wait_rev" -eq 0 ]
then
    watch_dog_pid_port=$(pstree -p $watch_dog_pid | egrep -o '[0-9]+')
    kill -9 $watch_dog_pid_port
else
    #echo "$INPUT_HQL check count failed"
    :
fi

# check result
hive_run_number_field=$(cat hive_run_count_$$| awk '{print NF}')
if [ "$hive_run_number_field" -eq 1 ]
then
    hive_run_count=$(cat hive_run_count_$$)
    INPUT_HQL=${INPUT_HQL%.hql}
    INPUT_HQL=${INPUT_HQL/\//\.}
    echo "$YESTERDAY ${INPUT_HQL} ${hive_run_count}"
elif [ "$hive_run_number_field" -eq 3 ]
then
    cat hive_run_count_$$ | awk '{print $1,$2,$3}'
fi

rm -f hive_run_count_$$