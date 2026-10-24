#!/usr/bin/env python
from numpy import *

data_1=[array([22.557258,21.818416,21.129814]),
array([21.862093,18.113360]),
array([16.452833,15.301398,10.788912]),
array([17.969481]),
array([10.410197]),
array([7.368690,0.108838,0.000000]),
array([6.438613,6.060210,5.309463]),
array([3.449049]),
array([1.056508,0.000000]),
array([2.041303,0.685219,0.081009,0.000000]),
array([0.424497,0.000000]),
array([0.188321,0.000000])]
d=[data_1]
names=['low_024']
def get_data(i): return d[i]
def get_out_name(i): return names[i]
taxa_names=['t1','t2','t3','t4','t5','t10','t11','t12','t14','t15','t16','t28']
def get_taxa_names(): return taxa_names
