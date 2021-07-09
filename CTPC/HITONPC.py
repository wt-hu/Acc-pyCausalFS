from CTPC.common.condition_independence_test import CCT_select
from CTPC.common.subsets import subsets
import numpy as np


def HITON_PC(data, target, alaph, is_discrete, dict_cache):
    number, kVar = np.shape(data)
    sepset = [[] for i in range(kVar)]
    variDepSet = []
    candidate_PC = []
    PC = []
    ci_number = 0
    noAdmissionSet = []
    max_k = 3
    # use a list to store variables which are not condition independence with
    # target,and sorted by dep max to min
    candidate_Vars = [i for i in range(kVar) if i != target]
    for x in candidate_Vars:
        ci_number += 1
        pval_gp, dep_gp, dict_cache = CCT_select(
            data, target, x, [], is_discrete, dict_cache)
        if pval_gp <= alaph:
            variDepSet.append([x, dep_gp])

    # sorted by dep from max to min
    variDepSet = sorted(variDepSet, key=lambda x: x[1], reverse=True)
    # print(variDepSet)

    # get number by dep from max to min
    for i in range(len(variDepSet)):
        candidate_PC.append(variDepSet[i][0])
    # print(candidate_PC)

    """ sp """
    for x in candidate_PC:

        PC.append(x)
        PC_index = len(PC)
        # if new x add will be removed ,test will not be continue,so break the
        # following circulate to save time ,but i don't not why other index
        # improve
        breakFlagTwo = False

        while PC_index >= 0:
            #  reverse traversal PC,and use PC_index as a pointer of PC
            PC_index -= 1
            y = PC[PC_index]
            breakFlag = False
            conditions_Set = [i for i in PC if i != y]

            if len(conditions_Set) >= max_k:
                Slength = max_k
            else:
                Slength = len(conditions_Set)

            for j in range(Slength + 1):
                SS = subsets(conditions_Set, j)
                for s in SS:
                    ci_number += 1
                    conditions_test_set = [i for i in s]
                    pval_rm, dep_rm, dict_cache = CCT_select(
                        data, target, y, conditions_test_set, is_discrete, dict_cache)
                    if pval_rm > alaph:
                        sepset[y] = [i for i in conditions_test_set]
                        # if new x add will be removed ,test will not be
                        # continue
                        if y == x:
                            breakFlagTwo = True
                        PC.remove(y)
                        breakFlag = True
                        break

                if breakFlag:
                    break
            if breakFlagTwo:
                break

    return list(set(PC)), sepset, ci_number, dict_cache


#data = pd.read_csv("E:/python/pycharm/algorithm/data/Child_s500_v1.csv")
#PC,sepset,ntest = HITON_PC(data, 1, 0.01)
# print(PC)
# print(ntest)
# import warnings
# warnings.filterwarnings('ignore')
# import pandas as pd
# data = pd.read_csv("C:/pythonProject/BN_PC_algorithm/CBD/data/child_s5000_v1.csv")
# print("the file read")
# import numpy as np
# num1, kvar = np.shape(data)
# alaph = 0.01
# dic = {}
# dic.setdefault("cache", [0, 0])
# for target in range(kvar):
# # target = 1
#     PC,sepset,ntest,dic = HITON_PC(data, target, alaph, True, dic)
# # from LSL_cache.MBs.common.g2test import g2_test_dis
# # pval,dep =g2_test_dis(data, 0, 1, [4], alaph)
#     print(target, " -PC-: ", PC)
#     print(dic["cache"][0]/(dic["cache"][0]+dic["cache"][1]))
# print("pval: ", pval, " ,dep: ", dep)