#!/usr/bin/python

'''
This script takes table output from Pf_popgenome_analysis.md for calculating
Fst, Kst and Dxy to determine population separation. Pull out high confidence
and low confidence genes for further analysis.
'''

import argparse
from collections import defaultdict
import os

ap = argparse.ArgumentParser()
ap.add_argument('--Fst_File', required=True, type=str, help='Tab separated text \
file of Fst values per gene')
ap.add_argument('--Kst_File', required=True, type=str, help='Tab separated text \
file of Kst values per gene')
ap.add_argument('--Dxy_File', required=True, type=str, help='Tab separated text \
file of Dxy values per gene')
ap.add_argument('--Out_Dir', required=True, type=str, help='Output directory')
ap.add_argument('--Out_Prefix', required=True, type=str, help='Prefix for output \
file')
conf = ap.parse_args()

# -----------------------------------------------------
# Step 1
# Load input files and build data structures
# -----------------------------------------------------

Fst_in = conf.Fst_File
Kst_in = conf.Kst_File
Dxy_in = conf.Dxy_File
OutDir = conf.Out_Dir
OutPre = conf.Out_Prefix
cwd = os.getcwd()

print("Arguments parsed")

# Create data structures

Fst_dict = defaultdict(float)
Kst_dict = defaultdict(float)
Dxy_dict = defaultdict(float)

with open(Fst_in) as f:
    lines = f.readlines()
    for line in lines:
        split_line = line.split()
        ID_field = split_line[0]
        ID_split = ID_field.split('=')
        Gene_ID = ID_split[1]
        Fst_Value = split_line[1]
        Fst_dict[Gene_ID] = Fst_Value

with open(Kst_in) as f:
    lines = f.readlines()
    for line in lines:
        split_line = line.split()
        ID_field = split_line[0]
        ID_split = ID_field.split('=')
        Gene_ID = ID_split[1]
        Kst_Value = split_line[1]
        Kst_dict[Gene_ID] = Kst_Value

with open(Dyx_in) as f:
    lines = f.readlines()
    for line in lines:
        split_line = line.split()
        ID_field = split_line[3]
        ID_split = ID_field.split('=')
        Gene_ID = ID_split[1]
        Dxy_Value = split_line[4]
        Dxy_dict[Gene_ID] = Dxy_Value
