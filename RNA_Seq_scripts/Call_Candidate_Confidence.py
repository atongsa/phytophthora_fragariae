#!/usr/bin/python

'''
This script takes outputs from Expression presence/absence and differently DEGs to create a sorted table of candidates with a score of 1-9, 9 being best
'''

import sys,argparse
from collections import defaultdict
from sets import Set
import os

ap = argparse.ArgumentParser()
ap.add_argument('--Unique_Expression_Files',required=True,nargs='+',type=str,help='Space separated list of files containing uniquely expressed genes')
ap.add_argument('--Differently_DEG_File',required=True,nargs='+',type=str,help='Space separated list of files containing unique differently differentially expressed genes')
ap.add_argument('--Orthogroup_in',required=True,type=str,help='Text output file of Orthogroups from OrthoFinder')
ap.add_argument('--Organism_1',required=True,type=str,help='ID of organism 1')
ap.add_argument('--Organism_2',required=True,type=str,help='ID of organism 2')
ap.add_argument('--Organism_3',required=True,type=str,help='ID of organism 3')
ap.add_argument('--Race_isolates',required=True,nargs='+',type=str,help='Space separated list of isolates of the race of interest')
ap.add_argument('--Reference_name',required=True,type=str,help='ID of isolate to score candidates of')
ap.add_argument('--RxLRs',required=True,type=str,help='File of all RxLR names for aligned genome')
ap.add_argument('--CRNs',required=True,type=str,help='File of all CRN names for aligned genome')
ap.add_argument('--ApoP',required=True,type=str,help='File of all hits from ApoplastP')
ap.add_argument('--Secreted_CQ',required=True,type=str,help='File of all secreted gene models')
ap.add_argument('--Secreted_ORF',required=True,type=str,help='File of all secreted ORF fragments')
ap.add_argument('--OutDir',required=True,type=str,help='Directory to write output files to')
conf = ap.parse_args()

#-----------------------------------------------------
# Step 1
# Load input files
#-----------------------------------------------------

Org1 = conf.Organism_1
Org2 = conf.Organism_2
Org3 = conf.Organism_3
Ref_Name = conf.Reference_name

Uniq_Exp_Files = conf.Unique_Expression_Files
gene_IDs = []
Org1_Uniq_Exp = []
Org2_Uniq_Exp = []
Org3_Uniq_Exp = []
for Uniq_Exp_File in Uniq_Exp_Files:
    with open(Uniq_Exp_File) as f:
        if Uniq_Exp_File.split('/')[-1].split('_')[0] == Org1 and Uniq_Exp_File.split('/')[-1].split('_')[1] == Ref_Name:
            gene_lines = f.readlines()[1:]
            transcript_ID = gene_lines.split('\t')[0]
            Org1_Uniq_Exp.append(transcipt_ID)
            gene_IDs.append(transcript_ID)
        elif Uniq_Exp_File.split('/')[-1].split('_')[0] == Org2 and Uniq_Exp_File.split('/')[-1].split('_')[1] == Ref_Name:
            gene_lines = f.readlines()[1:]
            transcript_ID = gene_lines.split('\t')[0]
            Org2_Uniq_Exp.append(transcipt_ID)
            gene_IDs.append(transcript_ID)
        elif Uniq_Exp_File.split('/')[-1].split('_')[0] == Org3 and Uniq_Exp_File.split('/')[-1].split('_')[1] == Ref_Name:
            gene_lines = f.readlines()[1:]
            transcript_ID = gene_lines.split('\t')[0]
            Org3_Uniq_Exp.append(transcipt_ID)
            gene_IDs.append(transcript_ID)
        else:
            sys.exit("Error, incorrect expression files provided")

Org1_Uniq_Exp_set = set(Org1_Uniq_Exp)
Org2_Uniq_Exp_set = set(Org2_Uniq_Exp)
Org3_Uniq_Exp_set = set(Org3_Uniq_Exp)
Gene_ID_set = set(gene_IDs)

Uniq_DEG_Files = conf.Unique_Expression_Files
Org1_Uniq_DEG = []
Org2_Uniq_DEG = []
Org3_Uniq_DEG = []
for Uniq_DEG_File in Uniq_DEG_Files:
    with open(Uniq_DEG_File) as f:
        if Uniq_DEG_File.split('/')[-1].split('_')[0] == Org1 and Uniq_DEG_File.split('/')[-1].split('_')[1] == Ref_Name:
            gene_lines = f.readlines()[1:]
            transcript_ID = gene_lines.split('\t')[0]
            Org1_Uniq_DEG.append(transcipt_ID)
        elif Uniq_DEG_File.split('/')[-1].split('_')[0] == Org2 and Uniq_DEG_File.split('/')[-1].split('_')[1] == Ref_Name:
            gene_lines = f.readlines()[1:]
            transcript_ID = gene_lines.split('\t')[0]
            Org2_Uniq_DEG.append(transcipt_ID)
        elif Uniq_DEG_File.split('/')[-1].split('_')[0] == Org3 and Uniq_DEG_File.split('/')[-1].split('_')[1] == Ref_Name:
            gene_lines = f.readlines()[1:]
            transcript_ID = gene_lines.split('\t')[0]
            Org3_Uniq_DEG.append(transcipt_ID)
        else:
            sys.exit("Error, incorrect DEG files provided")

Org1_Uniq_DEG_set = set(Org1_Uniq_DEG)
Org2_Uniq_DEG_set = set(Org2_Uniq_DEG)
Org3_Uniq_DEG_set = set(Org3_Uniq_DEG)

ortho_dict = defaultdict(list)
with open(conf.Orthogroup_in) as f:
    Ortho_lines = f.readlines()
    for line in Ortho_lines:
        line = line.rstrip()
        split_line = line.split()
        orthogroup = split_line[0]
        orthogroup = orthogroup.replace(":", "")
        genes_in_group = [ x for x in split_line if not 'OG' in x ]
        ortho_dict[orthogroup] = genes_in_group

ortho_set = set(ortho_dict.keys())

RxLRs = []
with open(conf.RxLRs) as f:
    RxLR_lines = f.readlines()
    for line in RxLR_lines:
        ID = line.rstrip()
        RxLRs.append(ID)

CRNs = []
with open(conf.CRNs) as f:
    CRN_lines = f.readlines()
    for line in CRN_lines:
        ID = line.rstrip()
        CRNs.append(ID)

ApoPs = []
with open(conf.ApoP) as f:
    ApoP_lines = f.readlines()
    for line in ApoP_lines:
        ID = line.rstrip()
        ApoPs.append(ID)

Sec = []
with open(conf.Secreted_CQ) as f:
    Sec_CQ_lines = f.readlines()
    for line in Sec_CQ_lines:
        ID = line.rstrip()
        Sec.append(ID)

with open(conf.Secreted_ORF) as f:
    Sec_ORF_lines = f.readlines()
    for line in Sec_ORF_lines:
        ID = line.rstrip()
        ID_modified = ".".join([ID, "t1"])
        Sec.append(ID_modified)

RxLR_set = set(RxLRs)
CRN_set = set(CRNs)
ApoP_set = set(ApoPs)
Sec_set = set(Sec)

#-----------------------------------------------------
# Step 2
# Create dictionaries listing gene IDs in each expressed set as keys with orthogroup ID as values
#-----------------------------------------------------

Race_list = conf.Race_isolates

Org1_Exp_dict = defaultdict(list)

for transcript_ID in Org1_Uniq_Exp_set:
    Isolates_in_OG = []
    ID_to_search = "|".join([Org1, transcript_ID])
    for OG in ortho_dict.keys():
        if ID_to_search in ortho_dict[OG]:
            for item in ortho_dict[OG]:
                Isolate = item.split('|')[0]
                Isolates_in_OG.append(Isolate)
                if set(Race_list).issubset(set(Isolates_in_OG)):
                    Org1_Exp_dict[transcript_ID] = orthogroup

#-----------------------------------------------------
# Step 3
# Loop through genes from isolate of interest, ID genes from other reference genomes in same OG and pull out relevant features
#-----------------------------------------------------

Org1_Org2_dict = defaultdict(list)
Org1_Org3_dict = defaultdict(list)

for transcript_ID in Org1_Exp_dict.keys():
    orthogroup = Org1_Exp_dict[transcript_ID]
    OG_genes = ortho_dict[orthogroup]
    for gene_ID in OG_genes:
        if gene_ID.split('|')[0] == Org2:
            Org1_Org2_dict[transcript_ID].append(gene_ID)
        elif gene_ID.split('|')[0] == Org3:
            Org1_Org3_dict[transcript_ID].append(gene_ID)
