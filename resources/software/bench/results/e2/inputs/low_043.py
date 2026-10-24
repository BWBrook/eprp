#!/usr/bin/env python
from numpy import *

data_1=[array([24.575048]),
array([15.391082,10.120269,9.644399,5.590581]),
array([18.256069,14.973436,6.007161,5.967472,4.798628,0.000000]),
array([20.019512]),
array([12.853023]),
array([12.082693]),
array([18.275272]),
array([1.774810,0.000000]),
array([7.290423,0.000000]),
array([8.283584,0.876790]),
array([4.218195,2.070573,0.000000]),
array([1.873143,0.000000]),
array([6.672430,5.729215,3.659065,1.529488]),
array([0.388865,0.000000]),
array([5.284216,4.529796,4.209933]),
array([0.515051])]
d=[data_1]
names=['low_043']
def get_data(i): return d[i]
def get_out_name(i): return names[i]
taxa_names=['t1','t5','t6','t8','t11','t12','t14','t16','t22','t25','t26','t27','t28','t30','t31','t34']
def get_taxa_names(): return taxa_names
