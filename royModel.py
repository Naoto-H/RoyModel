# Coded by Naoto Hayashi
# coding: UTF-8

import numpy as np
from royModel_data import *
from royModel_op import *
#from royModel_process import *
from numpy.random import *
from numpy import *
import random
import time

#ポワソン過程によって今残っているのtaskとworker
#curTask = [[random.choice(T)] * 100] #今残っているタスクリスト
#curWorker = [[random.choice(U)] * 100] #今残っているワーカリスト
#curTask = random.sample(T, 2) #今残っているタスクリスト
#curWorker = random.sample(U, 2) #今残っているワーカリスト
curTask = [T[1], T[2]]
curWorker = [U[0], U[1]]


########出力########
# 新しいTaskIndex
# Task、Worker振り分け
# 最終TaskIndexに更新
###################
if __name__ == '__main__':
	start = time.time()
	TaskIn = InitTaskIndex(curTask, curWorker) # TaskIndexの初期化(新規作成or追加)
	TaskIn1 = InitTaskIndex(curTask, curWorker)
	TaskIn = AssignWorker(0, TaskIn, 0, TaskIn1)
	TaskIn.cul_V()
	
	print TaskIn.TAlist[0].v_t
	print TaskIn.TAlist[1].v_t
#	print TaskIn.TAlist[2].v_t
#	print TaskIn.TAlist[3].v_t
#	print TaskIn.TAlist[4].v_t
	print TaskIn.TAlist[0].u_t
	print TaskIn.TAlist[1].u_t
#	print TaskIn.TAlist[2].u_t
#	print TaskIn.TAlist[3].u_t
#	print TaskIn.TAlist[4].u_t
	print TaskIn.V
	

	elapsed_time = time.time() - start
	print ("elapsed_time:{0}".format(elapsed_time)) + "[sec]"