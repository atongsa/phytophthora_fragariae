#Methodology 4 from Andy's files - run on A4, BC-1, BC-16, BC-23, NOV-27, NOV-5, NOV-71, NOV-77, NOV-9, ONT-3, SCRP245_v2

```bash
ProjDir=/home/groups/harrisonlab/project_files/phytophthora_fragariae
cd $ProjDir
IsolateAbrv=All_Strains_plus_rubi
WorkDir=analysis/orthology/orthomcl/$IsolateAbrv
mkdir -p $WorkDir
mkdir -p $WorkDir/formatted
mkdir -p $WorkDir/goodProteins
mkdir -p $WorkDir/badProteins
```

##4.1 Format fasta files


###for A4

```bash
Taxon_code=A4
Fasta_file=gene_pred/codingquary/P.fragariae/A4/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

###for BC-1

```bash
Taxon_code=Bc1
Fasta_file=gene_pred/codingquary/P.fragariae/Bc1/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

###for BC-16

```bash
Taxon_code=Bc16
Fasta_file=gene_pred/codingquary/P.fragariae/Bc16/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

###for BC-23

```bash
Taxon_code=Bc23
Fasta_file=gene_pred/codingquary/P.fragariae/Bc23/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

###for NOV-27

```bash
Taxon_code=Nov27
Fasta_file=gene_pred/codingquary/P.fragariae/Nov27/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

###for NOV-5

```bash
Taxon_code=Nov5
Fasta_file=gene_pred/codingquary/P.fragariae/Nov5/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

###for NOV-71

```bash
Taxon_code=Nov71
Fasta_file=gene_pred/codingquary/P.fragariae/Nov71/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

###for NOV-77

```bash
Taxon_code=Nov77
Fasta_file=gene_pred/codingquary/P.fragariae/Nov77/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

###for NOV-9

```bash
Taxon_code=Nov9
Fasta_file=gene_pred/codingquary/P.fragariae/Nov9/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

###for ONT-3

```bash
Taxon_code=ONT3
Fasta_file=gene_pred/codingquary/P.fragariae/ONT3/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

###for SCRP245_v2

```bash
Taxon_code=SCRP245_v2
Fasta_file=gene_pred/codingquary/P.fragariae/SCRP245_v2/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

###for SCRP249

```bash
Taxon_code=SCRP249
Fasta_file=../phytophthora_rubi/gene_pred/codingquary/discovar/P.rubi/SCRP249/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

###for SCRP324

```bash
Taxon_code=SCRP324
Fasta_file=../phytophthora_rubi/gene_pred/codingquary/discovar/P.rubi/SCRP324/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

###for SCRP333

```bash
Taxon_code=SCRP333
Fasta_file=../phytophthora_rubi/gene_pred/codingquary/discovar/P.rubi/SCRP333/final/final_genes_combined.pep.fasta
Id_field=1
orthomclAdjustFasta $Taxon_code $Fasta_file $Id_field
mv "$Taxon_code".fasta $WorkDir/formatted/"$Taxon_code".fasta
```

##4.2 Filter proteins into good and poor sets.

```bash
Input_dir=$WorkDir/formatted
Min_length=10
Max_percent_stops=20
Good_proteins_file=$WorkDir/goodProteins/goodProteins.fasta
Poor_proteins_file=$WorkDir/badProteins/poorProteins.fasta
orthomclFilterFasta $Input_dir $Min_length $Max_percent_stops $Good_proteins_file $Poor_proteins_file
```

##4.3.a Perform an all-vs-all blast of the proteins

```bash
BlastDB=$WorkDir/blastall/$IsolateAbrv.db

makeblastdb -in $Good_proteins_file -dbtype prot -out $BlastDB
BlastOut=$WorkDir/all-vs-all_results.tsv
mkdir -p $WorkDir/splitfiles

SplitDir=/home/adamst/git_repos/tools/seq_tools/feature_annotation/signal_peptides
$SplitDir/splitfile_500.py --inp_fasta $Good_proteins_file --out_dir $WorkDir/splitfiles --out_base goodProteins

ProgDir=/home/adamst/git_repos/scripts/phytophthora/pathogen/orthology  
for File in $(find $WorkDir/splitfiles)
do
    Jobs=$(qstat | grep 'blast_500' | grep 'qw' | wc -l)
    while [ $Jobs -gt 1 ]
    do
        sleep 3
        printf "."
        Jobs=$(qstat | grep 'blast_500' | grep 'qw' | wc -l)
    done
    printf "\n"
    echo $File
    BlastOut=$(echo $File | sed 's/.fa/.tab/g')
    qsub $ProgDir/blast_500.sh $BlastDB $File $BlastOut
done
```

##4.3.b Merge the all-vs-all blast results

```bash
MergeHits="$IsolateAbrv"_blast.tab
printf "" > $MergeHits
for Num in $(ls $WorkDir/splitfiles/*.tab | rev | cut -f1 -d '_' | rev | sort -n)
do
    File=$(ls $WorkDir/splitfiles/*_$Num)
    cat $File
done > $MergeHits
```

##4.4 Perform ortholog identification

```bash
ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
MergeHits="$IsolateAbrv"_blast.tab
GoodProts=$WorkDir/goodProteins/goodProteins.fasta
qsub $ProgDir/qsub_orthomcl.sh $MergeHits $GoodProts 5
```

##4.5.a Manual identification of numbers of orthologous and unique genes

```bash
for num in 1
do
    echo "The total number of orthogroups is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | wc -l
    echo "The total number of genes in orthogroups is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -o '|' | wc -l
    echo "The number of orthogroups common to P. rubi is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -e 'SCRP249|' | grep -e 'SCRP324|' | grep -e 'SCRP333|' | grep -v -e 'A4|' -e 'Bc1|' -e 'Bc16|' -e 'Bc23|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Nov77|' -e 'Nov9|' -e 'ONT3|' -e 'SCRP245_v2|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -e 'SCRP249|' | grep -e 'SCRP324|' | grep -e 'SCRP333|' | grep -v -e 'A4|' -e 'Bc1|' -e 'Bc16|' -e 'Bc23|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Nov77|' -e 'Nov9|' -e 'ONT3|' -e 'SCRP245_v2|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to P. fragariae is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'A4|' | grep -e 'Bc1|' | grep -e 'Bc16|' | grep -e 'Bc23|' | grep -e 'Nov5|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov77|' | grep -e 'Nov9|' | grep -e 'ONT3|' | grep -e 'SCRP245_v2|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'A4|' | grep -e 'Bc1|' | grep -e 'Bc16|' | grep -e 'Bc23|' | grep -e 'Nov5|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov77|' | grep -e 'Nov9|' | grep -e 'ONT3|' | grep -e 'SCRP245_v2|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to UK1 strains is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'Bc23|' -e 'Nov27|' -e 'Nov71|' -e 'Nov77|' -e 'Nov9|' -e 'ONT3|' -e 'SCRP245_v2|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Bc1|' | grep -e 'Nov5|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'Bc23|' -e 'Nov27|' -e 'Nov71|' -e 'Nov77|' -e 'Nov9|' -e 'ONT3|' -e 'SCRP245_v2|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Bc1|' | grep -e 'Nov5|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to UK2 strains is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'A4|' -e 'Bc1|' -e 'Bc23|' -e 'Nov27|' -e 'Nov71|' -e 'Nov77|' -e 'Nov9|' -e 'ONT3|' -e 'SCRP245_v2|' -e 'Nov5|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Bc16|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'A4|' -e 'Bc1|' -e 'Bc23|' -e 'Nov27|' -e 'Nov71|' -e 'Nov77|' -e 'Nov9|' -e 'ONT3|' -e 'SCRP245_v2|' -e 'Nov5|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Bc16|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to UK3 strains is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'ONT3|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov9|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'ONT3|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov9|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to CA4 strains is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'Nov9|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'ONT3|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'Nov9|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'ONT3|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to CA5 strains is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'ONT3|' -e 'Nov9|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Bc23|' | grep -e 'Nov77|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'ONT3|' -e 'Nov9|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Bc23|' | grep -e 'Nov77|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to US4 strains is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'Nov9|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'A4|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'Nov9|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'A4|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to Unknown race strains is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'Nov9|' -e 'A4|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'SCRP245_v2|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'Nov9|' -e 'A4|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'SCRP245_v2|' | grep -o '|' | wc -l
    echo "The number of orthogroups with only six highly conserved target strains is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc23|' -e 'Nov77|' -e 'A4|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' -e 'SCRP245_v2|' | grep -e 'Nov5|' | grep -e 'Nov27' | grep -e 'Nov71' | grep -e 'Bc16' | grep -e 'Nov9' | grep -e 'Bc1' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc23|' -e 'Nov77|' -e 'A4|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' -e 'SCRP245_v2|' | grep -e 'Nov5|' | grep -e 'Nov27' | grep -e 'Nov71' | grep -e 'Bc16' | grep -e 'Nov9' | grep -e 'Bc1' | grep -o '|' | wc -l
    echo "The number of orthogroups containing all six highly conserved target strains is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -e 'Nov5|' | grep -e 'Nov27' | grep -e 'Nov71' | grep -e 'Bc16' | grep -e 'Nov9' | grep -e 'Bc1' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -e 'Nov5|' | grep -e 'Nov27' | grep -e 'Nov71' | grep -e 'Bc16' | grep -e 'Nov9' | grep -e 'Bc1' | grep -o '|' | wc -l
done
```

```
The total number of orthogroups is:
19952
The total number of genes in orthogroups is:
356680
The number of orthogroups common to all strains is:
13436
This represents the following number of genes:
318253
The number of orthogroups common to UK1 strains is:
4
This represents the following number of genes:
8
The number of orthogroups common to UK2 strains is:
35
This represents the following number of genes:
76
The number of orthogroups common to UK3 strains is:
5
This represents the following number of genes:
15
The number of orthogroups common to CA4 strains is:
494
This represents the following number of genes:
1380
The number of orthogroups common to CA5 strains is:
12
This represents the following number of genes:
25
The number of orthogroups common to US4 strains is:
3
This represents the following number of genes:
3
The number of orthogroups common to Unknown race strains is:
169
This represents the following number of genes:
467
The number of orthogroups with only six highly conserved target strains is:
5
This represents the following number of genes:
39
The number of orthogroups containing all six highly conserved target strains is:
14275
This represents the following number of genes:
428573
```

Identification of orthogroups of closely related strains for further analysis

```bash
for num in 1
do
    echo "The total number of shared orthogroups is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -e 'A4|' | grep -e 'Nov5|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Bc16|' | grep -e 'Nov9|' | grep -e 'Bc1|' | wc -l
    echo "The total number of genes in shared orthogroups is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -e 'A4|' | grep -e 'Nov5|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Bc16|' | grep -e 'Nov9|' | grep -e 'Bc1|' | grep -o '|' | wc -l
    echo "The total number of orthogroups is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc23|' -e 'SCRP245_v2' -e 'Nov77|' -e 'SCRP249' -e 'SCRP324' -e 'SCRP333' | wc -l
    echo "The total number of genes in orthogroups is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc23|' -e 'SCRP245_v2' -e 'Nov77|' -e 'SCRP249' -e 'SCRP324' -e 'SCRP333' | grep -o '|' | wc -l
    echo "The total number of UK1 orthogroups is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'A4|' -e 'Nov27|' -e 'Nov71|' -e 'Bc16|' -e 'Nov9|' | grep -e 'Nov5|' | grep -e 'Bc1|' | wc -l
    echo "The total number of genes in UK1 orthogroups is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'A4|' -e 'Nov27|' -e 'Nov71|' -e 'Bc16|' -e 'Nov9|' | grep -e 'Nov5|' | grep -e 'Bc1|' | grep -o '|' | wc -l
    echo "The total number of UK2 orthogroups is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Bc1|' -e 'Nov9|' | grep -e 'A4|' | grep -e 'Bc16|' | wc -l
    echo "The total number of genes in UK2 orthogroups is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Bc1|' -e 'Nov9|' | grep -e 'A4|' | grep -e 'Bc16|' | grep -o '|' | wc -l
    echo "The total number of UK3 orthogroups is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'Nov5|' -e 'A4|' -e 'Bc16|' -e 'Bc1|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov9|' | wc -l
    echo "The total number of genes in UK3 orthogroups is:"
    cat $WorkDir/"$IsolateAbrv"_orthogroups.txt | grep -v -e 'Nov5|' -e 'A4|' -e 'Bc16|' -e 'Bc1|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov9|' | grep -o '|' | wc -l
done
```

```
The total number of shared orthogroups is:
14052
The total number of genes in shared orthogroups is:
425856
The total number of orthogroups is:
583
The total number of genes in orthogroups is:
1808
The total number of UK1 orthogroups is:
16
The total number of genes in UK1 orthogroups is:
74
The total number of UK2 orthogroups is:
29
The total number of genes in UK2 orthogroups is:
127
The total number of UK3 orthogroups is:
39
The total number of genes in UK3 orthogroups is:
220
```

##4.5.b Plot venn diagrams:

```bash
ProgDir=/home/adamst/git_repos/scripts/phytophthora_fragariae
$ProgDir/UK1_Pf_venn_diag.r --inp $WorkDir/"$IsolateAbrv"_orthogroups.tab --out $WorkDir/"$IsolateAbrv"_UK1_orthogroups.pdf
$ProgDir/UK2_Pf_venn_diag.r --inp $WorkDir/"$IsolateAbrv"_orthogroups.tab --out $WorkDir/"$IsolateAbrv"_UK2_orthogroups.pdf
$ProgDir/UK3_Pf_venn_diag.r --inp $WorkDir/"$IsolateAbrv"_orthogroups.tab --out $WorkDir/"$IsolateAbrv"_UK3_orthogroups.pdf
```

Output was a pdf file of the venn diagram.

The following additional information was also provided. The format of the following lines is as follows:

Isolate name (total number of orthogroups) number of unique singleton genes number of unique groups of inparalogs

###UK race 1 focused analysis

```
[1] "A4"
[1] "The total number of orthogroups and singleton genes in this isolate:  16638"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  2427"
[1] "The total number of singleton genes not in the venn diagram:  1013"
[1] "NOV-5"
[1] "The total number of orthogroups and singleton genes in this isolate:  16762"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  1539"
[1] "The total number of singleton genes not in the venn diagram:  1024"
[1] "NOV-27"
[1] "The total number of orthogroups and singleton genes in this isolate:  17613"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  3402"
[1] "The total number of singleton genes not in the venn diagram:  1373"
[1] "NOV-71"
[1] "The total number of orthogroups and singleton genes in this isolate:  16645"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  2434"
[1] "The total number of singleton genes not in the venn diagram:  962"
[1] "BC-16"
[1] "The total number of orthogroups and singleton genes in this isolate:  17356"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  3145"
[1] "The total number of singleton genes not in the venn diagram:  1530"
[1] "NOV-9"
[1] "The total number of orthogroups and singleton genes in this isolate:  17602"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  3391"
[1] "The total number of singleton genes not in the venn diagram:  1369"
[1] "BC-1"
[1] "The total number of orthogroups and singleton genes in this isolate:  17518"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  2049"
[1] "The total number of singleton genes not in the venn diagram:  1330"
```

###UK race 2 focused analysis

```
[1] "A4"
[1] "The total number of orthogroups and singleton genes in this isolate:  16638"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  1186"
[1] "The total number of singleton genes not in the venn diagram:  1013"
[1] "NOV-5"
[1] "The total number of orthogroups and singleton genes in this isolate:  16762"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  2246"
[1] "The total number of singleton genes not in the venn diagram:  1024"
[1] "NOV-27"
[1] "The total number of orthogroups and singleton genes in this isolate:  17613"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  3097"
[1] "The total number of singleton genes not in the venn diagram:  1373"
[1] "NOV-71"
[1] "The total number of orthogroups and singleton genes in this isolate:  16645"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  2129"
[1] "The total number of singleton genes not in the venn diagram:  962"
[1] "BC-16"
[1] "The total number of orthogroups and singleton genes in this isolate:  17356"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  1478"
[1] "The total number of singleton genes not in the venn diagram:  1530"
[1] "NOV-9"
[1] "The total number of orthogroups and singleton genes in this isolate:  17602"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  3086"
[1] "The total number of singleton genes not in the venn diagram:  1369"
[1] "BC-1"
[1] "The total number of orthogroups and singleton genes in this isolate:  17518"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  3086"
[1] "The total number of singleton genes not in the venn diagram:  1330"
```

###UK race 3 focused analysis

```
[1] "A4"
[1] "The total number of orthogroups and singleton genes in this isolate:  16638"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  2244"
[1] "The total number of singleton genes not in the venn diagram:  1013"
[1] "NOV-5"
[1] "The total number of orthogroups and singleton genes in this isolate:  16762"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  2368"
[1] "The total number of singleton genes not in the venn diagram:  1024"
[1] "NOV-27"
[1] "The total number of orthogroups and singleton genes in this isolate:  17613"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  1754"
[1] "The total number of singleton genes not in the venn diagram:  1373"
[1] "NOV-71"
[1] "The total number of orthogroups and singleton genes in this isolate:  16645"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  1331"
[1] "The total number of singleton genes not in the venn diagram:  962"
[1] "BC-16"
[1] "The total number of orthogroups and singleton genes in this isolate:  17356"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  2962"
[1] "The total number of singleton genes not in the venn diagram:  1530"
[1] "NOV-9"
[1] "The total number of orthogroups and singleton genes in this isolate:  17602"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  1757"
[1] "The total number of singleton genes not in the venn diagram:  1369"
[1] "BC-1"
[1] "The total number of orthogroups and singleton genes in this isolate:  17518"
[1] "The total number of orthogroups and singleton genes not in the venn diagram:  3208"
[1] "The total number of singleton genes not in the venn diagram:  1330"
```

#Analysis of orthogroups unique to UK race 2 (Strains BC-16 & A4)

##The genes unique to Race 2 were identified within the orthology analysis

##First variables were set:

```bash
WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi
UK2UniqDir=$WorkDir/UK2_unique
Orthogroups=$WorkDir/All_Strains_plus_rubi_orthogroups.txt
GoodProts=$WorkDir/goodProteins/goodProteins.fasta
Final_genes_Bc16=gene_pred/codingquary/P.fragariae/Bc16/final/final_genes_combined.pep.fasta
Final_genes_A4=gene_pred/codingquary/P.fragariae/A4/final/final_genes_combined.pep.fasta
Uniq_UK2_groups=$UK2UniqDir/UK2_uniq_orthogroups.txt
mkdir -p $UK2UniqDir
```

#Orthogroups only containing Race 2 genes were extracted:

##Bars are to prevent incorrect filtering

```bash
cat $Orthogroups | grep -v -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Bc1|' -e 'Nov9|' | grep -e 'A4|' | grep -e 'Bc16|' > $Uniq_UK2_groups
echo "The number of orthogroups unique to Race UK2 are:"
cat $Uniq_UK2_groups | wc -l
echo "The following number genes are contained in these orthogroups:"
cat $Uniq_UK2_groups | grep -v -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Bc1|' -e 'Nov9|' | grep -e 'A4|' | grep -e 'Bc16|' | grep -o '|' | wc -l
```

```
The number of orthogroups unique to Race 2 are:
29
The following number genes are contained in these orthogroups:
127
```

#Race 2 unique RxLR families

#Race 2 RxLR genes were parsed to the same format as the gene names used in the analysis:

```bash
for num in 1
do
    RxLR_Names_Bc16=analysis/RxLR_effectors/combined_evidence/P.fragariae/Bc16/Bc16_Total_RxLR_EER_motif_hmm.txt
    RxLR_Names_A4=analysis/RxLR_effectors/combined_evidence/P.fragariae/A4/A4_Total_RxLR_EER_motif_hmm.txt
    WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi
    RxLR_Dir=$WorkDir/UKR2_RxLR
    Orthogroups=$WorkDir/All_Strains_plus_rubi_orthogroups.txt
    RxLR_ID=$RxLR_Dir/UKR2_aug_RxLR_EER_IDs.txt
    mkdir -p $RxLR_Dir
    cat $RxLR_Names_Bc16 | sed -r 's/^/Bc16|/g' > $RxLR_ID
    cat $RxLR_Names_A4 | sed -r 's/^/A4|/g' >> $RxLR_ID
done
```

#Ortholog groups containing RxLR proteins were identified using the following commands:

```bash
for num in 1
do
    echo "The number of RxLRs searched for is:"
    cat $RxLR_ID | wc -l
    echo "Of these, the following number were found in orthogroups:"
    RxLR_Orthogroup_hits=$RxLR_Dir/UK2_RxLR_Orthogroups_hits.txt
    cat $Orthogroups | grep -o -w -f $RxLR_ID > $RxLR_Orthogroup_hits
    cat $RxLR_Orthogroup_hits | wc -l
    echo "These were distributed through the following number of Orthogroups:"
    RxLR_Orthogroup=$RxLR_Dir/UK2_RxLR_Orthogroups.txt
    cat $Orthogroups | grep -w -f $RxLR_ID > $RxLR_Orthogroup
    cat $RxLR_Orthogroup | wc -l
    echo "The following RxLRs were found in Race 2 unique orthogroups:"
    RxLR_UK2_uniq_groups=$RxLR_Dir/UK2_uniq_RxLR_Orthogroups_hits.txt
    cat $RxLR_Orthogroup | grep -v -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Bc1|' -e 'Nov9|' | grep -e 'A4|' | grep -e 'Bc16|' > $RxLR_UK2_uniq_groups
    cat $RxLR_UK2_uniq_groups | wc -l
    echo "These orthogroups contain the following number of RxLRs:"
    cat $RxLR_UK2_uniq_groups | grep -w -o -f $RxLR_ID | wc -l
    echo "The following RxLRs were found in P.fragariae unique orthogroups:"
    RxLR_Pf_uniq_groups=$RxLR_Dir/Pf_RxLR_Orthogroups_hits.txt
    cat $RxLR_Orthogroup > $RxLR_Pf_uniq_groups
    cat $RxLR_Pf_uniq_groups | wc -l
    echo "These orthogroups contain the following number of RxLRs:"
    cat $RxLR_Pf_uniq_groups | grep -w -o -f $RxLR_ID | wc -l
done
```

```
The number of RxLRs searched for is:
674
Of these, the following number were found in orthogroups:
485
These were distributed through the following number of Orthogroups:
185
The following RxLRs were found in Race 2 unique orthogroups:
0
These orthogroups contain the following number of RxLRs:
0
The following RxLRs were found in P.fragariae unique orthogroups:
185
These orthogroups contain the following number of RxLRs:
485
```

#The Race 2 RxLR genes that were not found in orthogroups were identified:

```bash
for num in 1
do
    RxLR_UK2_uniq=$RxLR_Dir/UK2_unique_RxLRs.txt
    cat $RxLR_ID | grep -v -w -f $RxLR_Orthogroup_hits | tr -d 'Bc16|' > $RxLR_UK2_uniq
    cat $RxLR_ID | grep -v -w -f $RxLR_Orthogroup_hits | tr -d 'A4|' >> $RxLR_UK2_uniq
    echo "The number of UK2 unique RxLRs are:"
    cat $RxLR_UK2_uniq | wc -l
    RxLR_Seq_Bc16=analysis/RxLR_effectors/combined_evidence/P.fragariae/Bc16/Bc16_final_RxLR_EER.fa
    RxLR_Seq_A4=analysis/RxLR_effectors/combined_evidence/P.fragariae/A4/A4_final_RxLR_EER.fa
    Final_genes_Bc16=gene_pred/codingquary/P.fragariae/Bc16/final/final_genes_combined.pep.fasta
    Final_genes_A4=gene_pred/codingquary/P.fragariae/A4/final/final_genes_combined.pep.fasta
    RxLR_UK2_uniq_fa=$RxLR_Dir/UK2_unique_RxLRs.fa
    cat $Final_genes_Bc16 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $RxLR_UK2_uniq | grep -E -v '^--' > $RxLR_UK2_uniq_fa
    cat $Final_genes_A4 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $RxLR_UK2_uniq | grep -E -v '^--' >> $RxLR_UK2_uniq_fa
done
```

```
The number of UK2 unique RxLRs are:
378
```

##Extracting fasta files for orthogroups containing Race 2 putative RxLRs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi/UKR2_RxLR/UK2_RxLR_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi/UKR2_RxLR/orthogroups_fasta_UK2_RxLR
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```


##Extracting fasta files for P. fragariae orthogroups containing Race 2 putative RxLRs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi/UKR2_RxLR/Pf_RxLR_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi/UKR2_RxLR/orthogroups_fasta_Pf_RxLR
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

<!-- ##Race 2 unique Crinkler families

#Race 2 crinkler genes were parsed to the same format as the gene names used in the analysis:

```bash
CRN_Names_Bc16=analysis/CRN_effectors/hmmer_CRN/P.fragariae/Bc16/Bc16_Braker1_CRN_hmmer_headers.txt
WorkDir=analysis/orthology/orthomcl/phytophthora_fragariae
CRN_Dir=$WorkDir/Bc16_CRN
Orthogroups=$WorkDir/phytophthora_fragariae_orthogroups.txt
CRN_ID_Bc16=$CRN_Dir/Bc16_CRN_hmmer_IDs.txt
mkdir -p $CRN_Dir
cat $CRN_Names_Bc16 | sed 's/g/Bc16|g/g' > $CRN_ID_Bc16
```

#Ortholog groups containing CRN proteins were identified using the following commands:

```bash
echo "The number of CRNs searched for is:"
cat $CRN_ID_Bc16 | wc -l
echo "Of these, the following number were found in orthogroups:"
CRN_Orthogroup_hits_Bc16=$CRN_Dir/Bc16_CRN_Orthogroups_hits.txt
cat $Orthogroups | grep -o -w -f $CRN_ID_Bc16 > $CRN_Orthogroup_hits_Bc16
cat $CRN_Orthogroup_hits_Bc16 | wc -l
echo "These were distributed through the following number of Orthogroups:"
CRN_Orthogroup_Bc16=$CRN_Dir/Bc16_CRN_Orthogroups.txt
cat $Orthogroups | grep -w -f $CRN_ID_Bc16 > $CRN_Orthogroup_Bc16
cat $CRN_Orthogroup_Bc16 | wc -l
echo "The following CRNs were found in Race 2 unique orthogroups:"
CRN_Bc16_uniq_groups=$CRN_Dir/Bc16_uniq_CRN_Orthogroups_hits.txt
cat $CRN_Orthogroup_Bc16 | grep -v 'A4' | grep -v 'Bc1' | grep -v 'Bc23' | grep -v 'Nov27' | grep -v 'Nov5' | grep -v 'Nov71' | grep -v 'Nov77' | grep -v 'Nov9' | grep -v 'ONT3' | grep -v 'SCRP245_v2' > $CRN_Bc16_uniq_groups
cat $CRN_Bc16_uniq_groups | wc -l
echo "The following CRNs were found in P.fragariae unique orthogroups:"
CRN_Pf_uniq_groups=$CRN_Dir/Pf_CRN_Orthogroups_hits.txt
cat $CRN_Orthogroup_Bc16 > $CRN_Pf_uniq_groups
cat $CRN_Pf_uniq_groups | wc -l
```

```
```

#The Race 2 CRN genes not found in orthogroups were identified:

```bash
CRN_Bc16_uniq=$CRN_Dir/Bc16_unique_CRNs.txt
cat $CRN_ID_Bc16 | grep -v -w -f $CRN_Orthogroup_hits_Bc16 | tr -d 'Bc16|' > $CRN_Bc16_uniq
echo "The number of Race 2 unique CRNs are:"
cat $CRN_Bc16_uniq | wc -l
CRN_Seq_Bc16=analysis/CRN_effectors/hmmer_CRN/P.fragariae/Bc16/Bc16_pub_CRN_hmmer_out.fa
Braker_genes=gene_pred/braker/P.fragariae/Bc16/P.fragariae_Bc16_braker/augustus.aa
CRN_Bc16_uniq_fa=$CRN_Dir/Bc16_unique_CRNs.fa
cat $Braker_genes | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $CRN_Bc16_uniq | grep -E -v '^--' > $CRN_Bc16_uniq_fa
```

```
```

##Extracting fasta files for orthogroups containing Race 2 putative CRNs

```bash
ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
OrthogroupTxt=analysis/orthology/orthomcl/phytophthora_fragariae/Bc16_CRN/Bc16_CRN_Orthogroups.txt
GoodProt=analysis/orthology/orthomcl/phytophthora_fragariae/goodProteins/goodProteins.fasta
OutDir=analysis/orthology/orthomcl/phytophthora_fragariae/Bc16_CRN/orthogroups_fasta_Bc16_CRN
mkdir -p $OutDir
$ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
``` -->

<!-- ##Determining function of orthogroups (6.3 is the start here, all not relevant)

#Lists of genes from Race 2 unique genes, P. fragariae orthogroups and the largest shared gene families were identified

#Unclear on interproscan here, it doesn't match my output

```bash
WorkDir=analysis/orthology/orthomcl/phytophthora_fragariae
InterProFile=gene_pred/interproscan/Bc16/P.fragariae_Bc16_braker/10300_interproscan.tsv
``` -->
