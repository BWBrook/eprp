#!/usr/bin/env python
from numpy import *

data_1=[array([23.846129,21.355583]),
array([21.655953,15.734869,13.492804]),
array([14.643233]),
array([12.528676]),
array([20.055113,19.590778]),
array([14.644987]),
array([9.725012]),
array([11.866166,11.743539,10.609796,9.964838]),
array([16.036648]),
array([13.038710]),
array([8.908128]),
array([8.048507,6.488621]),
array([1.823429]),
array([5.639884,4.077174,3.568850,0.000000]),
array([6.440695,1.888726,0.000000]),
array([1.467557,0.000000]),
array([3.888238,2.691685]),
array([2.886339,2.351785,0.000000]),
array([1.074025,0.188533,0.000000])]
d=[data_1]
names=['low_035']
def get_data(i): return d[i]
def get_out_name(i): return names[i]
taxa_names=['t1','t3','t5','t7','t8','t9','t10','t11','t14','t16','t20','t22','t24','t26','t28','t29','t30','t31','t36']
def get_taxa_names(): return taxa_names
