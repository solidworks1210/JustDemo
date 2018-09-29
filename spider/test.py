# -*- coding:utf-8 -*-
# --------------------
# Author:   SDN
# Description:	
# ----------------

# import re
#
# origin_string = """Sisimi:
# 天猫增添品类规则升级 商家扩大经营有据可依	摘要：6月27日天猫将生效一则新规，对天猫在营店铺扩大经营范围做出了规范，加强对店铺新增品类的标准化。　　　　
# 新零售引领着消费升级的到来。越来越多的商家也开始尝试调整自身货品结构，扩大经营范围的诉求日益旺盛。为了更好的服务商家，
# 6月27日天猫将生效一则新规，对在营店铺扩大经营范围做出规范，加强店铺新增品类的标准化。在此次规则变更中，天猫依然向优质品牌、品质服务、
# 品质商品敞开怀抱，也将根据市场需求及行业特点进行择优招募。　　
# 举例来说，某商家想申请添加A类目，如果A类目不在对应的天猫定向招商品牌库内，可尝试申请自荐添加，若品牌影响力及资质要求评估通过，便可添加成功。　　
# 除此之外，天猫将针对母婴部分类目在专营店授权链路上收紧要求，加强供应链审查，同时也紧贴政策法规变化，确保商家经营资质的实时合规，籍此为消费者把好关、站好岗，
# 充分保障消费者的购物权益。　　本次规则调整将于2017年6月27日正式生效，商家有添加品类需求且符合条件的，可以戳下面链接查看申请流程，
# 或直接进入&ldquo;商家中心-品牌和类目管理&rdquo;提交申请。　　
# 天猫在营店铺新增品牌申请流程：https://service.tmall.com/support/tmall/knowledge-1124487.htm　　
# 天猫在营店铺新增类目申请流程：http://service.tmall.com/support/tmall/knowledge-1126642.htm?spm=a225r.8199751.0.0.RBQ7mK　　
# 天猫添品添类规范细则如下：　　天猫在营店铺申请新增类目细则：　　https://rule.tmall.com/tdetail-5898.htm?spm=a2177.7731966.0.0.9Di4lN&amp;tag=self　　
# 天猫在营店铺申请新增品牌细则：　　https://rule.tmall.com/tdetail-5900.htm?spm=a2177.7731966.0.0.9Di4lN&amp;tag=self
# 正大零售业务全线接入京东到家：订单量亮眼"""
#
# pattern = re.compile(r'[hH][Tt][Tt][Pp][Ss]?.*[a-zA-Z0-9/]')
# result = pattern.findall(origin_string)
# print result

# print zip(('a','b','c','d','e'),(1,2,3,4,5))
# print dict(zip(('a','b','c','d','e'),(1,2,3,4,5)))
import random


def f1(lIn):
    l1 = sorted(lIn)
    l2 = [i for i in l1 if i < 0.5]
    return [i * i for i in l2]


def f2(lIn):
    l1 = [i for i in lIn if i < 0.5]
    l2 = sorted(l1)
    return [i * i for i in l2]


def f3(lIn):
    l1 = [i * i for i in lIn]
    l2 = sorted(l1)
    return [i for i in l1 if i < (0.5 * 0.5)]


# import cProfile
#
# lIn = [random.random() for i in range(100000)]
# cProfile.run('f1(lIn)')
# cProfile.run('f2(lIn)')
# cProfile.run('f3(lIn)')

class A(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(A, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    def __init__(self, go):
        if hasattr(self, 'go'):
            return
        self.go = go


b = A(1)
print b.go
c = A(2)
print c.go

print b.go

print b is c
