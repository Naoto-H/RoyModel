# Coded by Naoto Hayashi
# coding: UTF-8

import numpy as np
from royModel_data import *
from royModel_optimal import *
from numpy import *

#ポアソン分布の定数

IntervalTask = 8
IntervalWorker = 5

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
			#print "- task arrival %d -" % len(self.Arrival.arTask)
			self.Arrival.flag += 1 #フラグを立てる

		if self.Arrival.arWorkerTime == self.TIME:
			self.Arrival.arWorkerTime += nextP_worker(self.Arrival)
			#print "= worker arrival %d =" % len(self.Arrival.arWorker)
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

	def optimal(self):
		if self.TaskIn.Tasks != [] and self.TaskIn.Workers != []:

			#print "==="
			#printTI(self.TaskIn)
			#print "==="

			TI = initTaskIndex(self.TaskIn.Tasks, self.TaskIn.Workers)
			TI.V = self.TaskIn.V
			TI.Wage = self.TaskIn.Wage
			TI.Quality = self.TaskIn.Quality
			TI.finWorkers = self.TaskIn.finWorkers
			TI.finTasks = self.TaskIn.finTasks
			TI.failTasks = self.TaskIn.failTasks
			self.TaskIn = assignWorker(0, self.TaskIn, TI)
			
			#print "++++"
			#printTI(self.TaskIn)
			#print "++++"

			assignAndUpdateTI(self.TaskIn) # Task、Worker振り分け
	
	def taskLifeTime(self): #lifetimeを減らし、0になったものを消す
		dt_count = 0

		if self.TaskIn.TAlist != []:
			for i in range(len(self.TaskIn.TAlist)):
				self.TaskIn.Tasks[i-dt_count].lifetime += -1 #self.TaskIn.TAlist[i-dt_count].task.lifetimeも同期して減る

				if self.TaskIn.TAlist[i-dt_count].task.lifetime < 0 or self.TaskIn.Tasks[i-dt_count].lifetime < 0:
					assert("Some tasks are overdue")
				if self.TaskIn.TAlist[i-dt_count].task.lifetime == 0 and self.TaskIn.Tasks[i-dt_count].lifetime == 0:
					del self.TaskIn.TAlist[i-dt_count]
					del self.TaskIn.Tasks[i-dt_count]
					dt_count += 1
					self.TaskIn.failTasks += 1
		
	def ahead(self): # 1ユニットの間にすること
		self.arrivalTW()
		if self.Arrival.flag > 0:
			self.updateTW() # タスク・ワーカーの情報の変更
			self.optimal() # インデックスアップデート
			#printTI(self.TaskIn)	 
			self.taskLifeTime()
		self.TIME += 1 #　1時間1ユニットとすると？

def assignAndUpdateTI(TaskIn):
	dt_count = 0 #今回消すタスク
	
	#print "@@@@@@@@@"
	#printTI(TaskIn)
	#print "@@@@@@@@@"

	for i in range(len(TaskIn.TAlist)): #成功したタスクに印をつける
		if TaskIn.TAlist[i-dt_count].v_t != 0: #v_tが0でない、つまり成功したタスク
			
			for j in range(len(TaskIn.Workers)):
				TaskIn.Workers[j].X += int(TaskIn.TAlist[i-dt_count].u_t[j]) #Xに格納 #Xに格納して大丈夫か？

			del TaskIn.TAlist[i-dt_count] #タスク消去
			del TaskIn.Tasks[i-dt_count]
			dt_count += 1
			TaskIn.finTasks += 1

	#print "::::::::::" 
	#printTI(TaskIn)
	#print "::::::::::"

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
	next_p = poisson(lam = IntervalWorker) #次のワーカーの時間
	if next_p == 0:
		next_p = nextP_worker(Arrival)
	return next_p

def nextP_task(Arrival):
	if isinstance(Arrival.arTask, list) != True:
		Arrival.arTask = [Arrival.arTask]
	t = random.choice(T)
	t.lifetime = LIFELIMIT
	Arrival.arTask.append(t) #ワーカー加える
	next_p = poisson(lam = IntervalTask) #次のワーカーの時間
	if next_p == 0:
		next_p = nextP_task(Arrival)
	return next_p