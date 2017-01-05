# Coded by Naoto Hayashi
# coding: UTF-8

from numpy import *

C1 = C2 = 0.5
Xh = 2

class Worker(object):
	X = 0 #現在引き受けている仕事の数
	def __init__(self, q_s1, q_s2, wage, p, w_tr):
		self.q_s1 = q_s1	# IT skill
		self.q_s2 = q_s2	# Circuit sill
		self.wage = wage #minimum wage for which she is willing to accept a task
		self.p = p	#possibility to accept a task 
		self.w_tr = w_tr

class Task(object):
	lifetime = 0

	def __init__(self, Q_s1, Q_s2, Wage):
		self.Q_s1 = Q_s1
		self.Q_s2 = Q_s2
		self.Wage = Wage

class TaskAssign(object):
	v_t = 0
	w_t = 0
	q_t = 0
	def __init__(self, task, u_t):
		self.task = task
		self.u_t = u_t

class TaskIndex(object):
	V = 0
	Workers = []
	Tasks = []
	finWorkers = 0
	finTasks = 0
	failTasks = 0
	Wage = 0
	Quality = 0

	def __init__(self, TAlist):
		self.TAlist = TAlist #TaskAssingクラスのリスト
	
	def	cul_V(self):
		v = 0
		for TA in self.TAlist:
			v += TA.v_t
		return v

	def cul_sumV(self):
		V = self.V
		for TA in self.TAlist:
			V += TA.v_t
		return V

	def update_sumV(self):
		for TA in self.TAlist:
			self.V += TA.v_t
		return self.V

	def update_sumWage(self):
		for TA in self.TAlist:
			self.Wage += TA.w_t
		return self.Wage

	def update_sumQuality(self):
		for TA in self.TAlist:
			self.Quality += TA.q_t
		return self.Quality

def initTaskIndex(Tasks, Workers):
	TAlist = [] #新規の場合
	for task in Tasks:
		TAlist.append(TaskAssign(task, ['0'] * len(Workers) ))
	TI = TaskIndex(TAlist) #TAlist
	TI.Workers = Workers
	TI.Tasks = Tasks
	return TI

def copyTI(TI1, TI2): #T1をT2にコピー
	TI2.V = TI1.V
	TI2.Workers = TI1.Workers
	TI2.Tasks = TI1.Tasks
	TI2.finWorkers = TI1.finWorkers
	TI2.finTasks = TI1.finTasks
	TI2.failTasks = TI1.failTasks
	TI2.Wage = TI1.Wage
	TI2.Quality = TI1.Quality

	for i in range(len(TI1.TAlist)):
		TI2.TAlist[i].task = TI1.TAlist[i].task
		TI2.TAlist[i].v_t = TI1.TAlist[i].v_t
		TI2.TAlist[i].w_t = TI1.TAlist[i].w_t
		TI2.TAlist[i].u_t = TI1.TAlist[i].u_t
		TI2.TAlist[i].q_t = TI1.TAlist[i].q_t

def assignWorker(i, TI, OptimalTI):
	for j in range( 2 ** len(TI.TAlist[0].u_t) ): #2^nのパターン数

		if see_Xh(TI, Xh, i-1) == False:
			break
		TI.TAlist[i].u_t = binCon(j, len(TI.TAlist[0].u_t))
		
		if (i > 0) and (cul_wage(TI.TAlist[i-1].u_t, TI.Workers) > TI.TAlist[i-1].task.Wage):
			break
		TI.TAlist[i].v_t = value(TI.TAlist[i].task, TI.TAlist[i].u_t, TI.Workers)
		TI.TAlist[i].w_t = cul_wage(TI.TAlist[i].u_t, TI.Workers)
		TI.TAlist[i].q_t = cul_quality(TI.TAlist[i].u_t, TI.Workers)
		
		if i == ( len(TI.TAlist)-1 ): #最後の列まで行った場合
			if checkXh(TI, Xh) == True:				
				if TI.cul_V() > OptimalTI.cul_V() : #ここではVに足されない
					copyTI(TI, OptimalTI)
					OptimalTI.update_sumV() #ここでVに足される
					OptimalTI.update_sumWage()
					OptimalTI.update_sumQuality()

		else:
			OptimalTI = assignWorker(i+1, TI, OptimalTI)
	
	#print "666666"
	#printTI(TI)
	#print "666666"

	#print "333333"
	#printTI(OptimalTI)
	#print "3333333"
	
	return OptimalTI


def checkXh(TI, h):
	for j in range(len(TI.Workers)):
		flag = TI.Workers[j].X
		for i in range(len(TI.TAlist)):
			flag += int(TI.TAlist[i].u_t[j])
		if flag > h:
			return False
	return True

def see_Xh(TI, h, k): #k行目まででXhをチェック
	if k < 1:
		return True

	for j in range(len(TI.Workers)):
		flag = TI.Workers[j].X
		for i in range(k):
			flag += int(TI.TAlist[i].u_t[j])
		if flag > h:
			return False
	return True

def value(t, u_t, Workers): #v_t関数定義
	q_t_s1 = q_t_s2 = wage_t = 0
	if u_t == [] or Workers == []:
		return 0
	else:
		for i in range(len(u_t)):
			q_t_s1 += int(u_t[i]) * Workers[i].p * Workers[i].q_s1 
			q_t_s2 += int(u_t[i]) * Workers[i].p * Workers[i].q_s2 
			wage_t += int(u_t[i]) * Workers[i].p * ( Workers[i].wage + Workers[i].w_tr)

	v_t = C1 * (q_t_s1 + q_t_s2) + C2 * (1 - wage_t/t.Wage)

	if q_t_s1 >= t.Q_s1 and q_t_s2 >= t.Q_s2 and wage_t <= t.Wage: 
		return v_t
	else:
		return 0

def cul_wage(u_t, Workers):
	wage_t = 0
	if u_t == [] or Workers == []:
		wage_t = 0
	else:
		for i in range(len(u_t)):
			wage_t += int(u_t[i]) * Workers[i].p * Workers[i].wage
	return wage_t

def cul_quality(u_t, Workers):
	q_t = 0
	if u_t == [] or Workers == []:
		q_t = 0
	else:
		for i in range(len(u_t)):
			q_t += int(u_t[i]) * Workers[i].p * Workers[i].q_s1 + int(u_t[i]) * Workers[i].p * Workers[i].q_s2
	return q_t

def binCon(i, l): #二進法に変換
	u_t = str(bin(i))[2:]
	if len(u_t) != l:
		u_t = '0' *( l - len(u_t) ) + u_t
	ut = []
	for u in u_t:
		ut.append(u)
	return ut

def printTI(TI):
	print TI.TAlist
	print TI.Workers
	print TI.Tasks
	if TI.TAlist != []:
		for i in range (len(TI.TAlist)):
			print "v", TI.TAlist[i].v_t
		for i in range (len(TI.TAlist)):
			print "u", TI.TAlist[i].u_t
	print TI.finWorkers
	print TI.finTasks
	print TI.failTasks
	print TI.V
	print TI.Wage
	print TI.Quality