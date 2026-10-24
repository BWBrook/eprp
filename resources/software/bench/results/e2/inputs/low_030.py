#!/usr/bin/env python
from numpy import *

data_1=[array([21.504891]),
array([18.894057,16.381277]),
array([11.441017,11.188023]),
array([9.947769,8.531971,7.269222,2.726370,0.000000]),
array([9.222495]),
array([7.216517,6.771694]),
array([1.827618]),
array([3.505414]),
array([2.977780,0.000000]),
array([4.829046]),
array([4.785441]),
array([3.130828]),
array([3.446192]),
array([0.664931,0.392037,0.170661,0.000000])]
d=[data_1]
names=['low_030']
def get_data(i): return d[i]
def get_out_name(i): return names[i]
taxa_names=['t1','t3','t6','t10','t12','t17','t18','t19','t20','t22','t23','t24','t29','t31']
def get_taxa_names(): return taxa_names
