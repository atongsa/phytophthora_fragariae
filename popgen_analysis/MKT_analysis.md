#Runs analysis of *P. fragariae* and *P. rubi* genomes in preparation for McDonald-Kreitman test. Fay & Wu's H is not necessary right now.

#Set initial variables

```bash
scripts=/home/adamst/git_repos/scripts/popgen/summary_stats
input=/home/groups/harrisonlab/project_files/phytophthora_fragariae
```

#A)

```
Establish ancestral allele using genotype(s) from select outgroup species
1)
*P. rubi* - used as outgroup (incorrectly, as derived from *P. fragariae*) in order to test the ancestral allele annotation procedure using VCF polymorphism data stemming from alignment of genome outgroup reads to the focal species genome.
2)
Outgroups: *P. sojae*, *P. ramorum* (*P. ramorum* is quite distantly related to the other two species) in order to test the ancestral allele annotation procedure using Mauve-based whole-genome alignment.
3)
Lastly, the results of ancestral allele annotation using VCF-based annotation (#1) will be compared to the whole genome alignment annotation (#2).

Choice of the analysis to follow: 1, 2, 3 depends on the available resources and researcher preferences.
Annotation with ancestral alleles can be used just to polarise the mutation status of SNPs of interest or can be used in the formal tests for selection (e.g. McDonald-Kreitman Test and Fay & Wu's H described below)
```

##Set variables for locations of *P. fragariae* and *P. rubi* genomes

```bash
#*P. fragariae*
Pf=/home/groups/harrisonlab/project_files/phytophthora_fragariae/repeat_masked/quiver_results/Bc16/filtered_contigs_repmask/polished_contigs_hardmasked.fa
#*P. rubi* SCRP249
Pra=/home/groups/harrisonlab/project_files/phytophthora_rubi/repeat_masked/P.rubi/SCRP249/deconseq_Paen_repmask/SCRP249_contigs_hardmasked.fa
#*P. rubi* SCRP324
Prb=/home/groups/harrisonlab/project_files/phytophthora_rubi/repeat_masked/P.rubi/SCRP324/ncbi_edits_repmask/SCRP324_contigs_hardmasked.fa
#*P. rubi* SCRP333
Prc=/home/groups/harrisonlab/project_files/phytophthora_rubi/repeat_masked/P.rubi/SCRP333/deconseq_Paen_repmask/SCRP333_contigs_hardmasked.fa
```

###1

```bash
python $scripts/annotate_vcf_aa.py $input/SNP_calling/polished_contigs_unmasked_filtered.vcf 2 SCRP249,,SCRP324,,SCRP333
```

###2
####progressiveMauve

#####Run progressiveMauve

```bash
cp $Pf ./
cp $Pra ./
cp $Prb ./
cp $Prc ./
qsub $scripts/run_progressive_mauve.sh $input/progressiveMauve "polished_contigs_hardmasked.fa SCRP249_contigs_hardmasked.fa SCRP324_contigs_hardmasked.fa SCRP333_contigs_hardmasked.fa"
rm polished_contigs_hardmasked.fa SCRP249_contigs_hardmasked.fa SCRP324_contigs_hardmasked.fa SCRP333_contigs_hardmasked.fa
```

#####Parse Mauve output

```bash
perl /home/sobczm/bin/popoolation_1.2.2/mauve-parser.pl --ref $Pf \
--input $input/summary_stats/progressiveMauve/aligned_genomes.xmfa --output $input/summary_stats/progressiveMauve/mel-guided-alignment.txt
```

```
Option 'Y' specifies to print fake genotype into the VCF file encoding the identified ancestral alleles.
Use this option when proceeding to use Popgenome in order to calculate outgroup-based statistics: Fay & Wu's H and McDonald-Kreitman test
```

#####Carry out analysis with fake genotype

```bash
python $scripts/annotate_gen_aa.py $input/summary_stats/progressiveMauve/mel-guided-alignment.txt \
$input/summary_stats/polished_contigs_unmasked_filtered.vcf 2 Y
```

#####Carry out analysis above without printing fake genotypes.

```bash
python $scripts/annotate_gen_aa.py $input/summary_stats/progressiveMauve/mel-guided-alignment.txt \
$input/summary_stats/polished_contigs_unmasked_filtered.vcf 2 N
```

###3

####Compare the results of ancestral allele annotation obtained using VCF and genome alignment and print both AA field and fake genotype with the ancestral allele:

```bash
python $scripts/compare_outgroup_results.py $input/summary_stats/polished_contigs_unmasked_filtered_gen_aa.vcf \
$input/summary_stats/polished_contigs_unmasked_filtered_gen_aa.vcf 2 N
```

#B)

##McDonald-Kreitman test (a couple of genotypes from the outgroup species required) calculated by PopGenome.
##As an example, generate FASTA input using VCF created in A) 1

```bash
mkdir -p $input/mkt
cd $input/mkt
ref_genome=$Pf
vcf_file=$input/SNP_calling/polished_contigs_unmasked_filtered_vcf_aa.vcf
python $scripts/vcf_to_fasta.py $vcf_file $ref_genome 2
```

###Prepare Popgenome input

```bash
function Popgenome {
mkdir contigs && mv *.fasta ./contigs
cd contigs
for f in *.fasta
do
    folder=${f%.fasta}
    mkdir $folder
    mv $f $folder
done

#Gff files
cd ..
gff=/home/groups/harrisonlab/project_files/phytophthora_fragariae/gene_pred/annotation/P.fragariae/Bc16/Bc16_genes_incl_ORFeffectors_conservative.pep.fasta
$scripts/split_gff_contig.sh $gff
mkdir gff && mv *.gff ./gff

#Check for orphan contigs with no matching gff file, which need to be removed prior to the run.
for a in $PWD/contigs/*/*.fasta
do
    filename=$(basename "$a")
    expected_gff="$PWD/gff/${filename%.fa*}.gff"
    if [ ! -f "$expected_gff" ]
    then
       rm -rf $(dirname $a)
    fi
done
}
Popgenome
```

#Requires custom adjustment of the R script called below to include the samples being analysed.

```bash
qsub $scripts/sub_calculate_mkt.sh
```

################ Outgroup-based tests for selection
##Fay & Wu's H (at least one outgroup genotype needed) calculated by PopGenome
##As an example, generate FASTA input using VCF created in A) 2

```bash
mkdir -p $input/faywuh
cd $input/faywuh
ref_genome=/home/groups/harrisonlab/project_files/phytophthora_fragariae/repeat_masked/quiver_results/Bc16/filtered_contigs_repmask/polished_contigs_hardmasked.fa
vcf_file=$input/SNP_calling/polished_contigs_unmasked_filtered_gen_aa.vcf
python $scripts/vcf_to_fasta.py $vcf_file $ref_genome 2
##Prepare Popgenome input
Popgenome
#Requires custom adjustment of the R script called below to include the samples being analysed.
qsub $scripts/sub_calculate_faywu.sh
```
