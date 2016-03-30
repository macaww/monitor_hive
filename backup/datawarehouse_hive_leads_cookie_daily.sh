#!/bin/env bash

HOMEDIR=/usr/local/zabbix/etc/datawarehouse_hive
[ -d $HOMEDIR ] && cd $HOMEDIR || { mkdir -p $HOMEDIR;cd $HOMEDIR;}
source ./environment.sh
YESTERDAY=$(date +%Y-%m-%d --date '1 days ago')
HOUR=$(date +%H)
LOG=datawarehouse_hive_table_daily_run.log

sh datawarehouse_hive_table_daily.sh leads_cookie/leads_mobile.hql >> $LOG 2>/dev/null &
sh datawarehouse_hive_table_daily.sh leads_cookie/leads_map.hql >> $LOG 2>/dev/null &
sh datawarehouse_hive_table_daily.sh leads_cookie/leads.hql >> $LOG 2>/dev/null &
sh datawarehouse_hive_table_daily.sh leads_cookie/cookie_map.hql >> $LOG 2>/dev/null &
sh datawarehouse_hive_table_daily.sh leads_cookie/cookie_merge.hql >> $LOG 2>/dev/null &

