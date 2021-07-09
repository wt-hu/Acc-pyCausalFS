from Application.MBs.semi_HITON.semi_HITON_PC import semi_HITON_PC
from Application.MBs.common.condition_independence_test import CCT_select


def semi_HITON_MB(data, target, alaph, is_discrete, dict_cache):
    TPC, sep, ci_number, dict_cache = semi_HITON_PC(data, target, alaph, is_discrete, dict_cache)
    MB = TPC.copy()
    for x in TPC:
        xPC, sepx, ci_number2, dict_cache = semi_HITON_PC(data, x, alaph, is_discrete, dict_cache)
        ci_number += ci_number2
        for y in xPC:
            if y != target and y not in TPC:
                condition_set = [i for i in sep[y]]
                condition_set = list(set(condition_set).union(set([x])))
                ci_number += 1
                pval, _, dict_cache = CCT_select(
                    data, target, y, condition_set, is_discrete, dict_cache)
                if pval <= alaph:
                    # print("append y is " + str(y))
                    MB.append(y)
                    break
    return list(set(MB)), ci_number, dict_cache



# import warnings
# warnings.filterwarnings('ignore')
# import pandas as pd
# data = pd.read_csv("D:/data/alarm_data/Alarm1_s5000_v2.csv")
# print("the file read")
# import numpy as np
# num1, kvar = np.shape(data)
#
# alaph = 0.01
# averged = 0
# for target in range(kvar):
#     dic = {}
#     dic.setdefault("cache", [0, 0])
#     MBs, sepset, dic = semi_HITON_MB(data, target, alaph, True, dic)
#     # print(dic["cache"][0], "-", dic["cache"][1],
#     #   "-", (dic["cache"][0] + dic["cache"][1]))
#     print(dic["cache"][0] / (dic["cache"][0] + dic["cache"][1]))
#     averged += dic["cache"][0] / (dic["cache"][0] + dic["cache"][1])
# print("---", averged / kvar)
