#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -pe smp 1
#$ -l h_vmem=1G
#$ -l h=blacklace01.blacklace|blacklace02.blacklace|blacklace04.blacklace|blacklace05.blacklace|blacklace06.blacklace|blacklace07.blacklace|blacklace08.blacklace|blacklace09.blacklace|blacklace10.blacklace|blacklace12.blacklace

scripts=/home/adamst/git_repos/scripts/phytophthora_fragariae/RNA_Seq_scripts

/home/adamst/prog/R/R-3.2.5/bin/Rscript --vanilla $scripts/Export_Gene_Lists.R --out_dir $1

New_Dir=$1/modules
mkdir -p $New_Dir
mv $1/Genes_in_*.txt $New_Dir/.
