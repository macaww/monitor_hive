#!/usr/bin/env python
# coding: utf-8

SCRIPT_PATH = '/usr/local/zabbix/etc/datawarehouse_hive/'
LOG_PATH = SCRIPT_PATH + 'datawarehouse_hive_table_daily_run.log'
import sys, datetime

#mailList = parse_ini(SCRIPT_PATH + 'contacts.ini')
#contacts = mailList.get('mail', 'to')
#cc = mailList.get('mail', 'cc')
#subject_prefix = mailList.get('mail', 'subject_prefix')

Day1ago =  str(datetime.date.today() - datetime.timedelta(days=1))
today = str(datetime.date.today()) 
Day2ago =  str(datetime.date.today() - datetime.timedelta(days=2))
Day3ago =  str(datetime.date.today() - datetime.timedelta(days=3))
Day4ago =  str(datetime.date.today() - datetime.timedelta(days=4))
Day5ago =  str(datetime.date.today() - datetime.timedelta(days=5))
Day6ago =  str(datetime.date.today() - datetime.timedelta(days=6))
Day7ago =  str(datetime.date.today() - datetime.timedelta(days=7))

def commaDiv(num):
    if num is None:
        return num     
    num = str(num)
    if len(num) <= 3:
        return num
    ret = ''
    for i in range((len(num)-1)/3 + 1):
        if i is 0:
            ret = num[-3:]
        else:
            ret = num[(-3*i-3):(-3*i)] + ',' + ret
    return ret
    
def print_result(table):
    print ("|%-40s |%-17s |%-17s |%-8s|" % (table,commaDiv(count_table[table][Day1ago]),commaDiv(average_table[table]),error_table[table]))

log_object=open(LOG_PATH)
count_table={}
sum_table={}
average_table={}
error_table={}

for line in log_object:
    line = line.strip()
    words = line.split(" ")

    if len(words) is 3:
        log_date=words[0]
        log_name=words[1]
        log_size=words[2]
    if log_name not in count_table:
        count_table[log_name]={}
    if log_date not in count_table[log_name]:
        count_table[log_name][log_date]=int(log_size)

#for log_name_key,log_date_key in count_table.items():
for log_name_key in count_table:
    sum_table[log_name_key]=sum(count_table[log_name_key].values())
    average_table[log_name_key]=sum_table[log_name_key]/len(count_table[log_name_key])

    if count_table[log_name_key].get(Day1ago) is None:
        count_table[log_name_key][Day1ago]=None

    if count_table[log_name_key][Day1ago] > int(average_table[log_name_key]*0.7):
        error_table[log_name_key]="正确"
    else:
        error_table[log_name_key]="错误"

print ('+-----------------------------------------+------------------+------------------+------+')
print ('|                  库.表                  |   昨天入库值     |      平均值      | 状态 |')
print ('+-----------------------------------------+------------------+------------------+------+')
print_result("cig_dw.ods_bitauto_website_d_pc")
print_result("cig_dw.ods_bitauto_website_d_mobile")
print_result("auto2.tool_model_info_day")
print_result("auto2.tool_city_info")
print_result("auto2.tool_style_info_day")
print_result("mobile_dw.stage_mobile_bjdq_hdcarpk_d")
print_result("mobile_dw.stage_mobile_bjdq_event_d")
print_result("mobile_dw.stage_mobile_bjdq_start_d")
print_result("mobile_dw.stage_mobile_bjdq_ad_d")
print_result("mobile_dw.stage_mobile_bjdq_pv_d")
print_result("mobile_dw.stage_mobile_bjdq_d")
print_result("leads_cookie.leads")
print_result("leads_cookie.leads_mobile")
print_result("leads_cookie.cookie_map")
print_result("leads_cookie.cookie_merge")
print_result("leads_cookie.leads_map")
#print_result("mobile_dw.stage_mobile_yiche_article_d")
print_result("mobile_dw.stage_mobile_yiche_d")
print_result("mobile_dw.stage_mobile_yiche_info_d")
print_result("mobile_dw.stage_mobile_yiche_type_d")
print ('+-----------------------------------------+------------------+------------------+------+')
