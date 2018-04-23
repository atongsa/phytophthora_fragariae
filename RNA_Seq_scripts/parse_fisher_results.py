#!/usr/bin/python

'''
This script will analyse results from a Fishers Exact Test on enrichment
for specified gene types, with a specified False Discovery Rate
and specified P-value threshold
'''

import argparse
from collections import defaultdict
import os
import statsmodels.sandbox.stats.multicomp as stats

# -----------------------------------------------------
# Step 1
# Import variables
# -----------------------------------------------------

ap = argparse.ArgumentParser()
ap.add_argument('--inputs', required=True, type=str, nargs='+', help='List of \
files from all Fisher tests')
ap.add_argument('--outdir', required=True, type=str, help='Directory to output \
results to')
ap.add_argument('--FDR', required=True, type=float, help='False Discovery rate \
for Benjamini-Hochberg multi-test correction')
ap.add_argument('--Types', required=True, type=str, nargs='+', help='List of \
genes types to parse the enrichment results of')
ap.add_argument('--Threshold', required=True, type=float, help='P-value at \
which the null hypothesis of no enrichment is accepted')
conf = ap.parse_args()

cwd = os.getcwd()

# -----------------------------------------------------
# Step 2
# Creates dictionary of each gene type in each option and corrects p-values
# -----------------------------------------------------

enrichment_dict = defaultdict(float)

keys = []
P_vals = []

Files = conf.inputs
for File in Files:
    with open(File) as f:
        Lines = f.readlines()
        for line in Lines:
            split_line = line.split()
            Module_ID = str(split_line[0])
            Gene_type = str(split_line[1])
            P_value = float(split_line[2])
            key = "_".join([Module_ID, Gene_type])
            keys.append(key)
            P_vals.append(P_value)

FDR = conf.FDR
Corrected_Pval_array = stats.multipletests(P_vals, alpha=FDR, method='fdr_bh',
                                           is_sorted=False, returnsorted=False)

i = 0
for key in keys:
    P_value = Corrected_Pval_array[1][i]
    enrichment_dict[key] = P_value
    i = i + 1

# -----------------------------------------------------
# Step 3
# Make a list of tests which pass p-value thresholds for writing out
# -----------------------------------------------------

Significant = []
Non_Significant = []

for key in keys:
    P_value = enrichment_dict[key]
    if P_value < 0.05:
        Significant.append(key)
    else:
        Non_Significant.append(key)

# -----------------------------------------------------
# Step 4
# Write out files
# -----------------------------------------------------

OutDir = conf.outdir
Header = "\t".join(["Module_Gene type", "P-value"])

# Threshold of 0.001

Out_File = "Significant_enrichment_0.001.tsv"
Output = "/".join([cwd, OutDir, Out_File])

with open(Output, 'w') as o:
    o.write(Header)
    o.write("\n")
    for item in Significant_1e3:
        P_value = enrichment_dict[item]
        to_write = "\t".join([item, str(P_value)])
        o.write(to_write)
        o.write("\n")

# Threshold of 0.01

Out_File = "Significant_enrichment_0.01.tsv"
Output = "/".join([cwd, OutDir, Out_File])

with open(Output, 'w') as o:
    o.write(Header)
    o.write("\n")
    for item in Significant_1e2:
        P_value = enrichment_dict[item]
        to_write = "\t".join([item, str(P_value)])
        o.write(to_write)
        o.write("\n")

# Threshold of 0.05

Out_File = "Significant_enrichment_0.05.tsv"
Output = "/".join([cwd, OutDir, Out_File])

with open(Output, 'w') as o:
    o.write(Header)
    o.write("\n")
    for item in Significant_5e2:
        P_value = enrichment_dict[item]
        to_write = "\t".join([item, str(P_value)])
        o.write(to_write)
        o.write("\n")

# Threshold of 0.1

Out_File = "Significant_enrichment_0.1.tsv"
Output = "/".join([cwd, OutDir, Out_File])

with open(Output, 'w') as o:
    o.write(Header)
    o.write("\n")
    for item in Significant_1e1:
        P_value = enrichment_dict[item]
        to_write = "\t".join([item, str(P_value)])
        o.write(to_write)
        o.write("\n")
