#!/usr/bin/env python
from numpy import *

data_1=[array([24.245988,24.182085,20.501458,17.497784,13.892443,4.934742,2.554924]),
array([9.973079,7.038572]),
array([2.693673,0.000000]),
array([3.718026]),
array([8.402624,4.256628,0.000000]),
array([6.030246]),
array([3.336197]),
array([6.512380,5.423646,2.360575,1.981527,0.000000]),
array([5.965803,0.000000]),
array([4.624974]),
array([1.915357,0.000000]),
array([1.444787,0.000000]),
array([0.215653,0.000000]),
array([1.752713,0.000000]),
array([2.270491,1.046623,0.633773,0.000000])]
d=[data_1]
names=['low_050']
def get_data(i): return d[i]
def get_out_name(i): return names[i]
taxa_names=['t1','t4','t6','t7','t8','t9','t10','t12','t19','t20','t21','t22','t25','t27','t28']
def get_taxa_names(): return taxa_names
