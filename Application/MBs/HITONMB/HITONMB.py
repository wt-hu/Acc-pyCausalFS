import numpy as np
import pandas as pd
from Application.MBs.common.condition_independence_test import CCT_select
from Application.MBs.HITONMB.HITONPC import HITON_PC


def HITON_MB(data, target, alaph, is_discrete, dict_cache):
    PC, sepset, ci_number, dict_cache = HITON_PC(data, target, alaph, is_discrete, dict_cache)
    # print("PC is:" + str(PC))
    currentMB = PC.copy()
    for x in PC:
        # print("x is: " + str(x))
        PCofPC, _, ci_num2, dict_cache = HITON_PC(data, x, alaph, is_discrete, dict_cache)
        ci_number += ci_num2
        # print("PCofPC is " + str(PCofPC))
        for y in PCofPC:
            # print("y is " + str(y))
            if y != target and y not in PC:
                conditions_Set = [i for i in sepset[y]]
                conditions_Set.append(x)
                conditions_Set = list(set(conditions_Set))
                ci_number += 1
                pval, dep, dict_cache = CCT_select(
                    data, target, y, conditions_Set, is_discrete, dict_cache)
                if pval <= alaph:
                    # print("append is: " + str(y))
                    currentMB.append(y)
                    break

    return list(set(currentMB)), ci_number, dict_cache


# import warnings
# import time
# warnings.filterwarnings('ignore')
#
# data = pd.read_csv("D:/data/alarm_data/Alarm1_s5000_v3.csv")
# print("the file read")
# num1, kvar = np.shape(data)
#
# alaph = 0.01
# averged = 0
# time_spend = 0
# start_time = time.process_time()
# for target in range(kvar):
#     dic = {}
#     dic.setdefault("cache", [0, 0])
#     print("target = ", target)
#     MBs, sepset, dic, num_test, tw1 = HITON_MB(data, target, alaph, True, dic)
#     time_spend += tw1
#     end_time1 = time.process_time()
#     print(len(dic))
#     print("time_spend: ", time_spend)
#     print("run time once : ", end_time1 - start_time)
#     print("num _ test: ", num_test)
#
# end_time = time.process_time()
# # print("---", averged / kvar)
# print(time_spend)
# print("run time = ", end_time - start_time)