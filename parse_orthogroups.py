#!/usr/bin/python

'''
This script uses an orthology group txt file output from OrthoMCL to create a count table for the number of genes per strain in each orthogroup
'''

from sets import Set
import sys,argparse
from collections import defaultdict
import re

#-----------------------------------------------------
# Step 1
# Import variables & load input files
#-----------------------------------------------------

ap = argparse.ArgumentParser()
ap.add_argument('--orthogroups',required=True,type=str,help='text file output of OrthoMCL orthogroups')
ap.add_arguments('--out_dir',required=True,type=str,help='the directory where the count tble is output to')
conf = ap.parse_args()

with open(conf.orthogroups) as f:
    ortho_lines = f.readlines()

#-----------------------------------------------------
# Step 2
# Build a dictionary of orthogroups
#-----------------------------------------------------
