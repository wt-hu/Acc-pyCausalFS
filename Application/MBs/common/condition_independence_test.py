#!/usr/bin/env python
# encoding: utf-8
"""
 @Time    : 2019/11/13 21:34
 @File    : independence_condition_test.py
 """

from Application.MBs.common.chi_square_test import chi_square_test
from Application.MBs.common.fisher_z_test import cond_indep_fisher_z
from Application.MBs.common.chi_square_test import chi_square
from Application.MBs.common.g2test import g2_test_dis


def cond_indep_test(data, target, var, cond_set=[], is_discrete=True, alpha=0.01):
    if is_discrete:
        pval, dep = g2_test_dis(data, target, var, cond_set, alpha)
    else:
        _, dep, pval = cond_indep_fisher_z(data, target, var, cond_set, alpha)

    return pval, dep


def CCT_select(data, target, var, cond_set, is_discrete, dict_cache, flag=True):
    # 1.将target，var，cond_set整合成字典所需的key值
    na = sorted([target, var])
    len_con_set = len(cond_set)
    if len_con_set != 0:
        na.extend(sorted(cond_set))

    akey = "_".join('%s' % id for id in na)

    # 2.如果发现字典中存有本次所需的值，则调用
    if akey in dict_cache.keys():
        if flag:
            dict_cache["cache"][0] += 1
        pvalue, dep = dict_cache[akey]

    # 3.否则直接进行独立性测试，并存储本次结果
    else:
        if flag:
            dict_cache["cache"][1] += 1
        pvalue, dep = cond_indep_test(data, target, var, cond_set, is_discrete)
        dict_cache.setdefault(akey, [pvalue, dep])

    return pvalue, dep, dict_cache
