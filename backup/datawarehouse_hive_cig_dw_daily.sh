#!/bin/env bash

HOMEDIR=/usr/local/zabbix/etc/datawarehouse_hive
[ -d $HOMEDIR ] && cd $HOMEDIR || { mkdir -p $HOMEDIR;cd $HOMEDIR;}
source ./environment.sh
YESTERDAY=$(date +%Y-%m-%d --date '1 days ago')
HOUR=$(date +%H)
LOG=datawarehouse_hive_table_daily_run.log

sh datawarehouse_hive_table_daily.sh cig_dw/ods_bitauto_website_d_pc.hql >> $LOG 2>/dev/null &
sh datawarehouse_hive_table_daily.sh cig_dw/ods_bitauto_website_d_mobile.hql >> $LOG 2>/dev/null &

