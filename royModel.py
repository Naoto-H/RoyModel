# Coded by Naoto Hayashi
# coding: UTF-8

import numpy as np
from royModel_data import *
from royModel_op import *
from royModel_process import *
from numpy.random import *
from numpy import *
import random
import time
seed(1) 
if __name__ == '__main__':
	start = time.time()
	
	Arv =  Arrival()# (arTaskTime, arWorkerTime, arTask, arWorker)
	TaskIn = InitTaskIndex([], [])
	cm = CrowdMaint(Arv, TaskIn)

	for i in range(50):
		print "unit %d start" % i
		cm.arrivalTW()
		if cm.Arrival.flag > 0:
			cm.updateTW() # タスク・ワーカーの情報の変更
			cm.optimalOn() # インデックスアップデート
		cm.TIME += 1 #
		print "^^^^^^^"
		print cm.TaskIn.TAlist
		print cm.TaskIn.Workers
		print cm.TaskIn.Tasks
		if cm.TaskIn.TAlist != []:
			for j in range (len(cm.TaskIn.TAlist)):
				print "v", cm.TaskIn.TAlist[j].v_t
			for k in range (len(cm.TaskIn.TAlist)):
				print "u", cm.TaskIn.TAlist[k].u_t
		
		print cm.TaskIn.finWorkers
		print cm.TaskIn.finTasks
		print cm.TaskIn.V
		print "^^^^^^^"
		print "unit %d finish" % i

	print cm.TaskIn.TAlist
	print cm.TaskIn.Workers
	print cm.TaskIn.Tasks
	if cm.TaskIn.TAlist != []:
		for j in range (len(cm.TaskIn.TAlist)):
			print "v", cm.TaskIn.TAlist[j].v_t
		for k in range (len(cm.TaskIn.TAlist)):
			print "u", cm.TaskIn.TAlist[k].u_t
	
	print cm.TaskIn.finWorkers
	print cm.TaskIn.finTasks
	print cm.TaskIn.V
	elapsed_time = time.time() - start
	print ("elapsed_time:{0}".format(elapsed_time)) + "[sec]"

	'''
	rng = range(100)
	plt.plot(rng,,label=u"training data")
	plt.plot(rng,,label=u"predicted data")
	plt.plot(rng,,label=u"filtered data")
	plt.xlabel('Time',fontsize=16)
	plt.ylabel('Value',fontsize=16)    
	plt.legend() 
	plt.show()
	'''