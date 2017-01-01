# Coded by Naoto Hayashi
# coding: UTF-8

import numpy as np
from numpy.random import *
from royModel_op import *

T = [Task(0.8, 0.8, 10, 0.1),	#1
	Task(0.8, 0.1, 5, 0.1),		#2
	Task(0.3, 0.1, 2.5, 0.1),	#3
	Task(0.8, 0.1, 5, 0.1),		#4
	Task(0.3, 0.1, 2.5, 0.1),	#5
	Task(0.1, 0.3, 2.5, 0.1),	#6
	Task(0.1, 0.2, 2.5, 0.1),	#7
	Task(0.6, 0.3, 5, 0.1),		#8
	Task(0.1, 0.4, 2.5, 0.05),	#9
	Task(0.1, 0.3, 2.5, 0.05),	#10
	Task(0.1, 0.2, 5, 0.05),	#11
	Task(0.1, 0.4, 5, 0.05),	#12
	]

d = []
for i in range(100):
	d.append(normal(1, 0.2))

x_s1 = []
for i in range(100):
	x_s1.append(normal(1000, 0.05))

x_s2 = []
for i in range(100):
	x_s2.append(normal(1000, 0.1))

y = []
for i in range(100):
	y.append(normal(0.1, 0.005))

p = []
for i in range(100):
	p.append(normal(0.5, 0.2))

#z = []
#for i in range(100):
#	z.append(normal(0.5, 0.2))

U = [Worker(0.6, 0.5, 0.8, 0.8),
	Worker(0.8, 0.6, 1, 0.6),
	Worker(0.3, 0.6, 0.4, 0.9),
	Worker(0.5, 0.5, 0.7, 0.9),
	Worker(0.3, 0.4, 0.6, 0.9)
	]

'''
U = []
for i in range(100):
	U.append( Worker(d[i]*x_s1[i], d[i]*x_s2[i], d[i]*y[i], p[i]) )
'''