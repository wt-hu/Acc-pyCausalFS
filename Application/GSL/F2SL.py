#!/usr/bin/env python
# encoding: utf-8
"""
 @Time    : 2020/8/13 9:43
 @File    : F2SL.py
 """

import numpy as np
from Application.MBs.common.subsets import subsets
from Application.MBs.common.Meek import meek
from Application.MBs.common.condition_independence_test import CCT_select
from Application.MBs.MMMB.MMPC import MMPC
from Application.MBs.HITONMB.HITONPC import HITON_PC
from Application.MBs.semi_HITON.semi_HITON_PC import semi_HITON_PC
from Application.MBs.PCMB.getPC import getPC



def F2SL(data, alpha, is_discrete):
    _, kvar = np.shape(data)
    max_k = 3
    all_pc = [[] for i in range(kvar)]
    all_sepset = [[[] for i in range(kvar)] for j in range(kvar)]
    PP = np.zeros((kvar, kvar))

    # Set initial cache valuej
    dict_cache = {}
    dict_cache.setdefault("cache", [0, 0])


    for i in range(kvar):
        PC, _, _, dict_cache = MMPC(data, i, alpha, is_discrete, dict_cache)

        # PC, _, _, dict_cache = HITON_PC(data, i, alpha, is_discrete, dict_cache)
        # PC, _, _, dict_cache = getPC(data, i, alpha, is_discrete, dict_cache)
        # PC, _, _, dict_cache = semi_HITON_PC(data, i, alpha, is_discrete, dict_cache)

        for j in PC:
            PP[i, j] = 1

    # # AND Rule
    # for i in range(kvar):
    #     for j in range(0, i):
    #         if DAG[i, j] != DAG[j, i]:
    #             DAG[i, j] = 0
    #             DAG[j, i] = 0

    # OR Rule due to imprecise CI test
    for i in range(kvar):
        for j in range(0, i):
            if PP[i, j] != PP[j, i]:
                PP[i, j] = 1
                PP[j, i] = 1

    # step 2: orient V-structures
    for i in range(kvar):
        for j in range(kvar):
            if PP[i, j] == 1:
                all_pc[i].append(j)

    DAG = PP.copy()
    pdag = PP.copy()
    G = PP.copy()

    for A in range(kvar):
        for B in all_pc[A]:
            for C in all_pc[B]:

                if C in all_pc[A] or C == A:
                    continue

                canPC = all_pc[A]
                cutSetSize = 0
                break_flag = 0
                while len(canPC) >= cutSetSize and cutSetSize <= max_k:

                    SS = subsets(canPC, cutSetSize)
                    for s in SS:
                        z = [i for i in s]
                        pval, _, dict_cache = CCT_select(
                            data, C, A, z, is_discrete, dict_cache)
                        if pval > alpha:
                            all_sepset[A][C].append(list(map(int, z)))
                            all_sepset[C][A].append(list(map(int, z)))

                            if B not in z:
                                conSet = set(z).union(set([B]))
                                pval2, _, dict_cache = CCT_select(
                                    data, C, A, conSet, is_discrete, dict_cache)

                                if pval2 <= alpha:

                                    pdag[A, B] = -1
                                    pdag[B, A] = 0

                                    pdag[C, B] = -1
                                    pdag[B, C] = 0

                                    G[A, B] = 1
                                    G[B, A] = 0

                                    G[C, B] = 1
                                    G[B, C] = 0

                            break_flag = True
                            break
                    if break_flag:
                        break
                    cutSetSize += 1

    DAG, pdag, G = meek(DAG, pdag, G, kvar)

    return pdag, dict_cache


# import warnings
# warnings.filterwarnings('ignore')
# import pandas as pd
# data = pd.read_csv("D:/data/child_data/Child_s5000_v5.csv")
# print("the file read")
# import numpy as np
# num1, kvar = np.shape(data)
# alpha = 0.01
#
# pdag, dic = F2SL(data, alpha, True)
# print(pdag)
# for i in range(kvar):
#     for j in range(kvar):
#         if pdag[i, j] == -1:
#             print("i: ", i, " ,j: ", j)
# print(dic["cache"][0]/(dic["cache"][0]+dic["cache"][1]))
