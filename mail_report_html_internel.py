#!/usr/bin/env python2.6
# coding: utf-8
import sys
import datetime
from Cheetah.Template import Template
from report_internel import report_internel

LOG_PATH = 'datawarehouse_hive_table_daily_run.log'

today = str(datetime.date.today())
Day1ago = str(datetime.date.today() - datetime.timedelta(days=1))
Day2ago = str(datetime.date.today() - datetime.timedelta(days=2))
Day3ago = str(datetime.date.today() - datetime.timedelta(days=3))
Day4ago = str(datetime.date.today() - datetime.timedelta(days=4))
Day5ago = str(datetime.date.today() - datetime.timedelta(days=5))
Day6ago = str(datetime.date.today() - datetime.timedelta(days=6))
Day7ago = str(datetime.date.today() - datetime.timedelta(days=7))


def comma_div(num):
    if num is None:
        return num
    num = str(num)
    if len(num) <= 3:
        return num
    ret = ''
    for i in range((len(num) - 1) / 3 + 1):
        if i is 0:
            ret = num[-3:]
        else:
            ret = num[(-3 * i - 3):(-3 * i)] + ',' + ret
    return ret


log_object = open(LOG_PATH)
# 定义所有表的一个数组
table_name = ["cig_dw.ods_bitauto_website_d_pc", "cig_dw.ods_bitauto_website_d_mobile",
              "auto2.tool_model_info_day", "auto2.tool_price_day", "auto2.tool_style_info_day",
              "auto2.tool_ad_meterial_info_day","auto2.tool_ad_place_info_day","auto2.tool_shangpainum_month",
              "mobile_dw.stage_mobile_bjdq_hdcarpk_d", "mobile_dw.stage_mobile_bjdq_event_d",
              "mobile_dw.stage_mobile_bjdq_start_d", "mobile_dw.stage_mobile_bjdq_ad_d",
              "mobile_dw.stage_mobile_bjdq_pv_d", "mobile_dw.stage_mobile_bjdq_d",
              "leads_cookie.leads", "leads_cookie.leads_mobile", "leads_cookie.cookie_map",
              "leads_cookie.cookie_merge", "leads_cookie.leads_map",
              "mobile_dw.stage_mobile_yiche_d","mobile_dw.stage_mobile_yiche_info_d", "mobile_dw.stage_mobile_yiche_type_d",
              "usercenter_dw.stage_tags_zamplus"]
week = [Day1ago, Day2ago, Day3ago, Day4ago, Day5ago, Day6ago, Day7ago]

# day
sum_table = {}
average_table = {}
count_table = {}
error_table = {}
# week
none_table_array = {}
error_table_array = {}
# month
month_days_status = {}

# 从日志读入数据
for line in log_object:
    line = line.strip()
    words = line.split(" ")
    # 只读取了3个字段正常的输出，没读size空的，或者整条为空的
    if len(words) is 3:
        log_date = words[0]
        log_name = words[1]
        log_size = words[2]
    if log_name in table_name:
        # 初始化 count二维字典
        if log_name not in count_table:
            count_table[log_name] = {}
        # 初始化 error二维字典
        if log_name not in error_table:
            error_table[log_name] = {}
        count_table[log_name][log_date] = int(log_size)

# 遍历已经录入的表和日期，执行各类统计策略
for log_name_key in count_table:
    # 计算总数和平均数
    sum_table[log_name_key] = sum(count_table[log_name_key].values())
    average_table[log_name_key] = sum_table[log_name_key] / len(count_table[log_name_key])
    # 如果过去一周的获取失败，count补为空，便于显示，再多了不补，一周外的必须提前补完。
    for log_date_key in week:
        if count_table[log_name_key].get(log_date_key) is None:
            count_table[log_name_key][log_date_key] = None
    # 遍历所有存在的日期，判断异常的,和错误的
    for log_date_key in count_table[log_name_key]:
        if count_table[log_name_key][log_date_key] == 0 or count_table[log_name_key][log_date_key] is None:
            error_table[log_name_key][log_date_key] = "错误"
            if log_date_key not in none_table_array:
                none_table_array[log_date_key] = log_name_key
            else:
                none_table_array[log_date_key] = none_table_array[log_date_key] + "," + log_name_key
        elif count_table[log_name_key][log_date_key] < int(average_table[log_name_key] * 0.6):
            error_table[log_name_key][log_date_key] = "异常"
            if log_date_key not in error_table_array:
                error_table_array[log_date_key] = log_name_key
            else:
                error_table_array[log_date_key] = error_table_array[log_date_key] + "," + log_name_key
        else:
            error_table[log_name_key][log_date_key] = "正常"
# 如果错误和异常数组表内无值，表示正常
for log_date_key in week:
    if none_table_array.get(log_date_key) is None:
        none_table_array[log_date_key] = "正常"
    if error_table_array.get(log_date_key) is None:
        error_table_array[log_date_key] = "正常"
# 总结上面的值，生成month状态
for log_name_key in error_table:
    for log_date_key in error_table[log_name_key]:
        if error_table[log_name_key][log_date_key] is "异常":
            month_days_status[log_date_key] = "异常"
for log_name_key in error_table:
    for log_date_key in error_table[log_name_key]:
        if error_table[log_name_key][log_date_key] is "错误":
            month_days_status[log_date_key] = "错误"
for day_key in range(1, 36):
    dayago = str(datetime.date.today() - datetime.timedelta(days=day_key))
    if month_days_status.get(dayago) is None:
        month_days_status[dayago] = "正常"
    month_days_status["month_date" + str(day_key)] = dayago + " " + month_days_status[dayago]

# ('+-----------------------------------------+------------------+------------------+------+')
# ('|                  库.表                  |   昨天入库值     |      平均值      | 状态 |')
# ('+-----------------------------------------+------------------+------------------+------+')
print report_internel(searchList=[
    {'title': "数据仓库接入（内部）报告(" + Day1ago + ")", 'title_week': "最近一周", 'title_month': "最近一个月", 'database': "库.表",
     'yesterday': "昨日入库值", 'average': "平均值", 'status': "状态", 'explain': "库表含义",'none_data_table':"无数据表",'error_data_table':"异常数据表"},
    {'cig_dw_ods_bitauto_website_d_pc': "cig_dw.ods_bitauto_website_d_pc",
     'cig_dw_ods_bitauto_website_d_pc_yesterday': count_table["cig_dw.ods_bitauto_website_d_pc"][Day1ago],
     'cig_dw_ods_bitauto_website_d_pc_average': average_table["cig_dw.ods_bitauto_website_d_pc"],
     'cig_dw_ods_bitauto_website_d_pc_error': error_table["cig_dw.ods_bitauto_website_d_pc"][Day1ago],
     'cig_dw_ods_bitauto_website_d_pc_explain': "易车网PC端日志数据"},
    {'cig_dw_ods_bitauto_website_d_mobile': "cig_dw.ods_bitauto_website_d_mobile",
     'cig_dw_ods_bitauto_website_d_mobile_yesterday': count_table["cig_dw.ods_bitauto_website_d_mobile"][Day1ago],
     'cig_dw_ods_bitauto_website_d_mobile_average': average_table["cig_dw.ods_bitauto_website_d_mobile"],
     'cig_dw_ods_bitauto_website_d_mobile_error': error_table["cig_dw.ods_bitauto_website_d_mobile"][Day1ago],
     'cig_dw_ods_bitauto_website_d_mobile_explain': "易车网移动端日志数据（WAP）"},
    {'auto2_tool_ad_meterial_info_day': "auto2.tool_ad_meterial_info_day",
     'auto2_tool_ad_meterial_info_day_yesterday': count_table["auto2.tool_ad_meterial_info_day"][Day1ago],
     'auto2_tool_ad_meterial_info_day_average': average_table["auto2.tool_ad_meterial_info_day"],
     'auto2_tool_ad_meterial_info_day_error': error_table["auto2.tool_ad_meterial_info_day"][Day1ago],
     'auto2_tool_ad_meterial_info_day_explain': "广告物料信息数据"},
    {'auto2_tool_ad_place_info_day': "auto2.tool_ad_place_info_day",
     'auto2_tool_ad_place_info_day_yesterday': count_table["auto2.tool_ad_place_info_day"][Day1ago],
     'auto2_tool_ad_place_info_day_average': average_table["auto2.tool_ad_place_info_day"],
     'auto2_tool_ad_place_info_day_error': error_table["auto2.tool_ad_place_info_day"][Day1ago],
     'auto2_tool_ad_place_info_day_explain': "广告位信息数据"},
    {'auto2_tool_model_info_day': "auto2.tool_model_info_day",
     'auto2_tool_model_info_day_yesterday': count_table["auto2.tool_model_info_day"][Day1ago],
     'auto2_tool_model_info_day_average': average_table["auto2.tool_model_info_day"],
     'auto2_tool_model_info_day_error': error_table["auto2.tool_model_info_day"][Day1ago],
     'auto2_tool_model_info_day_explain': "车型信息数据"},
    {'auto2_tool_price_day': "auto2.tool_price_day",
     'auto2_tool_price_day_yesterday': count_table["auto2.tool_price_day"][Day1ago],
     'auto2_tool_price_day_average': average_table["auto2.tool_price_day"],
     'auto2_tool_price_day_error': error_table["auto2.tool_price_day"][Day1ago],
     'auto2_tool_price_day_explain': "车型售价信息数据"},
    {'auto2_tool_style_info_day': "auto2.tool_style_info_day",
     'auto2_tool_style_info_day_yesterday': count_table["auto2.tool_style_info_day"][Day1ago],
     'auto2_tool_style_info_day_average': average_table["auto2.tool_style_info_day"],
     'auto2_tool_style_info_day_error': error_table["auto2.tool_style_info_day"][Day1ago],
     'auto2_tool_style_info_day_explain': "车款信息数据"},
    {'auto2_tool_shangpainum_month': "auto2.tool_shangpainum_month",
     'auto2_tool_shangpainum_month_yesterday': count_table["auto2.tool_shangpainum_month"][Day1ago],
     'auto2_tool_shangpainum_month_average': average_table["auto2.tool_shangpainum_month"],
     'auto2_tool_shangpainum_month_error': error_table["auto2.tool_shangpainum_month"][Day1ago],
     'auto2_tool_shangpainum_month_explain': "上牌信息数据"},
    {'mobile_dw_stage_mobile_bjdq_hdcarpk_d': "mobile_dw.stage_mobile_bjdq_hdcarpk_d",
     'mobile_dw_stage_mobile_bjdq_hdcarpk_d_yesterday': count_table["mobile_dw.stage_mobile_bjdq_hdcarpk_d"][Day1ago],
     'mobile_dw_stage_mobile_bjdq_hdcarpk_d_average': average_table["mobile_dw.stage_mobile_bjdq_hdcarpk_d"],
     'mobile_dw_stage_mobile_bjdq_hdcarpk_d_error': error_table["mobile_dw.stage_mobile_bjdq_hdcarpk_d"][Day1ago],
     'mobile_dw_stage_mobile_bjdq_hdcarpk_d_explain': "报价大全车型对比日志"},
    {'mobile_dw_stage_mobile_bjdq_event_d': "mobile_dw.stage_mobile_bjdq_event_d",
     'mobile_dw_stage_mobile_bjdq_event_d_yesterday': count_table["mobile_dw.stage_mobile_bjdq_event_d"][Day1ago],
     'mobile_dw_stage_mobile_bjdq_event_d_average': average_table["mobile_dw.stage_mobile_bjdq_event_d"],
     'mobile_dw_stage_mobile_bjdq_event_d_error': error_table["mobile_dw.stage_mobile_bjdq_event_d"][Day1ago],
     'mobile_dw_stage_mobile_bjdq_event_d_explain': "报价大全事件日志"},
    {'mobile_dw_stage_mobile_bjdq_start_d': "mobile_dw.stage_mobile_bjdq_start_d",
     'mobile_dw_stage_mobile_bjdq_start_d_yesterday': count_table["mobile_dw.stage_mobile_bjdq_start_d"][Day1ago],
     'mobile_dw_stage_mobile_bjdq_start_d_average': average_table["mobile_dw.stage_mobile_bjdq_start_d"],
     'mobile_dw_stage_mobile_bjdq_start_d_error': error_table["mobile_dw.stage_mobile_bjdq_start_d"][Day1ago],
     'mobile_dw_stage_mobile_bjdq_start_d_explain': "报价大全启动日志"},
    {'mobile_dw_stage_mobile_bjdq_ad_d': "mobile_dw.stage_mobile_bjdq_ad_d",
     'mobile_dw_stage_mobile_bjdq_ad_d_yesterday': count_table["mobile_dw.stage_mobile_bjdq_ad_d"][Day1ago],
     'mobile_dw_stage_mobile_bjdq_ad_d_average': average_table["mobile_dw.stage_mobile_bjdq_ad_d"],
     'mobile_dw_stage_mobile_bjdq_ad_d_error': error_table["mobile_dw.stage_mobile_bjdq_ad_d"][Day1ago],
     'mobile_dw_stage_mobile_bjdq_ad_d_explain': "报价大全广告日志"},
    {'mobile_dw_stage_mobile_bjdq_pv_d': "mobile_dw.stage_mobile_bjdq_pv_d",
     'mobile_dw_stage_mobile_bjdq_pv_d_yesterday': count_table["mobile_dw.stage_mobile_bjdq_pv_d"][Day1ago],
     'mobile_dw_stage_mobile_bjdq_pv_d_average': average_table["mobile_dw.stage_mobile_bjdq_pv_d"],
     'mobile_dw_stage_mobile_bjdq_pv_d_error': error_table["mobile_dw.stage_mobile_bjdq_pv_d"][Day1ago],
     'mobile_dw_stage_mobile_bjdq_pv_d_explain': "报价大全页面访问日志"},
    {'mobile_dw_stage_mobile_bjdq_d': "mobile_dw.stage_mobile_bjdq_d",
     'mobile_dw_stage_mobile_bjdq_d_yesterday': count_table["mobile_dw.stage_mobile_bjdq_d"][Day1ago],
     'mobile_dw_stage_mobile_bjdq_d_average': average_table["mobile_dw.stage_mobile_bjdq_d"],
     'mobile_dw_stage_mobile_bjdq_d_error': error_table["mobile_dw.stage_mobile_bjdq_d"][Day1ago],
     'mobile_dw_stage_mobile_bjdq_d_explain': "报价大全全量日志数据"},
    {'leads_cookie_leads': "leads_cookie.leads",
     'leads_cookie_leads_yesterday': count_table["leads_cookie.leads"][Day1ago],
     'leads_cookie_leads_average': average_table["leads_cookie.leads"],
     'leads_cookie_leads_error': error_table["leads_cookie.leads"][Day1ago],
     'leads_cookie_leads_explain': "PC端线索数据"},
    {'leads_cookie_leads_mobile': "leads_cookie.leads_mobile",
     'leads_cookie_leads_mobile_yesterday': count_table["leads_cookie.leads_mobile"][Day1ago],
     'leads_cookie_leads_mobile_average': average_table["leads_cookie.leads_mobile"],
     'leads_cookie_leads_mobile_error': error_table["leads_cookie.leads_mobile"][Day1ago],
     'leads_cookie_leads_mobile_explain': "移动端线索数据"},
    {'leads_cookie_cookie_map': "leads_cookie.cookie_map",
     'leads_cookie_cookie_map_yesterday': count_table["leads_cookie.cookie_map"][Day1ago],
     'leads_cookie_cookie_map_average': average_table["leads_cookie.cookie_map"],
     'leads_cookie_cookie_map_error': error_table["leads_cookie.cookie_map"][Day1ago],
     'leads_cookie_cookie_map_explain': "cookies映射数据（用户中心和网站cookies的映射数据）"},
    {'leads_cookie_cookie_merge': "leads_cookie.cookie_merge",
     'leads_cookie_cookie_merge_yesterday': count_table["leads_cookie.cookie_merge"][Day1ago],
     'leads_cookie_cookie_merge_average': average_table["leads_cookie.cookie_merge"],
     'leads_cookie_cookie_merge_error': error_table["leads_cookie.cookie_merge"][Day1ago],
     'leads_cookie_cookie_merge_explain': "cookies映射取唯一"},
    {'leads_cookie_leads_map': "leads_cookie.leads_map",
     'leads_cookie_leads_map_yesterday': count_table["leads_cookie.leads_map"][Day1ago],
     'leads_cookie_leads_map_average': average_table["leads_cookie.leads_map"],
     'leads_cookie_leads_map_error': error_table["leads_cookie.leads_map"][Day1ago],
     'leads_cookie_leads_map_explain': "线索和cookies的映射"},
    # {'mobile_dw_stage_mobile_yiche_article_d': "mobile_dw.stage_mobile_yiche_article_d",
    #  'mobile_dw_stage_mobile_yiche_article_d_yesterday': count_table["mobile_dw.stage_mobile_yiche_article_d"][Day1ago],
    #  'mobile_dw_stage_mobile_yiche_article_d_average': average_table["mobile_dw.stage_mobile_yiche_article_d"],
    #  'mobile_dw_stage_mobile_yiche_article_d_error': error_table["mobile_dw.stage_mobile_yiche_article_d"][Day1ago],
    #  'mobile_dw_stage_mobile_yiche_article_d_explain': "易车app文章表"},
    {'mobile_dw_stage_mobile_yiche_d': "mobile_dw.stage_mobile_yiche_d",
     'mobile_dw_stage_mobile_yiche_d_yesterday': count_table["mobile_dw.stage_mobile_yiche_d"][Day1ago],
     'mobile_dw_stage_mobile_yiche_d_average': average_table["mobile_dw.stage_mobile_yiche_d"],
     'mobile_dw_stage_mobile_yiche_d_error': error_table["mobile_dw.stage_mobile_yiche_d"][Day1ago],
     'mobile_dw_stage_mobile_yiche_d_explain': "易车APP全量数据"},
    {'mobile_dw_stage_mobile_yiche_info_d': "mobile_dw.stage_mobile_yiche_info_d",
     'mobile_dw_stage_mobile_yiche_info_d_yesterday': count_table["mobile_dw.stage_mobile_yiche_info_d"][Day1ago],
     'mobile_dw_stage_mobile_yiche_info_d_average': average_table["mobile_dw.stage_mobile_yiche_info_d"],
     'mobile_dw_stage_mobile_yiche_info_d_error': error_table["mobile_dw.stage_mobile_yiche_info_d"][Day1ago],
     'mobile_dw_stage_mobile_yiche_info_d_explain': "易车app信息表"},
    {'mobile_dw_stage_mobile_yiche_type_d': "mobile_dw.stage_mobile_yiche_type_d",
     'mobile_dw_stage_mobile_yiche_type_d_yesterday': count_table["mobile_dw.stage_mobile_yiche_type_d"][Day1ago],
     'mobile_dw_stage_mobile_yiche_type_d_average': average_table["mobile_dw.stage_mobile_yiche_type_d"],
     'mobile_dw_stage_mobile_yiche_type_d_error': error_table["mobile_dw.stage_mobile_yiche_type_d"][Day1ago],
     'mobile_dw_stage_mobile_yiche_type_d_explain': "易车app类型表"},
    {'usercenter_dw_stage_tags_zamplus': "usercenter_dw.stage_tags_zamplus",
     'usercenter_dw_stage_tags_zamplus_yesterday': count_table["usercenter_dw.stage_tags_zamplus"][Day1ago],
     'usercenter_dw_stage_tags_zamplus_average': average_table["usercenter_dw.stage_tags_zamplus"],
     'usercenter_dw_stage_tags_zamplus_error': error_table["usercenter_dw.stage_tags_zamplus"][Day1ago],
     'usercenter_dw_stage_tags_zamplus_explain': "晶赞人群画像数据"},
    {'current_month_1date': Day1ago,
     'none_table_1date': none_table_array[Day1ago],
     'error_table_1date': error_table_array[Day1ago]},
    {'current_month_2date': Day2ago,
     'none_table_2date': none_table_array[Day2ago],
     'error_table_2date': error_table_array[Day2ago]},
    {'current_month_3date': Day3ago,
     'none_table_3date': none_table_array[Day3ago],
     'error_table_3date': error_table_array[Day3ago]},
    {'current_month_4date': Day4ago,
     'none_table_4date': none_table_array[Day4ago],
     'error_table_4date': error_table_array[Day4ago]},
    {'current_month_5date': Day5ago,
     'none_table_5date': none_table_array[Day5ago],
     'error_table_5date': error_table_array[Day5ago]},
    {'current_month_6date': Day6ago,
     'none_table_6date': none_table_array[Day6ago],
     'error_table_6date': error_table_array[Day6ago]},
    {'current_month_7date': Day7ago,
     'none_table_7date': none_table_array[Day7ago],
     'error_table_7date': error_table_array[Day7ago]},
    month_days_status,
])
