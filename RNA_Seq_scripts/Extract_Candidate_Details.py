#!/usr/bin/python

'''
This script uses candidates identified by Call_Candidate_Confidence.py and
extracts details from tables created by pacbio_anntoation_tables_modified.py
or pacbio_anntoation_tables_modified_no_coexp.py depending on isolate examined
'''

import sys
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument('--candidates', required=True, type=str,
                help='TSV file of candidate genes explaning the phenotypic \
                differences')
ap.add_argument('--annotation_table', required=True, type=str,
                help='TSV file containing gene expression details and other \
                information')
ap.add_argument('--out_dir', required=True, type=str,
                help='Directory to write output files to')
conf = ap.parse_args()
