#!/bin/env bash

HOMEDIR=$(dirname $(readlink -f $0))
cd $HOMEDIR
source ./environment.sh
HOUR=$(date +%H)
LOG=datawarehouse_hive_table_daily_run.log

if [ $HOUR -eq 05 ]
then
    sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_bjdq_ad_d.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_bjdq_d.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_bjdq_event_d.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_bjdq_hdcarpk_d.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_bjdq_pv_d.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_bjdq_start_d.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_yiche_article_d.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_yiche_d.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_yiche_info_d.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh mobile_dw/stage_mobile_yiche_type_d.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh auto2/tool_price_day.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh usercenter_dw/stage_tags_zamplus.hql >> $LOG 2>/dev/null &
elif [ $HOUR -eq 07 ]
then
    sh datawarehouse_hive_table_daily.sh cig_dw/ods_bitauto_website_d_pc.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh cig_dw/ods_bitauto_website_d_mobile.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh leads_cookie/leads_mobile.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh leads_cookie/leads_map.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh leads_cookie/leads.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh leads_cookie/cookie_map.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh leads_cookie/cookie_merge.hql >> $LOG 2>/dev/null &
elif [ $HOUR -eq 00 ]
then
    sh datawarehouse_hive_table_daily.sh auto2/tool_model_info_day.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh auto2/tool_style_info_day.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh auto2/tool_ad_meterial_info_day.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh auto2/tool_ad_place_info_day.hql >> $LOG 2>/dev/null &
    sh datawarehouse_hive_table_daily.sh auto2/tool_shangpainum_month.hql >> $LOG 2>/dev/null &
elif [ $HOUR -eq 08 ]    
then
    #python mail_report.py > mail_$$
    #send_mail "[report] zabbix check table" "mail_$$"
    python2.6 mail_report_html_internel.py  > mail_$$
    send_mail_html mail_$$
    python2.6 mail_report_html_externel.py  > mail_$$
    send_mail_html_ex mail_$$
    rm -f mail_$$
fi

