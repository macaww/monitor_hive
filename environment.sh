#!/bin/env bash
export PATH=$PATH:/usr/sbin

MAIL_LIST="wangliang7 xiangr huangwl zhangxinpeng3 chenweiqiang guodl zhangxiongfei yanw pengcz mingrui1 chehy dut"
MAIL_LIST_EX="wangliang7 xiangr huangwl zhangxinpeng3 chenweiqiang guodl zhangxiongfei yanw pengcz mingrui1 chehy dut yangjin1 wanghongxia"

send_mail () {
    if [ $# -ne 2 ]
    then
        echo "usage: $0 [mail subject] [mail content|mail content file]"
        return 1
    fi
    mail_subject="$1"
    mail_content="$2"
    for receiver in $MAIL_LIST
    do  
        if [ -f "${mail_content}" ]
        then
            mail -s "${mail_subject}" ${receiver}@yiche.com < "${mail_content}"
        else
            echo "${mail_content}" | mail -s "${mail_subject}" ${receiver}@yiche.com
        fi
    done
}

send_mail_html () {

    if [ $# -ne 1 -o ! -f "$1" ]
    then
        echo "usage: $0 [mail html content file]"
        return 1
    fi

    local mail_content="$1"
    for receiver in $MAIL_LIST
    do  
        sendmail ${receiver}@yiche.com < "${mail_content}"
    done
}

send_mail_html_ex () {

    if [ $# -ne 1 -o ! -f "$1" ]
    then
        echo "usage: $0 [mail html content file]"
        return 1
    fi

    local mail_content="$1"
    for receiver in $MAIL_LIST_EX
    do  
        sendmail ${receiver}@yiche.com < "${mail_content}"
    done
}
