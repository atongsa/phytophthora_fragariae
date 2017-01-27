#Begins the analysis of the summary stats section from Maria's github

##Copy input for the analysis into a new directory

```bash
input=/home/groups/harrisonlab/project_files/phytophthora_fragariae/summary_stats
snpeff=/home/sobczm/bin/snpEff
scripts=/home/adamst/git_repos/scripts/popgen
```

##All individuals

```bash
mkdir -p $input
cp /home/groups/harrisonlab/project_files/phytophthora_fragariae/SNP_calling/95m_contigs_unmasked.vcf $input
cp /home/groups/harrisonlab/project_files/phytophthora_fragariae/SNP_calling/95m_contigs_unmasked_filtered.vcf $input
cp /home/groups/harrisonlab/project_files/phytophthora_fragariae/repeat_masked/P.fragariae/Bc16/filtered_contigs_repmask/95m_contigs_unmasked.fa $input
cp gene_pred/codingquary/P.fragariae/Bc16/final/final_genes_appended.gff3 $input
cd $input
```

##Create additional subsets of VCF files with reduced number of individuals

```bash
vcftools=/home/sobczm/bin/vcftools/bin
vcflib=/home/sobczm/bin/vcflib/bin
```

##Cutting down vcf to just closely related strains of UK1, 2 and 3 and one for all *P. fragariae* strains, excluding NOV-77
First argument: unfiltered input VCF file with all SNPs
Subsequent arguments: Sample names of individuals to be removed

```bash
$vcflib/vcfremovesamples 95m_contigs_unmasked.vcf SCRP245_v2 Bc23 ONT3 Nov77 SCRP249 SCRP324 SCRP333 >95m_contigs_unmasked_UK123.vcf
$vcflib/vcfremovesamples 95m_contigs_unmasked.vcf Nov77 SCRP249 SCRP324 SCRP333 >95m_contigs_unmasked_Pf.vcf
```

##Filter the SNPs

```bash
cd summary_stats/
for vcf in $(ls *_contigs_unmasked_*.vcf | grep -e 'UK123\.' -e 'Pf\.')
do
    echo $vcf
    script=/home/adamst/git_repos/scripts/popgen/snp/sub_vcf_parser.sh
    qsub $script $vcf
done
```

##Remove monomorphic sites (minor allele count minimum 1). Argument --vcf is the filtered VCF file, and --out is the suffix to be used for the output file.

```bash
$vcftools/vcftools --vcf 95m_contigs_unmasked_UK123_filtered.vcf --mac 1 --recode --out 95m_contigs_unmasked_UK123_filtered
$vcftools/vcftools --vcf 95m_contigs_unmasked_Pf_filtered.vcf --mac 1 --recode --out 95m_contigs_unmasked_Pf_filtered
```

##Create custom SnpEff genome database

```bash
$scripts/summary_stats/build_genome_database.sh 95m_contigs_unmasked.fa final_genes_appended.gff3 Bc16
```

##Annotate VCF files

```bash
cd $input
for a in *recode.vcf
do
    $scripts/summary_stats/annotate_snps_genome.sh $a Bc16
done
```

##Create FASTA alignment files containing only select subsets of SNPs. Required for analyses in the Pf_popgenome_analysis.sh script. From now onwards, analysing only UK123.

```bash
cd $input
ref_genome=$input/95m_contigs_unmasked.fa
```

###all

```bash
python $scripts/summary_stats/vcf_to_fasta.py 95m_contigs_unmasked_UK123_filtered.recode_annotated.vcf $ref_genome 2
```

###Moving each subset of FASTA files into a separate dir.

```bash
mkdir all
mv *.fasta ./all
```

##coding

```bash
python $scripts/summary_stats/vcf_to_fasta.py 95m_contigs_unmasked_UK123_filtered.recode_coding.vcf $ref_genome 2
mkdir coding
mv *.fasta ./coding
```

##silent(four-fold degenerate)

```bash
python $scripts/summary_stats/vcf_to_fasta.py 95m_contigs_unmasked_UK123_filtered.recode_syn_4fd.vcf $ref_genome 2
mkdir silent
mv *.fasta ./silent
```

###Split the GFF file into one contig --> one GFF file. Required for analyses in Pf_popgenome_analysis.md

```bash
cd $input
mkdir -p gff
$scripts/summary_stats/split_gff_contig.sh final_genes_appended.gff3
mv *.gff ./gff
```

##Create FASTA alignment files containing only select subsets of SNPs. Required for analyses in the Pf_popgenome_analysis.sh script. From now onwards, analysing only Pf.

```bash
cd $input
ref_genome=$input/95m_contigs_unmasked.fa
```

###all

```bash
python $scripts/summary_stats/vcf_to_fasta.py 95m_contigs_unmasked_Pf_filtered.recode_annotated.vcf $ref_genome 2
```

###Moving each subset of FASTA files into a separate dir.

```bash
mkdir all_Pf
mv *.fasta ./all_Pf
```

##coding

```bash
python $scripts/summary_stats/vcf_to_fasta.py 95m_contigs_unmasked_Pf_filtered.recode_coding.vcf $ref_genome 2
mkdir coding_Pf
mv *.fasta ./coding_Pf
```

##silent(four-fold degenerate)

```bash
python $scripts/summary_stats/vcf_to_fasta.py 95m_contigs_unmasked_Pf_filtered.recode_syn_4fd.vcf $ref_genome 2
mkdir silent_Pf
mv *.fasta ./silent_Pf
```

###Split the GFF file into one contig --> one GFF file. Required for analyses in Pf_popgenome_analysis.md

```bash
cd $input
mkdir -p gff
$scripts/summary_stats/split_gff_contig.sh final_genes_appended.gff3
mv *.gff ./gff
```
