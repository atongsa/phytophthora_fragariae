#!/usr/bin/python

'''
This script takes three gene tables produced by pacbio_anntoation_tables_modified.py as input and outputs text files with a list of uniquely differentially expressed genes, based on gene ID in BC-16.
'''

import sys,argparse

#-----------------------------------------------------
# Step 1
# Import variables, load input files and create lists of gene names
#-----------------------------------------------------
