#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -pe smp 1
#$ -l h_vmem=6G
#$ -l h=blacklace01.blacklace|blacklace02.blacklace|blacklace06.blacklace|blacklace07.blacklace|blacklace08.blacklace|blacklace09.blacklace|blacklace10.blacklace|blacklace12.blacklace

scripts=/home/adamst/git_repos/scripts/phytophthora_fragariae/RNA_Seq_scripts

/home/adamst/prog/R/R-3.2.5/bin/Rscript --vanilla $scripts/Export_Network_Cytoscape.R --out_dir $1
