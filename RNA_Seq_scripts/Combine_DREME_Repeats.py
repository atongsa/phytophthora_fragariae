#!/usr/bin/python

'''
This script will analyse results from each repetition of DREME and extract
motifs present in a percentage of runs (value provided by user)
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
ap.add_argument('--inputs', required=True, type=str, help='Lists of files \
from repeated runs of DREME')
ap.add_argument('--percentage', required=True, type=float, help='Percentage \
of repeats where a motif must be significantly identified to be counted')
ap.add_argument(--'outdir', required=True, type=str, help='Directory to output \
results to')
conf = ap.parse_args()

cwd = os.getcwd()

# -----------------------------------------------------
# Step 2
# Load motifs and p-values into a dictionary
# -----------------------------------------------------

motif_dict = defaultdict(list)

Files = conf.inputs
for File in Files:
    with open(File) as f:
        Lines = f.readlines()
        for line in Lines:
            if line.startswith('# BEST'):
                list = line.split()
                P_val = list[6]
                Motif = [2]
                motif_dict[Motif].append(P_val)

# -----------------------------------------------------
# Step 3
# Count number of times motifs identified with a p-value below thresholds
# -----------------------------------------------------

Motifs = motif_dict.keys()

Percentage = conf.percentage
Num_Files_Sub = len(Files)

# Threshold of 0.1

Positive_Motifs_1 = []

for Motif in Motifs:
    P_values = motif_dict[Motif]
    Count = sum(1 for P_val in P_values if P_val <= 0.1)
    Count_Percent = (float(Count) / float(Num_Files_Sub)) * 100
    if Count_Percent >= Percentage:
        Positive_Motifs_1.append(Motif)

# Threshold of 0.05

Positive_Motifs_2 = []

for Motif in Motifs:
    P_values = motif_dict[Motif]
    Count = sum(1 for P_val in P_values if P_val <= 0.05)
    Count_Percent = (float(Count) / float(Num_Files_Sub)) * 100
    if Count_Percent >= Percentage:
        Positive_Motifs_2.append(Motif)

# Threshold of 0.01

Positive_Motifs_3 = []

for Motif in Motifs:
    P_values = motif_dict[Motif]
    Count = sum(1 for P_val in P_values if P_val <= 0.01)
    Count_Percent = (float(Count) / float(Num_Files_Sub)) * 100
    if Count_Percent >= Percentage:
        Positive_Motifs_3.append(Motif)

# Threshold of 0.001

Positive_Motifs_4 = []

for Motif in Motifs:
    P_values = motif_dict[Motif]
    Count = sum(1 for P_val in P_values if P_val <= 0.001)
    Count_Percent = (float(Count) / float(Num_Files_Sub)) * 100
    if Count_Percent >= Percentage:
        Positive_Motifs_4.append(Motif)

# Create list of non-significant motifs reliably identified

Negative_Motifs = []

for Motif in Motifs:
    P_values = motif_dict[Motif]
    Count = sum(1 for P_val in P_values)
    Count_Percent = (float(Count) / float(Num_Files_Sub)) * 100
    if Count_Percent >= Percentage:
        Negative_Motifs.append(Motif)

# -----------------------------------------------------
# Step 4
# Cut down lists to avoid duplication at various significance levels
# Write lists out to files
# -----------------------------------------------------

OutDir = conf.outdir

# Threshold of 0.001
# Create list to write out

List_to_write = []
for Motif in Positive_Motifs_4:
    List_to_write.append(Motif)

# Write out motifs

Out_File = "Significant_Motifs_0.001.txt"
Output = "/".join([cwd, OutDir, Out_File])

with open(Output, 'w') as o:
    o.write("Motifs significant with an e-value threshold of 0.001")
    o.write("\n")
    for Motif in List_to_write:
        o.write(Motif)
        o.write("\n")

# Threshold of 0.01
# Create list to write out

List_to_write = []
for Motif in Positive_Motifs_3:
    if Motif not in Positive_Motifs_4:
        List_to_write.append(Motif)

# Write out motifs

Out_File = "Significant_motifs_0.01.txt"
Output = "/".join([cwd, OutDir, Out_File])

with open(Output, 'w') as o:
    o.write("Motifs significant with an e-value threshold of 0.01")
    o.write("\n")
    for Mofit in List_to_write:
        o.write(Motif)
        o.write("\n")

# Threshold of 0.05
# Create list to write out

List_to_write = []
for Motif in Positive_Motifs_2:
    if Motif not in Positive_Motifs_4:
        if Motif not in Positive_Motifs_3:
            List_to_write.append(Motif)

# Write out motifs

Out_File = "Significant_motifs_0.05.txt"
Output = "/".join([cwd, OutDir, Out_File])

with open(Output, 'w') as o:
    o.write("Motifs significant with an e-value threshold of 0.05")
    o.write("\n")
    for Mofit in List_to_write:
        o.write(Motif)
        o.write("\n")

# Threshold of 0.1
# Create list to write out

List_to_write = []
for Motif in Positive_Motifs_1:
    if Motif not in Positive_Motifs_4:
        if Motif not in Positive_Motifs_3:
            if Motif not in Positive_Motifs_2:
                List_to_write.append(Motif)

# Write out motifs

Out_File = "Significant_motifs_0.1.txt"
Output = "/".join([cwd, OutDir, Out_File])

with open(Output, 'w') as o:
    o.write("Motifs significant with an e-value threshold of 0.1")
    o.write("\n")
    for Mofit in List_to_write:
        o.write(Motif)
        o.write("\n")

# Non-significant
# Create list to write out

List_to_write = []
for Motif in Negative_Motifs:
    if Motif not in Positive_Motifs_4:
        if Motif not in Positive_Motifs_3:
            if Motif not in Positive_Motifs_2:
                if Motif not in Positive_Motifs_1:
                    List_to_write.append(Motif)

# Write out motifs

Out_File = "Non-Significant_motifs.txt"
Output = "/".join([cwd, OutDir, Out_File])

with open(Output, 'w') as o:
    o.write("Motifs significant with an e-value above 0.1")
    o.write("\n")
    for Mofit in List_to_write:
        o.write(Motif)
        o.write("\n")
