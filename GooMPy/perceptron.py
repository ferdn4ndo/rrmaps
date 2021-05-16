#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import choice 
from numpy import array, dot, random 

unit_step = lambda x: 0 if x < 0 else 1 

training_data = [ 
	(array([11,1280,1792,450,316]), array([900,633])),
	(array([12,2048,3584,900,633]), array([1288,1266])),
	(array([13,4096,6400,1288,1266]), array([2579,2023])),
	(array([14,7424,12800,2579,2023]), array([4903,4046])),
	(array([15,14848,25088,4903,4046]), array([9807,7839])),
	(array([16,29440,50176,9807,7839]), array([19615,15678])),
] 

w = random.rand(5) 
errors = [] 
eta = 0.2 
n = 100 

for i in xrange(n): 
	x, expected = choice(training_data) 
	result = dot(w, x) 
	error = expected - unit_step(result) 
	print "error",error
	errors.append(error) 
	w += eta * error * x 

for x, _ in training_data: 
	result = dot(x, w) 
	print("{}: {} -> {}".format(x[:2], result, unit_step(result)))