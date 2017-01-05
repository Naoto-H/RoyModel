# Coded by Naoto Hayashi
# coding: UTF-8

from numpy import *
from numpy.random import *
from royModel_optimal import *

seed(7)
#794

PATTERN = 2
# 0 日本都市
# 1 日本農村
# 2 インド都市
# 3 インド農村

TLOAD = 1000
WORKER = 1000
LIFELIMIT = 12 #タスクの寿命

#1つのシステムにおけるタスクの種類
Tkind = [Task(0.7, 0.7, 10), #1
	Task(0.7, 0.1, 5), #2
	Task(0.3, 0.1, 2.5), #3
	Task(0.7, 0.1, 5), #4
	Task(0.3, 0.1, 2.5), #5
	Task(0.1, 0.1, 2.5), #6
	Task(0.1, 0.1, 2.5), #7
	Task(0.5, 0.3, 5), #8
	Task(0.1, 0.4, 3), #9
	Task(0.1, 0.3, 2.5), #10
	Task(0.1, 0.2, 5), #11
	Task(0.1, 0.4, 5)  #12
	]

#タスクが1つのシステムにおいて起きる確率
weight = [0.1, 0.02, 0.15, 0.02, 
	0.02, 0.15, 0.02, 0.02,
	0.15, 0.1, 0.15, 0.1]

if sum(weight) != 1:
	assert("the sum of weight probability should be 1")

def taskSetting(task):
	task.lifetime = LIFELIMIT

#タスクとタスク量定義
T = []
for i in range(TLOAD):
	t = random.choice(Tkind, p=weight)
	taskSetting(t)
	T.append(t)

def p_norm(m, v):
	a = normal(m, v)
	if a < 0:
		a = p_norm(m, v)
	return a

def p_normOne(m, v):
	a = normal(m, v)
	if a < 0 or a > 1:
		a = p_normOne(m, v)
	return a

if PATTERN == 0 or PATTERN == 1: #japan
	w = 1

if PATTERN == 2 or PATTERN == 3: #india
	w = 0.5

for i in range(WORKER):
	if i == 0:
		d = []
		x_s1 = [] 
		x_s2 = [] 
		y = []
		p = []
		wtr = [] #住民の基本レベル
	if PATTERN == 0: #日本都市
		d.append(p_normOne(0.5, 0.2))
		y.append(p_norm(4, 1)) #賃金の倍率
		wtr.append(p_norm(0.6, 0.2) * w)
	if PATTERN == 1: #日本農村
		d.append(p_normOne(0.4, 0.2))
		y.append(p_norm(4, 1)) #賃金の倍率
		wtr.append( d[i] * p_norm(3, 1.5) * w)
	if PATTERN == 2: #インド都市
		d.append(p_normOne(0.4, 0.25)) 
		y.append(p_norm(2.5, 0.625)) #賃金の倍率
		wtr.append(p_norm(0.6, 0.2) * w)
	if PATTERN == 3: #インド農村
		d.append(p_normOne(0.3, 0.2)) 
		y.append(p_norm(2.5, 0.625)) #賃金の倍率
		wtr.append( d[i] * p_norm(3, 1.5) * w)
	
	x_s1.append(p_norm(0.7, 0.15)) #スキル1の倍率
	x_s2.append(p_norm(0.6, 0.2)) #スキル2の倍率 
	p.append(p_normOne(0.5, 0.2)) #受注率

U = []
for i in range(WORKER):
	u = Worker(d[i]*x_s1[i], d[i]*x_s2[i], d[i]*y[i], p[i], wtr[i])
	U.append(u)
