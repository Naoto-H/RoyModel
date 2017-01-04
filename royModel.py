# Coded by Naoto Hayashi
# coding: UTF-8

import numpy as np
from royModel_data import *
from royModel_optimal import *
from royModel_process import *
from numpy.random import *
from numpy import *
import matplotlib.pyplot as plt
import random
import time

PERIOD = 1440 #全体の時間
CUL_UNI = 1 #出力したい期間単位

seed(7) 

if __name__ == '__main__':
	start = time.time()

	Arv =  Arrival()
	TaskIn = initTaskIndex([], [])
	cm = CrowdMaint(Arv, TaskIn)
	
	FIN = [0]
	V = [0]

	for i in range(PERIOD):
		cm.ahead()
		if i%CUL_UNI == 0 and i > 0:
			elapsed_time = time.time() - start
			print "%d時間後" % i, cm.TaskIn.finTasks, cm.TaskIn.V, ("elapsed_time:{0}".format(elapsed_time)) + "[sec]"
			FIN.append(cm.TaskIn.finTasks)
			V.append(cm.TaskIn.V)
			#FIN.append(cm.TaskIn.finTasks - FIN[i/CUL_UNI-1])
			#V.append(cm.TaskIn.V - V[i / CUL_UNI -1])

		#	print cm.wage
		#print "^^^ unit %d ^^^" % i
		#printTI(cm.TaskIn)
		#print "^^^ unit %d ^^^" % i
		
	printTI(cm.TaskIn)
	
	'''
	W = []
	X = []
	Y = []
	Z = []
	S = []
	for u in U:
		X.append(u.wage)
		Y.append(u.q_s2)
		Z.append(u.q_s1)
		S.append(u.p)
		W.append(u.w_tr+u.wage)
	'''
	rng = range(PERIOD)	
	plt.plot(rng, FIN, label=u"Fraction of Successful tasks")
	plt.plot(rng, V, label=u"Objective function")
	
	#rng = range(len(FIN))	
	#plt.plot(rng, FIN, label=u"Fraction of Successful tasks")
	#plt.plot(rng, V, label=u"Objective function")

	#plt.hist(x_s1 ,label=u"x_s1")
	#plt.hist(W,label=u"x_s2")
	#plt.hist(d_i,label=u"x_s2")

	plt.xlabel('Time',fontsize=16)
	plt.ylabel('Value',fontsize=16)    
	plt.legend()
	plt.show()
	
	elapsed_time = time.time() - start
	print ("elapsed_time:{0}".format(elapsed_time)) + "[sec]"