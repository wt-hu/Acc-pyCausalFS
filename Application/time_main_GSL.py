#!/usr/bin/env python
# encoding: utf-8
"""
 @Time    : 2020/11/5 20:46
 @File    : time_main_GSL.py
 """
import numpy as np
import pandas as pd
from Application.LSL.common.real_P_C_S import real_p_c_s
from Application.GSL.MMHC.MMHC import MMHC
# from Application.GSL.F2SL import F2SL
# from Application.GSL.GSBN import GSBN
from Application.GSL.MBGSL import MBGSL
import time

def evaluation_cache(method,
               path,
               all_number_Para,
               real_graph_path,
               is_discrete,
               filenumber=10,
               alpha=0.01,
               ):
    # pre_set variables is zero
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
        get_p, get_c, get_un = [[] for i in range(all_number_Para)], [[] for i in range(all_number_Para)] , [[] for i in range(all_number_Para)]

        # initialize the cache table
        dict_cache = {}
        dict_cache.setdefault("cache", [0, 0])
        if method == "MMHC":
            start_time = time.process_time()
            DAG, n_c, dict_cache = MMHC(data, alpha, dict_cache)
            end_time = time.process_time()
        elif method == "MMMBGSL":
            start_time = time.process_time()
            DAG, n_c, dict_cache = MBGSL(data, alpha, is_discrete, 1, dict_cache)
            end_time = time.process_time()
        elif method == "HITONMBGSL":
            start_time = time.process_time()
            DAG, n_c, dict_cache = MBGSL(data, alpha, is_discrete, 2, dict_cache)
            end_time = time.process_time()
        else:
            raise Exception("method input error!")
        for i in range(all_number_Para):
            for j in range(all_number_Para):
                if DAG[i, j] == -1:
                    get_c[i].append(j)
                    get_p[j].append(i)
                elif DAG[i, j] == 1:
                    get_un[i].append(j)

        all_time += end_time - start_time
        num_ci += n_c
        num_cache += dict_cache['cache'][0]
        num_ci_test += dict_cache['cache'][1]

        print("use time:", all_time)
        for n in range(all_number_Para):

            true_diection = list((set(real_p[n]).intersection(set(get_p[n]))).union(set(real_c[n]).intersection(set(get_c[n]))))
            num_true += len(true_diection)

            reverse_direction = list((set(real_p[n]).intersection(
                set(get_c[n]))).union(set(real_c[n]).intersection(set(get_p[n]))))
            num_re += len(reverse_direction)

            undirected_direction = list(get_un[n])
            num_undirect += len(undirected_direction)

            miss_direction = list(((set(real_p[n]).difference(set(get_p[n]))).union(
                set(real_c[n]).difference(set(get_c[n])))).difference(reverse_direction))
            num_miss += len(miss_direction)

            extra_direction = list(((set(get_p[n]).difference(set(real_p[n]))).union(
                set(get_c[n]).difference(set(real_c[n])))).difference(reverse_direction))
            num_extra += len(extra_direction)

    cache_utilization = num_cache / (num_cache + num_ci_test)
    commonDivisor = filenumber * 2
    return num_true / commonDivisor, num_re / commonDivisor, num_miss / commonDivisor, num_extra / commonDivisor, num_undirect/commonDivisor, all_time/ filenumber, num_ci/ filenumber, cache_utilization


# test main
if __name__ == '__main__':
    #
    method_list = ['HITONMBGSL']
    num_i_list = ["", "3", "5", "10"]
    for i in num_i_list:

        data_path = "D:/data/hailf"+i+"_data/HailFinder"+i+"_s5000_v"
        print(data_path)
        alpha = 0.01
        isdiscrete = True
        real_graph_path = "D:/data/hailf"+i+"_data/HailFinder"+i+"_graph.txt"
        print(real_graph_path)
        for method in method_list:
            pre_data = pd.read_csv("D:/data/hailf"+i+"_data/HailFinder"+i+"_s5000_v1.csv")
            _, num_para = np.shape(pre_data)
            isdiscrete = True
            file_number = 5
            print("method: ", method)
            num_true, num_re, num_miss, num_extra, num_undirected, use_time, num_ci, cache_utilization = evaluation_cache(
                method, data_path, num_para, real_graph_path, isdiscrete, file_number, alpha)

            print("true direction is: ", str("%.3f" % num_true))
            print("reverse is: ", str("%.3f" % num_re))
            print("miss is: ", str("%.3f" % num_miss))
            print("extra is: ", str("%.3f" % num_extra))
            print("undirected is:", str("%.3f" % num_undirected))
            print("time is:", str("%.3f" % use_time))
            print("num_ci is:", str("%.3f" % num_ci))
            print("cache_utilization is:", str("%.3f" % cache_utilization))
            with open(r".\output\time_indicator_GSL.txt", "a+") as file:
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