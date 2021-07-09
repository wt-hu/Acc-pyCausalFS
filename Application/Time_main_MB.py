#!/usr/bin/env python
# encoding: utf-8
"""
 @Time    : 2020/9/18 16:17
 @File    : Time_main_MB.py
 """
import numpy as np
import pandas as pd
import time
from Application.MBs.common.realMB import realMB
from Application.MBs.MMMB.MMMB import MMMB
from Application.MBs.HITONMB.HITONMB import HITON_MB
from Application.MBs.PCMB.PCMB import PCMB
from Application.MBs.semi_HITON.semi_HITON_MB import semi_HITON_MB


def evaluation_mb_cache( method, path, all_number_Para, target_list, real_graph_path, is_discrete, filenumber, alaph):

    # pre_set variables is zero

    cache_utilization = 0
    num_cache = 0
    num_ci_test = 0
    Precision = 0
    Recall = 0
    F1 = 0
    Distance = 0
    use_time = 0
    ci_number = 0
    realmb, realpc = realMB(all_number_Para, real_graph_path)
    # print("realmb is: ", realmb)
    length_targets = len(target_list)
    for m in range(filenumber):
        completePath = path + str(m + 1) + ".csv"
        data = pd.read_csv(completePath)
        number, kVar = np.shape(data)
        ResMB = [[]] * length_targets
        completePath = path + str(m + 1) + ".csv"
        data = pd.read_csv(completePath)
        for i, target in enumerate(target_list):
            # print("target is: " + str(target))

            # initialize the cache table
            dict_cache = {}
            dict_cache.setdefault("cache", [0, 0])

            if method == "MMMB":
                start_time = time.process_time()
                MB, ci_num, dict_cache = MMMB(data, target, alaph, is_discrete, dict_cache)
                end_time = time.process_time()
            elif method == "HITON_MB":
                start_time = time.process_time()
                MB, ci_num, dict_cache = HITON_MB(data, target, alaph, is_discrete, dict_cache)
                end_time = time.process_time()
            elif method == "semi_HITON_MB":
                start_time = time.process_time()
                MB, ci_num, dict_cache = semi_HITON_MB(data, target, alaph, is_discrete, dict_cache)
                end_time = time.process_time()
            elif method == "PCMB":
                start_time = time.process_time()
                MB, ci_num, dict_cache = PCMB(data, target, alaph, is_discrete, dict_cache)
                end_time = time.process_time()
            else:
                raise Exception("method input error!")
            use_time += (end_time - start_time)
            ResMB[i] = MB
            num_cache += dict_cache['cache'][0]
            num_ci_test += dict_cache['cache'][1]
            ci_number += ci_num

        for n, target in enumerate(target_list):
            # print("target is: " + str(target) + " , n is: " + str(n))
            true_positive = list(
                set(realmb[target]).intersection(set(ResMB[n])))
            length_true_positive = len(true_positive)
            length_RealMB = len(realmb[target])
            length_ResMB = len(ResMB[n])
            if length_RealMB == 0:
                if length_ResMB == 0:
                    precision = 1
                    recall = 1
                    distance = 0
                    F1 += 1
                else:
                    F1 += 0
                    precision = 0
                    distance = 2 ** 0.5
                    recall = 0
            else:
                if length_ResMB != 0:
                    precision = length_true_positive / length_ResMB
                    recall = length_true_positive / length_RealMB
                    distance = ((1 - precision) ** 2 + (1 - recall) ** 2) ** 0.5
                    if precision + recall != 0:
                        F1 += 2 * precision * recall / (precision + recall)
                else:
                    F1 += 0
                    precision = 0
                    recall = 0
                    distance = 2 ** 0.5
            Distance += distance
            Precision += precision
            Recall += recall

        print("file: ", m + 1, " , use_time: ", use_time)
        print("cache_rate: ", num_cache / (num_cache + num_ci_test))
    cache_utilization = num_cache / (num_cache + num_ci_test)
    commonDivisor = length_targets * filenumber

    return F1 / commonDivisor, Precision / commonDivisor, Recall / commonDivisor, Distance / \
        commonDivisor, use_time / commonDivisor, ci_number / commonDivisor, cache_utilization,


# test main
if __name__ == '__main__':
    #
    method_list = ["HITON_MB", "MMMB", "PCMB", "semi_HITON_MB","MBOR"]
    data_path = "D:/data/ins5_data/Insurance5_s5000_v"
    real_graph_path = "D:/data/ins5_data/Insurance5_graph.txt"
    alpha = 0.01
    isdiscrete = True
    for method in method_list:
        print(str(method))
        pre_data = pd.read_csv('D:/data/ins5_data/Insurance5_s5000_v1.csv')    # get number of data feature
        _, num_para = np.shape(pre_data)
        print(num_para)
        list_target = [i for i in range(num_para)]
        file_number = 5
        F1, Precision, Recall, Distance, average_time, num_ci, cache_utilization = evaluation_mb_cache(method, data_path, num_para, list_target, real_graph_path,isdiscrete,
                                                                  file_number, alpha)
        print("F1 is: " + str("%.3f " % F1))
        print("Precision is: " + str("%.3f" % Precision))
        print("Recall is: " + str("%.3f" % Recall))
        print("Distance is: " + str("%.3f" % Distance))
        print("time is: ", str("%.3f" % average_time))
        print("num_CI is: ", str("%.3f" % num_ci))
        print("cache_utilization is: ", str("%.3f" % cache_utilization))
        with open(r".\output\time_indicator.txt", "a+") as file:
            file.write("data is: " + str(data_path)+"\n")
            file.write(str(method) + ": \n")
            file.write("F1 is: " + str("%.3f " % F1) + "\n")
            file.write("Precision is: " + str("%.3f" % Precision) + "\n")
            file.write("Recall is: " + str("%.3f" % Recall) + "\n")
            file.write("Distance is: " + str("%.3f" % Distance) + "\n")
            file.write("Time is: " + str("%.3f " % average_time) + "\n")
            file.write("num_CI is: " + str("%.3f " % num_ci) + "\n")
            file.write("cache_utilization is: " + str("%.3f " % cache_utilization) + "\n")
