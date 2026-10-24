#!/usr/bin/env python
from numpy import *

data_1=[array([24.368482]),
array([21.457434,21.190041]),
array([24.512572]),
array([21.944505,14.913645]),
array([22.355989]),
array([21.874895,20.266981]),
array([19.476263]),
array([14.987813]),
array([13.639009]),
array([19.899815]),
array([13.647072,13.568923]),
array([6.626236,3.403750,2.155529,0.000000]),
array([7.142822,2.619201]),
array([5.502711]),
array([5.581506]),
array([3.838799,0.000000]),
array([3.950178,0.707524,0.212947,0.000000]),
array([5.959940]),
array([2.739848,0.716764,0.000000])]
d=[data_1]
names=['low_023']
def get_data(i): return d[i]
def get_out_name(i): return names[i]
taxa_names=['t1','t2','t4','t5','t6','t7','t8','t9','t10','t11','t14','t15','t17','t18','t20','t21','t24','t25','t32']
def get_taxa_names(): return taxa_names
