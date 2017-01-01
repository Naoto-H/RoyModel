# Coded by Naoto Hayashi
# coding: UTF-8

import numpy as np
from numpy.random import *
from numpy import *

C1 = C2 = 0.5
Xh = 2

class Worker(object):
	X = 0
	def __init__(self, q_s1, q_s2, wage, p):
		self.q_s1 = q_s1	# IT skill
		self.q_s2 = q_s2	# Circuit sill
		self.wage = wage #minimum wage for which she is willing to accept a task
		self.p = p	#possibility to accept a task 

class Task(object):
	def __init__(self, Q_s1, Q_s2, Wage, P):
		self.Q_s1 = Q_s1
		self.Q_s2 = Q_s2
		self.Wage = Wage
		self.P = P

class TaskAssign(object):
	v_t = 0
	def __init__(self, task, u_t):
		self.task = task
		self.u_t = u_t

class TaskIndex(object):
	V = 0
	Workers = []
	Tasks = []
	finWorkers = 0
	finTasks = 0

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

def InitTaskIndex(Tasks, Workers):
	TAlist = [] #新規の場合
	for task in Tasks:
		TAlist.append(TaskAssign(task, ['0'] * len(Workers) ))
	TI = TaskIndex(TAlist) #TAlist
	TI.Workers = Workers
	TI.Tasks = Tasks
	return TI

def CopyTI(TI1, TI2): #T1をT2にコピー
	TI2.V = TI1.V
	TI2.Workers = TI1.Workers
	TI2.Tasks = TI1.Tasks
	TI2.finWorkers = TI1.finWorkers
	TI2.finTasks = TI1.finTasks

	for i in range(len(TI1.TAlist)):
		TI2.TAlist[i].task = TI1.TAlist[i].task
		TI2.TAlist[i].v_t = TI1.TAlist[i].v_t
		TI2.TAlist[i].u_t = TI1.TAlist[i].u_t

def AssignWorker(i, TI, OptimalTI):
	if i == 0:
		OptimalTI.V = TI.V
		OptimalTI.finWorkers = TI.finWorkers
		OptimalTI.finTasks = TI.finTasks

	for j in range( 2 ** len(TI.TAlist[0].u_t) ): #2^nのパターン数

		if see_Xh(TI, Xh, i-1) == False:
			print u"じぇじぇじぇXh"
			break

		TI.TAlist[i].u_t = binCon(j, len(TI.TAlist[0].u_t))		

		if (i > 0) and (cul_wage(TI.TAlist[i-1].u_t, TI.Workers) > TI.TAlist[i-1].task.Wage):
			print u"じぇじぇじぇWage"
			break

		TI.TAlist[i].v_t = value(TI.TAlist[i].task, TI.TAlist[i].u_t, TI.Workers)
		
		if i == ( len(TI.TAlist)-1 ): #最後の列まで行った場合
			if checkXh(TI, Xh) == True:
				print "iiiiiiii"
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
				print TI.V
				print "iiiiiiii"

				print "oooooooooo"
				print OptimalTI.TAlist
				print OptimalTI.Workers
				print OptimalTI.Tasks
				if OptimalTI.TAlist != []:
					for i in range (len(OptimalTI.TAlist)):
						print "v", OptimalTI.TAlist[i].v_t
					for i in range (len(OptimalTI.TAlist)):
						print "u", OptimalTI.TAlist[i].u_t
				print OptimalTI.finWorkers
				print OptimalTI.finTasks
				print OptimalTI.V
				print "oooooooooo"

				if TI.cul_V() > OptimalTI.cul_V(): #ここではVに足されない
					
					CopyTI(TI, OptimalTI)
					OptimalTI.update_sumV() #ここでVに足される

					print "^^^"
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
					print TI.V
					print "^^^"

					print "---"
					print OptimalTI.TAlist
					print OptimalTI.Workers
					print OptimalTI.Tasks
					if OptimalTI.TAlist != []:
						for i in range (len(OptimalTI.TAlist)):
							print "v", OptimalTI.TAlist[i].v_t
						for i in range (len(OptimalTI.TAlist)):
							print "u", OptimalTI.TAlist[i].u_t
					print OptimalTI.finWorkers
					print OptimalTI.finTasks
					print OptimalTI.V
					print "---"

		else:
			OptimalTI = AssignWorker(i+1, TI, OptimalTI)
	
		print "666666"
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
		print TI.V
		print "666666"

		print "333333"
		print OptimalTI.TAlist
		print OptimalTI.Workers
		print OptimalTI.Tasks
		if OptimalTI.TAlist != []:
			for i in range (len(OptimalTI.TAlist)):
				print "v", OptimalTI.TAlist[i].v_t
			for i in range (len(OptimalTI.TAlist)):
				print "u", OptimalTI.TAlist[i].u_t
		print OptimalTI.finWorkers
		print OptimalTI.finTasks
		print OptimalTI.V
		print "3333333"

	return OptimalTI

def cul_wage(u_t, Workers):
	wage_t = 0
	if u_t == [] or Workers == []:
		wage_t = 0
	else:
		for i in range(len(u_t)):
			wage_t += int(u_t[i]) * Workers[i].p * Workers[i].wage
	return wage_t

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

def checkXh(TI, h):
	for j in range(len(TI.Workers)):
		flag = 0
		for i in range(len(TI.TAlist)):
			flag += int(TI.TAlist[i].u_t[j])
		if flag > h:
			return False
	return True

def value(t, u_t, Workers): #v_t関数定義
	q_t_s1 = q_t_s2 = wage_t = 0
	if u_t == [] or Workers == []:
		q_t_s1 = q_t_s2 = wage_t = 0
	else:
		for i in range(len(u_t)):
			q_t_s1 += int(u_t[i]) * Workers[i].p * Workers[i].q_s1 
			q_t_s2 += int(u_t[i]) * Workers[i].p * Workers[i].q_s2 
			wage_t += int(u_t[i]) * Workers[i].p * Workers[i].wage

	v_t = C1 * (q_t_s1 + q_t_s2) + C2 * (1 - wage_t/t.Wage)
	if q_t_s1 >= t.Q_s1 and q_t_s2 >= t.Q_s2 and wage_t <= t.Wage: 
		return v_t
	else:
		return 0

def binCon(i, l): #二進法に変換
	u_t = str(bin(i))[2:]
	if len(u_t) != l:
		u_t = '0' *( l - len(u_t) ) + u_t
	ut = []
	for u in u_t:
		ut.append(u)
	return ut