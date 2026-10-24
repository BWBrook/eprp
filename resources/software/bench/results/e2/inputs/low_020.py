#!/usr/bin/env python
from numpy import *

data_1=[array([16.217746]),
array([7.356293]),
array([3.145772]),
array([9.865972]),
array([5.782706,0.016057,0.000000]),
array([7.031598,2.402348,0.000000]),
array([3.870033]),
array([8.600419]),
array([4.354307,3.102213,0.000000]),
array([5.146774,0.972305,0.000000]),
array([4.423268]),
array([3.344979]),
array([1.472140,1.269196]),
array([1.598491]),
array([0.409820,0.000000]),
array([2.415180,2.403532,0.000000]),
array([0.735994]),
array([0.332754,0.000000])]
d=[data_1]
names=['low_020']
def get_data(i): return d[i]
def get_out_name(i): return names[i]
taxa_names=['t1','t3','t5','t7','t8','t9','t11','t12','t19','t21','t22','t23','t24','t26','t27','t28','t34','t35']
def get_taxa_names(): return taxa_names
