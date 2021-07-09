#!/usr/bin/env python
# encoding: utf-8
"""
 @Time    : 2020/10/28 14:38
 @File    : time_main_LSL.py
 """


import numpy as np
import pandas as pd
from Application.LSL.common.real_P_C_S import real_p_c_s
from Application.LSL.PCDbyPCD import PCDbyPCD
from Application.LSL.MBbyMB import MBbyMB
from Application.LSL.CMB.CMB import CMB
import time

def evaluation_cache(method,
               path,
               all_number_Para,
               target_list,
               real_graph_path,
               is_discrete,
               filenumber=10,
               alaph=0.01,
               ):
    # pre_set variables is zero
    length_target_list = len(target_list)
    real_p, real_c, real_s = real_p_c_s(all_number_Para, real_graph_path)
    num_re, num_undirect = 0, 0
    num_miss ,num_extra= 0, 0
    num_true = 0
    all_time = 0
    num_cache = 0
    num_ci_test = 0
    num_ci = 0
    for m in range(filenumber):
        completePath = path + str(m + 1) + ".csv"
        data = pd.read_csv(completePath)
        get_p, get_c, get_un = [[] for i in range(length_target_list)], [[] for i in range(length_target_list)], [[] for i in range(length_target_list)]

        for i, target in enumerate(target_list):

            # initialize the cache table
            dict_cache = {}
            dict_cache.setdefault("cache", [0, 0])

            if method == "PCDbyPCD":
                start_time = time.process_time()
                parents, children, PC, undirected, n_c, dict_cache = PCDbyPCD(data, target, alaph, is_discrete, dict_cache)
                end_time = time.process_time()
            elif method == "MBbyMB":
                start_time = time.process_time()
                parents, children, PC, undirected, n_c, dict_cache = MBbyMB(data, target, alaph, is_discrete, dict_cache)
                end_time = time.process_time()
            elif method == "CMB":
                start_time = time.process_time()
                parents, children, PC, undirected, n_c, dict_cache = CMB(data, target, alaph, is_discrete, dict_cache)
                end_time = time.process_time()
            else:
                raise Exception("method input error!")

            get_p[i] = parents
            get_c[i] = children
            get_un[i] = undirected
            all_time += end_time - start_time

            num_cache += dict_cache['cache'][0]
            num_ci_test += dict_cache['cache'][1]
            num_ci += n_c

        print("use time:", all_time)

        for n, target in enumerate(target_list):

            true_diection = list((set(real_p[target]).intersection(set(get_p[n]))).union(set(real_c[target]).intersection(set(get_c[n]))))
            num_true += len(true_diection)

            reverse_direction = list((set(real_p[target]).intersection(
                set(get_c[n]))).union(set(real_c[target]).intersection(set(get_p[n]))))
            num_re += len(reverse_direction)

            undirected_direction = list(get_un[n])
            num_undirect += len(undirected_direction)

            miss_direction = list(((set(real_p[target]).difference(set(get_p[n]))).union(
                set(real_c[target]).difference(set(get_c[n])))).difference(set(reverse_direction).union(undirected_direction)))
            num_miss += len(miss_direction)

            extra_direction = list(((set(get_p[n]).difference(real_p[target])).union(
                set(get_c[n]).difference(set(real_c[target])))))
            num_extra += len(extra_direction)

    commonDivisor = length_target_list * filenumber
    cache_utilization = num_cache / (num_cache + num_ci_test)
    return num_true / commonDivisor, num_re / commonDivisor, num_miss / commonDivisor, num_extra / commonDivisor, num_undirect / commonDivisor, all_time / commonDivisor, num_ci/commonDivisor, cache_utilization


# test main
if __name__ == '__main__':
    #
    method_list = ["PCDbyPCD", "MBbyMB", "CMB"]
    data_path = "D:/data/Alarm3_data/Alarm3_s5000_v"
    alpha = 0.01
    isdiscrete = True
    real_graph_path = "D:/data/Alarm3_data/Alarm3_graph.txt"
    for method in method_list:
        pre_data = pd.read_csv('D:/data/Alarm3_data/Alarm3_s5000_v1.csv')
        _, num_para = np.shape(pre_data)
        list_target = [i for i in range(11) if i != 0]
        isdiscrete = True
        file_number = 5
        print("method: ", method)
        num_true, num_re, num_miss, num_extra, num_undirected, use_time, num_ci, cache_utilization = evaluation_cache(
            method, data_path, num_para, list_target, real_graph_path, isdiscrete, file_number, alpha)

        print("true direction is: ", str("%.3f" % num_true))
        print("reverse is: ", str("%.3f" % num_re))
        print("miss is: ", str("%.3f" % num_miss))
        print("extra is: ", str("%.3f" % num_extra))
        print("undirected is:", str("%.3f" % num_undirected))
        print("time is:", str("%.3f" % use_time))
        print("num_ci is:", str("%.3f" % num_ci))
        print("cache_utilization is:", str("%.3f" % cache_utilization))
        with open(r".\output\time_indicator_LSL.txt", "a+") as file:
            file.write(str(method) + ": \n")
            file.write("path: " + data_path + ".\n")
            file.write("true direction is: " + str("%.3f" % num_true) + "\n")
            file.write("reverse is: " + str("%.3f" % num_re) + "\n")
            file.write("miss is: " + str("%.3f" % num_miss) + "\n")
            file.write("extra is: " + str("%.3f" % num_extra) + "\n")
            file.write("undirected is: " + str("%.3f" % num_undirected) + "\n")
            file.write("time is:" + str("%.3f" % use_time) + "\n")
            file.write("num_ci is:" + str("%.3f" % num_ci) + "\n")
            file.write("cache_utilization is:" + str("%.3f" % cache_utilization) + "\n")