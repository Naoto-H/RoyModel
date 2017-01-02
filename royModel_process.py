# Coded by Naoto Hayashi
# coding: UTF-8

import numpy as np
from royModel_data import *
from royModel_op import *
from numpy.random import *
from numpy import *

IntervalTask = 2
IntervalWorker = 4

class Arrival(object):
	arTaskTime = 0
	arWorkerTime = 0
	flag = 0
	arTask = [] #到着したタスク
	arWorker = [] #到着したワーカー

	def clear(self):
		self.arTask = []
		self.arWorker = []

class CrowdMaint(object):
	TIME = 0

	def __init__(self, Arrival, TaskIn):
		self.Arrival = Arrival
		self.TaskIn = TaskIn

	def arrivalTW(self): 
		self.Arrival.flag = 0
		if self.Arrival.arTaskTime == self.TIME:
			self.Arrival.arTaskTime += nextP_task(self.Arrival)
			print "- task arrival "
			self.Arrival.flag += 1 #フラグを立てる

		if self.Arrival.arWorkerTime == self.TIME:
			self.Arrival.arWorkerTime += nextP_worker(self.Arrival)
			print "= worker arrival ="
			self.Arrival.flag += 2	

	def updateTW(self):
		if self.Arrival.flag == 1:
			addTask(self.Arrival, self.TaskIn)
			self.Arrival.clear()
		elif self.Arrival.flag == 2:
			addWorker(self.Arrival, self.TaskIn)
			self.Arrival.clear()	
		elif self.Arrival.flag == 3:
			addTask(self.Arrival, self.TaskIn)
			addWorker(self.Arrival, self.TaskIn)
			self.Arrival.clear()

		if self.Arrival.flag != 0:
			TAlist = []
			for task in self.TaskIn.Tasks:
				TAlist.append(TaskAssign(task, ['0'] * len(self.TaskIn.Workers) ))
			self.TaskIn.TAlist = TAlist

	def optimalOn(self):
		if self.TaskIn.Tasks != [] and self.TaskIn.Workers != []:
			
			#TI = InitTaskIndex(self.TaskIn.Tasks, self.TaskIn.Workers)
			print "==="
			print self.TaskIn.TAlist
			print self.TaskIn.Workers
			print self.TaskIn.Tasks
			for worker in self.TaskIn.Workers:
				print worker.X
			if self.TaskIn.TAlist != []:
				for i in range (len(self.TaskIn.TAlist)):
					print "v", self.TaskIn.TAlist[i].v_t
				for i in range (len(self.TaskIn.TAlist)):
					print "u", self.TaskIn.TAlist[i].u_t
			print self.TaskIn.finWorkers
			print self.TaskIn.finTasks
			print self.TaskIn.V
			print "==="

			TI = InitTaskIndex(self.TaskIn.Tasks, self.TaskIn.Workers)
			TI.V = self.TaskIn.V
			TI.finWorkers = self.TaskIn.finWorkers
			TI.finTasks = self.TaskIn.finTasks
			self.TaskIn = AssignWorker(0, self.TaskIn, TI)
			
			print "++++"
			print self.TaskIn.TAlist
			print self.TaskIn.Workers
			print self.TaskIn.Tasks
			for worker in self.TaskIn.Workers:
				print worker.X
			if self.TaskIn.TAlist != []:
				for i in range (len(self.TaskIn.TAlist)):
					print "v", self.TaskIn.TAlist[i].v_t
				for i in range (len(self.TaskIn.TAlist)):
					print "u", self.TaskIn.TAlist[i].u_t
			print self.TaskIn.finWorkers
			print self.TaskIn.finTasks
			print self.TaskIn.V
			print "++++"

			assignAndUpdateTI(self.TaskIn) # Task、Worker振り分け
			
	def ahead(self): # 1ユニットの間にすること
		self.arrivalTW()
		if self.Arrival.flag > 0:
			self.updateTW() # タスク・ワーカーの情報の変更
			self.optimalOn() # インデックスアップデート	 
		self.TIME += 1 #　1時間1ユニットとすると？

def assignAndUpdateTI(TaskIn):
	dt_count = 0 #今回消すタスク
	
	print "llllllllllllllllllll"
	print TaskIn.TAlist
	print TaskIn.Workers
	print TaskIn.Tasks
	for worker in TaskIn.Workers:
		print worker.X
	if TaskIn.TAlist != []:
		for i in range (len(TaskIn.TAlist)):
			print "v", TaskIn.TAlist[i].v_t
		for i in range (len(TaskIn.TAlist)):
			print "u", TaskIn.TAlist[i].u_t
	print TaskIn.finWorkers
	print TaskIn.finTasks
	print TaskIn.V
	print "llllllllllllllllllll"


	for i in range(len(TaskIn.TAlist)): #成功したタスクに印をつける
		if TaskIn.TAlist[i-dt_count].v_t != 0: #v_tが0でない、つまり成功したタスク
			
			for j in range(len(TaskIn.Workers)):
				TaskIn.Workers[j].X += int(TaskIn.TAlist[i-dt_count].u_t[j]) #Xに格納 #Xに格納して大丈夫か？

			del TaskIn.TAlist[i-dt_count] #タスク消去
			del TaskIn.Tasks[i-dt_count]
			dt_count += 1
			TaskIn.finTasks += 1


	print "BBBBBBBBBBBBBBBB"
	print TaskIn.TAlist
	print TaskIn.Workers
	print TaskIn.Tasks
	for worker in TaskIn.Workers:
		print worker.X
	if TaskIn.TAlist != []:
		for i in range (len(TaskIn.TAlist)):
			print "v", TaskIn.TAlist[i].v_t
		for i in range (len(TaskIn.TAlist)):
			print "u", TaskIn.TAlist[i].u_t
	print TaskIn.finWorkers
	print TaskIn.finTasks
	print TaskIn.V
	print "BBBBBBBBBBBBBBBB"

	dw_count = 0
	for j in range(len(TaskIn.Workers)):
		if TaskIn.Workers[j-dw_count].X == Xh:
			del TaskIn.Workers[j-dw_count] #ワーカー消去
			for TA in TaskIn.TAlist:
				del TA.u_t[j-dw_count]
			dw_count += 1 #今回卒業するワーカー
			TaskIn.finWorkers += 1

		elif TaskIn.Workers[j-dw_count].X > Xh:
			assert("Over Capacity(Xh) of a Worker")
			
	return TaskIn

def addTask(Arrival, TaskIn):
	if isinstance(Arrival.arTask, list):
		for ar_task in Arrival.arTask:
			TaskIn.Tasks.append(ar_task)
	else:
		TaskIn.Tasks.append(Arrival.arTask)

def addWorker(Arrival, TaskIn):
	if isinstance(Arrival.arWorker, list):
		for ar_worker in Arrival.arWorker:
			TaskIn.Workers.append(ar_worker)
	else:
		TaskIn.Workers.append(Arrival.arWorker)

def nextP_worker(Arrival):
	if isinstance(Arrival.arWorker, list) != True:
		Arrival.arWorker = [Arrival.arWorker]
	u = random.choice(U)
	u.X = 0
	Arrival.arWorker.append(u) #ワーカー加える
#	Arrival.arWorker.append(random.choice(U)) #ワーカー加える
	next_p = poisson(lam = IntervalWorker) #次のワーカーの時間
	if next_p == 0:
		next_p = nextP_worker(Arrival)
	return next_p

def nextP_task(Arrival):
	if isinstance(Arrival.arTask, list) != True:
		Arrival.arTask = [Arrival.arTask]
	Arrival.arTask.append(random.choice(T)) #ワーカー加える
	next_p = poisson(lam = IntervalTask) #次のワーカーの時間
	if next_p == 0:
		next_p = nextP_task(Arrival)
	return next_p
