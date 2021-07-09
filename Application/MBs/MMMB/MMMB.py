# coding=utf-8
# /usr/bin/env python
"""
date: 2019/7/15 9:57
desc: 
"""
from Application.MBs.MMMB.MMPC import MMPC
from Application.MBs.common.condition_independence_test import CCT_select


def MMMB(data, target, alaph, is_discrete, dict_cache):
    ci_number = 0
    PC, sepset, ci_num2, dict_cache = MMPC(data, target, alaph, is_discrete, dict_cache)
    ci_number += ci_num2

    MB = PC.copy()
    for x in PC:

        PCofPC, _, ci_num3, dict_cache = MMPC(data, x, alaph, is_discrete, dict_cache)
        ci_number += ci_num3

        for y in PCofPC:

            if y != target and y not in PC:
                conditions_Set = [i for i in sepset[y]]
                conditions_Set.append(x)
                conditions_Set = list(set(conditions_Set))
                ci_number += 1
                pval, dep, dict_cache = CCT_select(data, target, y, conditions_Set, is_discrete, dict_cache)

                if pval <= alaph:
                    MB.append(y)
                    break
    return list(set(MB)), ci_number, dict_cache



# import warnings
# warnings.filterwarnings('ignore')
# import pandas as pd
# import numpy as np
# data = pd.read_csv("D:/data/alarm_data/Alarm1_s5000_v8.csv")
# print("the file read")
# num1, kvar = np.shape(data)
#
# alaph = 0.01
# averged = 0
# for target in range(kvar):
#     dic = {}
#     dic.setdefault("cache", [0, 0])
#     MBs, sepset, dic = MMMB(data, target, alaph, True, dic)
#     # print(dic["cache"][0], "-", dic["cache"][1],
#     #   "-", (dic["cache"][0] + dic["cache"][1]))
#     print(dic["cache"][0] / (dic["cache"][0] + dic["cache"][1]))
#     averged += dic["cache"][0] / (dic["cache"][0] + dic["cache"][1])
#     print(dic["cache"][0], "-------", dic["cache"][1])
# print("---", averged / kvar)

# import pandas as pd
# data = pd.read_csv("D:/data/Alarm5_data/Alarm5_s5000_v4.csv")
# print("the file read")
#
#
# import numpy as np
# num1, kvar = np.shape(data)
# alaph = 0.01
# dic = {}
# dic.setdefault("cache", [0, 0])
# for target in range(kvar):
# # target = 1
#     dic = {}
#     dic.setdefault("cache", [0, 0])
#     MB,ntest,dic = MMMB(data, target, alaph, True, dic)
# # from LSL_cache.MBs.common.g2test import g2_test_dis
# # pval,dep =g2_test_dis(data, 0, 1, [4], alaph)
# #     print(target, " -MB-: ", MB)
#     print(dic["cache"][0]/(dic["cache"][0]+dic["cache"][1]))


