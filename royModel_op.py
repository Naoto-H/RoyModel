# Coded by Naoto Hayashi
# coding: UTF-8

import numpy as np
from numpy.random import *
from numpy import *

C1 = C2 = 0.5

class Worker(object):
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
	def __init__(self, task, u_t):
		self.task = task
		self.v_t = 0
		self.u_t = u_t

class TaskIndex(object):
	def __init__(self, TAlist):
		self.TAlist = TAlist #TaskAssingクラスのリスト
		self.Workers = []
		self.Tasks = []
		self.V = 0
	
	def	cul_V(self):
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

def AssignWorker(i, TI, V_M, OptimalTI):
	for j in range( 2 ** len(TI.TAlist[0].u_t) ): #TA1について

		TI.TAlist[i].u_t = binCon(j, len(TI.TAlist[0].u_t))
		'''
		print "## TI ##"
		print TI.TAlist[0].u_t
		print TI.TAlist[1].u_t
		print TI.TAlist[0].v_t
		print TI.TAlist[1].v_t
		print i, j
		print "####"
		print "== op =="
		print OptimalTI.TAlist[0].u_t
		print OptimalTI.TAlist[1].u_t
		print OptimalTI.TAlist[0].v_t
		print OptimalTI.TAlist[1].v_t
		print i
		print "====="
		'''
		TI.TAlist[i].v_t = value(TI.TAlist[i].task, TI.TAlist[i].u_t, TI.Workers)
		'''
		print "####"
		print TI.TAlist[0].u_t
		print TI.TAlist[1].u_t
		print TI.TAlist[0].v_t
		print TI.TAlist[1].v_t
		print i, j
		print "####"
		print "===="
		print OptimalTI.TAlist[0].u_t
		print OptimalTI.TAlist[1].u_t
		print OptimalTI.TAlist[0].v_t
		print OptimalTI.TAlist[1].v_t
		print i
		print "====="
		'''
		if i == ( len(TI.TAlist)-1 ): #最後の列まで行った場合
			if checkXh(TI, 1) == True:				
				if TI.cul_V() > OptimalTI.cul_V():

					OptimalTI = TI
					'''
					print "^^ 更新 ^^"
					print OptimalTI.TAlist[0].u_t
					print OptimalTI.TAlist[1].u_t
					print OptimalTI.TAlist[0].v_t
					print OptimalTI.TAlist[1].v_t
					print i
					print "^^^^^^"
					'''
		else:
			OptimalTI = AssignWorker(i+1, TI, V_M, OptimalTI)	
	return OptimalTI
	
def checkXh(TI, Xh):
	for j in range(len(TI.Workers)):
		flag = 0
		for i in range(len(TI.TAlist)):
			flag += int(TI.TAlist[i].u_t[j])
		if flag > Xh:
			return False
	return True
'''
def sum_str(S):#['1','0']のような数字の文字列を入れたら合計が出る関数
	amount = 0
	for s in S:
		amount += int(s)
	return amount
'''
def value(t, u_t, Workers): #v_t関数定義
	q_t_s1 = q_t_s2 = wage_t = 0
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