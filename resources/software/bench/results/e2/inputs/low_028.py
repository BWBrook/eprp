#!/usr/bin/env python
from numpy import *

data_1=[array([16.489569]),
array([19.754594]),
array([15.953553]),
array([17.239350,9.257372]),
array([15.326598]),
array([6.945436,6.100637,0.072440,0.000000]),
array([8.392212,3.734662,0.000000]),
array([10.021971,8.954276,4.883460]),
array([2.718732,2.000978]),
array([1.008559,0.000000]),
array([1.283807,0.000000]),
array([7.357376]),
array([4.694410,0.328236,0.000000]),
array([0.716100,0.000000]),
array([2.825246]),
array([2.185889])]
d=[data_1]
names=['low_028']
def get_data(i): return d[i]
def get_out_name(i): return names[i]
taxa_names=['t2','t3','t4','t5','t7','t10','t12','t13','t15','t17','t18','t22','t31','t34','t36','t40']
def get_taxa_names(): return taxa_names
