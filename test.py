# Coded by Naoto Hayashi
# coding: UTF-8

from numpy import *
from numpy.random import *
from royModel_optimal import *

seed(19)

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

for i in range(10):
	print p_normOne(0.3, 1) 