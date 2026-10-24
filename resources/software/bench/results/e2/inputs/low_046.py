#!/usr/bin/env python
from numpy import *

data_1=[array([20.574152]),
array([24.751149,23.590611]),
array([21.949488]),
array([16.600362]),
array([12.844102]),
array([11.961367]),
array([6.833516,6.087101,3.746362,3.414361,2.481459,0.000000]),
array([10.232869]),
array([6.293617]),
array([11.613300]),
array([3.510537]),
array([4.611124]),
array([1.858799,1.793573,0.000000]),
array([9.955053]),
array([5.938355,0.655686,0.000000]),
array([5.895039]),
array([6.525382]),
array([3.698954,3.175954]),
array([3.786525,0.516494,0.000000])]
d=[data_1]
names=['low_046']
def get_data(i): return d[i]
def get_out_name(i): return names[i]
taxa_names=['t1','t2','t6','t7','t9','t10','t12','t17','t21','t23','t25','t29','t32','t33','t34','t35','t41','t42','t43']
def get_taxa_names(): return taxa_names
