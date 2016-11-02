#Runs commands from Maria to analyse output from SNP calling

##Filter inital vcf output

```bash
vcf=SNP_calling/95m_contigs_unmasked.vcf
script=/home/adamst/git_repos/scripts/popgen/snp/sub_vcf_parser.sh
qsub $script $vcf
```

#Only retain biallelic high-quality SNPS with no missing data for genetic analyses.
#For diploid genomes use another script: sub_vcf_parser.sh
cd $input
$scripts/vcf_parser_haploid.py --i Fus2_canu_contigs_unmasked.vcf
#General VCF stats (remember that vcftools needs to have the PERL library exported)
perl /home/sobczm/bin/vcftools/bin/vcf-stats \
Fus2_canu_contigs_unmasked.vcf >Fus2_canu_contigs_unmasked.stat
perl /home/sobczm/bin/vcftools/bin/vcf-stats \
Fus2_canu_contigs_unmasked_filtered.vcf >Fus2_canu_contigs_unmasked_filtered.stat
#Calculate the index for percentage of shared SNP alleles between the individs.
$scripts/similarity_percentage.py Fus2_canu_contigs_unmasked_filtered.vcf
#Visualise the output as heatmap and clustering dendrogram
Rscript --vanilla $scripts/distance_matrix.R Fus2_canu_contigs_unmasked_filtered_distance.log
#Carry out PCA and plot the results
Rscript --vanilla $scripts/pca.R Fus2_canu_contigs_unmasked_filtered.vcf
#Calculate an NJ tree based on all the SNPs. Outputs a basic diplay of the tree, plus a Newick file to be used
#for displaying the tree in FigTree and beautifying it.
$scripts/nj_tree.sh Fus2_canu_contigs_unmasked_filtered.vcf