#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -pe smp 6
#$ -l h_vmem=4G
#$ -l h=blacklace01.blacklace|blacklace03.blacklace|blacklace04.blacklace|blacklace05.blacklace|blacklace06.blacklace|blacklace07.blacklace|blacklace08.blacklace|blacklace09.blacklace|blacklace10.blacklace

scripts=/home/adamst/git_repos/scripts/phytophthora_fragariae/popgen_analysis/popgenome_scripts

/home/adamst/prog/R/R-3.2.5/bin/Rscript --vanilla $scripts/calculate_fst.R
