#!/usr/bin/python

'''
This script uses the output of DeSeq2 to produce a list of genes that are expressed only in a single isolate and add orthogroup ID for each gene
'''

import sys,argparse
from sets import Set
from collections import defaultdict
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('--FPKM_in',required=True,type=str,help='text output file from DeSeq2 commands of non-normalised FPKM values')
ap.add_argument('--Orthogroup_in',required=True,type=str,help='text output file of Orthogroups from OrthoFinder')
ap.add_argument('--Output_1',required=True,type=str,help='Output text file for isolate 1')
ap.add_argument('--Output_2',required=True,type=str,help='Output text file for isolate 2')
ap.add_argument('--Output_3',required=True,type=str,help='Output text file for isolate 3')
conf = ap.parse_args()

#-----------------------------------------------------
# Step 1
# Load input files, create sets and dictionaries
#-----------------------------------------------------
