#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:  常量，一些数据中的常量
# --------------------

# 学历
GRADE_NO = {
    0: u'小学',
    1: u'初中',
    2: u'高中',
    3: u'专科',
    4: u'本科',
    5: u'硕士',
    6: u'博士',
    7: u'博士后'
}

GRADE_NAME = {value: key for key, value in GRADE_NO.iteritems()}

# 性别
SEX_NAME = {
    0: u'男',
    1: u'女',
    2: u'未知'
}

SEX_NO = {value: key for key, value in SEX_NAME.iteritems()}

# 人员关系
RELATIONSHIP_NO = {
    1: u'兄',
    2: u'弟',
    3: u'姐',
    4: u'妹',
    5: u'父',
    6: u'母',
    7: u'丈',
    8: u'妻',
    9: u'朋',
}

RELATIONSHIP_NAME = {value: key for key, value in RELATIONSHIP_NO.iteritems()}

# 岗位
POSITION_NO = {
    1: u'Python开发',
    2: u'Web前端开发',
    3: u'手工测试',
    4: u'自动化测试',
    5: u'Java开发',
    6: u'C开发',
    7: u'C++开发',
    8: u'安全SE',
    9: u'PM',
}

POSITION_NAME = {value: key for key, value in POSITION_NO.iteritems()}