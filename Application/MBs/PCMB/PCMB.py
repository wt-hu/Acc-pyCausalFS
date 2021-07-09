# coding=utf-8
# /usr/bin/env python
"""
date: 2019/7/17 15:23
desc:
"""

from Application.MBs.PCMB.getPC import getPC
from Application.MBs.common.condition_independence_test import CCT_select


def PCMB(data, target, alaph, is_discrete, dict_cache):
    ci_number = 0
    PC, sepset, ci_num2, dict_cache = getPC(data, target, alaph, is_discrete, dict_cache)
    ci_number += ci_num2
    # print(PC)
    # print(sepset)
    MB = PC.copy()

    for x in PC:
        PCofPC_temp, _, ci_num3, dict_cache = getPC(data, x, alaph, is_discrete, dict_cache)
        ci_number += ci_num3
        # print(" pc of pc_temp is: " + str(PCofPC_temp))
        PCofPC = [i for i in PCofPC_temp if i != target and i not in MB]
        # print(" pc of pc is: " + str(PCofPC))
        for y in PCofPC:
            conditionSet = [i for i in sepset[y]]
            conditionSet.append(x)
            conditionSet = list(set(conditionSet))
            ci_number += 1
            pval, dep, dict_cache = CCT_select(
                data, target, y, conditionSet, is_discrete, dict_cache)
            if pval <= alaph:
                MB.append(y)
                break
    return list(set(MB)), ci_number, dict_cache


# import warnings
# warnings.filterwarnings('ignore')
# import pandas as pd
# import numpy as np
# data = pd.read_csv("D:/data/alarm_data/Alarm1_s5000_v6.csv")
# print("the file read")
# num1, kvar = np.shape(data)
#
# alaph = 0.01
# averged = 0
# for target in range(kvar):
#     dic = {}
#     dic.setdefault("cache", [0, 0])
#     MBs, sepset, dic = PCMB(data, target, alaph, True, dic)
#     # print(dic["cache"][0], "-", dic["cache"][1],
#     #   "-", (dic["cache"][0] + dic["cache"][1]))
#     print(dic["cache"][0] / (dic["cache"][0] + dic["cache"][1]))
#     averged += dic["cache"][0] / (dic["cache"][0] + dic["cache"][1])
# print("---", averged / kvar)

