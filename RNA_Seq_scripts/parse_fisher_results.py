#!/usr/bin/python

'''
This script will analyse results from a Fishers Exact Test on enrichment
for RxLRs, CRNs, ApoplastP hits and combined Effectors vs the genome
With significance thresholds of: 0.1, 0.05, 0.01 and 0.001
'''

import argparse
from collections import defaultdict
import os

# -----------------------------------------------------
# Step 1
# Import variables
# -----------------------------------------------------

ap = argparse.ArgumentParser()
ap.add_argument('--inputs', required=True, type=str, nargs='+', help='List of \
files from all Fisher tests')
ap.add_argument('--outdir', required=True, type=str, help='Directory to output \
results to')
conf = ap.parse_args()

cwd = os.getcwd()

# -----------------------------------------------------
# Step 2
# Creates dictionary of each gene type in each option
# -----------------------------------------------------
