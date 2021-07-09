#!/usr/bin/env python
# encoding: utf-8
"""
 @Time    : 2019/11/13 21:34
 @File    : independence_condition_test.py
 """

from CTPC.common.fisher_z_test import cond_indep_fisher_z
from CTPC.common.g2test import g2_test_dis


def cond_indep_test(data, target, var, cond_set=[], is_discrete=True, alpha=0.01):
    if is_discrete:
        pval, dep = g2_test_dis(data, target, var, cond_set, alpha)

    else:
        _, dep, pval = cond_indep_fisher_z(data, target, var, cond_set, alpha)

    return pval, dep


def CCT_select(data, target, var, cond_set, is_discrete, dict_cache, flag=True):

    # Phase 1: Generate the key

    na = sorted([target, var])
    len_con_set = len(cond_set)
    if len_con_set != 0:
        na.extend(sorted(cond_set))
    # Splice
    akey = "_".join('%s' % id for id in na)

    #  Phase 2:  Query cache table by the key
    if akey in dict_cache.keys():
        if flag:
            dict_cache["cache"][0] += 1
        pvalue, dep = dict_cache[akey]

    else:
        if flag:
            dict_cache["cache"][1] += 1
        pvalue, dep = cond_indep_test(data, target, var, cond_set, is_discrete)
        dict_cache.setdefault(akey, [pvalue, dep])

    return pvalue, dep, dict_cache
