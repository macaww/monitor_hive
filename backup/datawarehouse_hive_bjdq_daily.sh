#!/bin/env bash

HOMEDIR=/usr/local/zabbix/etc/datawarehouse_hive
[ -d $HOMEDIR ] && cd $HOMEDIR || { mkdir -p $HOMEDIR;cd $HOMEDIR;}
source ./environment.sh
YESTERDAY=$(date +%Y-%m-%d --date '1 days ago')
HOUR=$(date +%H)
LOG=datawarehouse_hive_table_daily_run.log

sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_bjdq_ad_d.hql >> $LOG 2>/dev/null &
sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_bjdq_d.hql >> $LOG 2>/dev/null &
sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_bjdq_event_d.hql >> $LOG 2>/dev/null &
sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_bjdq_hdcarpk_d.hql >> $LOG 2>/dev/null &
sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_bjdq_pv_d.hql >> $LOG 2>/dev/null &
sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_bjdq_start_d.hql >> $LOG 2>/dev/null &
