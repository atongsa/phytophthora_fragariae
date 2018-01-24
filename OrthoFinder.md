#Maria has suggested a new tool to try for orthology analysis, run it in parallel with orthomcl as a comparison.

##Setting of variables

```bash
input=/home/groups/harrisonlab/project_files/phytophthora_fragariae/analysis/orthology/OrthoFinder
scripts=/home/adamst/git_repos/scripts/popgen/clock/motif_discovery
WorkDir=/home/groups/harrisonlab/project_files/phytophthora_fragariae/analysis/orthology/OrthoFinder/formatted/Results_Jan16
```

##Copy files of all protein sequences to one directory

```bash
mkdir -p $input
cp -r analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/formatted $input
```

###Runs orthofinder

```bash
screen -a
qlogin -pe smp 24
input=/home/groups/harrisonlab/project_files/phytophthora_fragariae/analysis/orthology/OrthoFinder
scripts=/home/adamst/git_repos/scripts/popgen/clock/motif_discovery
cd $input
IsolateAbrv=All_Strains_plus_rubi_no_removal
orthofinder -f formatted -t 24
```

```
Best outgroup(s) for species tree
---------------------------------
Observed 250 duplications. 228 support the best root and 22 contradict it.
Best outgroup for species tree:
SCRP249, SCRP333, SCRP324

OrthoFinder assigned 469036 genes (97.9% of total) to 38179 orthogroups. Fifty percent of all genes were in orthogroups with 14 or more genes (G50 was 14) and were contained in the largest 12233 orthogroups (O50 was 12233). There were 17388 orthogroups with all species present and 13444 of these consisted entirely of single-copy genes.
```

##Compare OrthoFinder with orthoMCL

OrthoFinder produces a set of statistics, generate what of these I can for orthoMCL, some others will be calculated manually

```bash
for num in 1
do
    echo "Number of genes:"
    GoodProts=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    cat $GoodProts | grep '>' | wc -l
    echo "Number of genes in orthogroups:"
    OrthoGroups=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/All_Strains_plus_rubi_no_removal_orthogroups.txt
    fgrep -o '|' $OrthoGroups | wc -l
    echo "Number of orthogroups:"
    fgrep -o ':' $OrthoGroups | wc -l
    echo "Median orthogroup size:"
    ProgDir=/home/adamst/git_repos/scripts/phytophthora_fragariae
    python $ProgDir/calc_orthogroup_median.py --orthogroups $OrthoGroups
done
```

```
OrthoMCL:
Number of genes input: 478,997
Number of genes in orthogroups: 455,838
Number of unassigned genes: 23,159
Percentage of unassigned genes: 4.8%
Number of orthogroups: 24,041
Mean orthogroup size: 19.0
Median orthogroup size: 14

OrthoFinder:
Number of genes input: 479,008
Number of genes in orthogroups: 469,036
Number of unassigned genes: 9,972
Percentage of unassigned genes: 2.1%
Number of orthogroups: 38,179 - this does not include singletons
Mean orthogroup size: 12.3
Median orthogroup size: 12

Unclear where there are 11 more genes fed into OrthoFinder, but there are 2.7 percentage points fewer genes in unassigned groups, with 14,138 more orthogroups, with a 6.7 smaller mean orthogroup size and a 2 smaller median orthogroup size. So, OrthoFinder seems better than OrthoMCL for my requirements.
```

##4.5.a Manual identification of numbers of orthologous and unique genes

```bash
for num in 1
do
    echo "The total number of orthogroups is:"
    cat $WorkDir/Orthogroups.txt | wc -l
    echo "The total number of genes in orthogroups is:"
    cat $WorkDir/Orthogroups.txt | grep -o '|' | wc -l
    echo "The number of orthogroups common to P. rubi is:"
    cat $WorkDir/Orthogroups.txt | grep -e 'SCRP249|' | grep -e 'SCRP324|' | grep -e 'SCRP333|' | grep -v -e 'A4|' -e 'Bc1|' -e 'Bc16|' -e 'Bc23|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Nov77|' -e 'Nov9|' -e 'ONT3|' -e 'SCRP245_v2|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/Orthogroups.txt | grep -e 'SCRP249|' | grep -e 'SCRP324|' | grep -e 'SCRP333|' | grep -v -e 'A4|' -e 'Bc1|' -e 'Bc16|' -e 'Bc23|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Nov77|' -e 'Nov9|' -e 'ONT3|' -e 'SCRP245_v2|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to P. fragariae is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'A4|' | grep -e 'Bc1|' | grep -e 'Bc16|' | grep -e 'Bc23|' | grep -e 'Nov5|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov77|' | grep -e 'Nov9|' | grep -e 'ONT3|' | grep -e 'SCRP245_v2|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'A4|' | grep -e 'Bc1|' | grep -e 'Bc16|' | grep -e 'Bc23|' | grep -e 'Nov5|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov77|' | grep -e 'Nov9|' | grep -e 'ONT3|' | grep -e 'SCRP245_v2|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to UK1 isolates is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'Bc23|' -e 'Nov27|' -e 'Nov71|' -e 'Nov77|' -e 'Nov9|' -e 'ONT3|' -e 'SCRP245_v2|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Bc1|' | grep -e 'Nov5|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'Bc23|' -e 'Nov27|' -e 'Nov71|' -e 'Nov77|' -e 'Nov9|' -e 'ONT3|' -e 'SCRP245_v2|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Bc1|' | grep -e 'Nov5|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to UK2 isolates is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'Bc1|' -e 'Bc23|' -e 'Nov27|' -e 'Nov71|' -e 'Nov77|' -e 'Nov9|' -e 'ONT3|' -e 'SCRP245_v2|' -e 'Nov5|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Bc16|' | grep -e 'A4|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'Bc1|' -e 'Bc23|' -e 'Nov27|' -e 'Nov71|' -e 'Nov77|' -e 'Nov9|' -e 'ONT3|' -e 'SCRP245_v2|' -e 'Nov5|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Bc16|' | grep -e 'A4|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to UK3 isolates is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'ONT3|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov9|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'ONT3|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov9|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to CA4 isolates is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'Nov9|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'ONT3|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'Nov9|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'ONT3|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to CA5 isolates is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'ONT3|' -e 'Nov9|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Bc23|' | grep -e 'Nov77|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'A4|' -e 'Bc16|' -e 'ONT3|' -e 'Nov9|' -e 'SCRP245_v2|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'Bc23|' | grep -e 'Nov77|' | grep -o '|' | wc -l
    echo "The number of orthogroups common to Unknown race isolates is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'Nov9|' -e 'A4|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'SCRP245_v2|' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc16|' -e 'Bc23|' -e 'Nov77|' -e 'Nov9|' -e 'A4|' -e 'Bc1|' -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' | grep -e 'SCRP245_v2|' | grep -o '|' | wc -l
    echo "The number of orthogroups with only seven highly conserved target isolates is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc23|' -e 'Nov77|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' -e 'SCRP245_v2|' | grep -e 'Nov5|' | grep -e 'Nov27' | grep -e 'Nov71' | grep -e 'Bc16' | grep -e 'Nov9' | grep -e 'Bc1' | grep -e 'A4' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc23|' -e 'Nov77|' -e 'SCRP249|' -e 'SCRP324|' -e 'SCRP333|' -e 'SCRP245_v2|' | grep -e 'Nov5|' | grep -e 'Nov27' | grep -e 'Nov71' | grep -e 'Bc16' | grep -e 'Nov9' | grep -e 'Bc1' | grep -e 'A4' | grep -o '|' | wc -l
    echo "The number of orthogroups containing all seven highly conserved target isolates is:"
    cat $WorkDir/Orthogroups.txt | grep -e 'Nov5|' | grep -e 'Nov27' | grep -e 'Nov71' | grep -e 'Bc16' | grep -e 'Nov9' | grep -e 'Bc1' | grep -e 'A4' | wc -l
    echo "This represents the following number of genes:"
    cat $WorkDir/Orthogroups.txt | grep -e 'Nov5|' | grep -e 'Nov27' | grep -e 'Nov71' | grep -e 'Bc16' | grep -e 'Nov9' | grep -e 'Bc1' | grep -e 'A4' | grep -o '|' | wc -l
done
```

```
The total number of orthogroups is:
48,151
The total number of genes in orthogroups is:
479,008
The number of orthogroups common to P. rubi is:
2,531
This represents the following number of genes:
7,985
The number of orthogroups common to P. fragariae is:
1,845
This represents the following number of genes:
21,663
The number of orthogroups common to UK1 isolates is:
13
This represents the following number of genes:
26
The number of orthogroups common to UK2 isolates is:
24
This represents the following number of genes:
57
The number of orthogroups common to UK3 isolates is:
2
This represents the following number of genes:
6
The number of orthogroups common to CA4 isolates is:
2,199
This represents the following number of genes:
2,202
The number of orthogroups common to CA5 isolates is:
25
This represents the following number of genes:
51
The number of orthogroups common to Unknown race isolates is:
2,559
This represents the following number of genes:
2,560
The number of orthogroups with only seven highly conserved target isolates is:
42
This represents the following number of genes:
293
The number of orthogroups containing all seven highly conserved target isolates is:
22,824
This represents the following number of genes:
367,953
```

Identification of orthogroups of closely related isolates for further analysis

```bash
for num in 1
do
    echo "The total number of shared orthogroups is:"
    cat $WorkDir/Orthogroups.txt | grep -e 'A4|' | grep -e 'Nov5|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Bc16|' | grep -e 'Nov9|' | grep -e 'Bc1|' | wc -l
    echo "The total number of genes in shared orthogroups is:"
    cat $WorkDir/Orthogroups.txt | grep -e 'A4|' | grep -e 'Nov5|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Bc16|' | grep -e 'Nov9|' | grep -e 'Bc1|' | grep -o '|' | wc -l
    echo "The total number of orthogroups is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc23|' -e 'SCRP245_v2' -e 'Nov77|' -e 'SCRP249' -e 'SCRP324' -e 'SCRP333' | wc -l
    echo "The total number of genes in orthogroups is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'ONT3|' -e 'Bc23|' -e 'SCRP245_v2' -e 'Nov77|' -e 'SCRP249' -e 'SCRP324' -e 'SCRP333' | grep -o '|' | wc -l
    echo "The total number of UK1 orthogroups is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'A4|' -e 'Nov27|' -e 'Nov71|' -e 'Bc16|' -e 'Nov9|' | grep -e 'Nov5|' | grep -e 'Bc1|' | wc -l
    echo "The total number of genes in UK1 orthogroups is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'A4|' -e 'Nov27|' -e 'Nov71|' -e 'Bc16|' -e 'Nov9|' | grep -e 'Nov5|' | grep -e 'Bc1|' | grep -o '|' | wc -l
    echo "The total number of UK2 orthogroups is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Bc1|' -e 'Nov9|' | grep -e 'A4|' | grep -e 'Bc16|' | wc -l
    echo "The total number of genes in UK2 orthogroups is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Bc1|' -e 'Nov9|' | grep -e 'A4|' | grep -e 'Bc16|' | grep -o '|' | wc -l
    echo "The total number of UK3 orthogroups is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'Nov5|' -e 'A4|' -e 'Bc16|' -e 'Bc1|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov9|' | wc -l
    echo "The total number of genes in UK3 orthogroups is:"
    cat $WorkDir/Orthogroups.txt | grep -v -e 'Nov5|' -e 'A4|' -e 'Bc16|' -e 'Bc1|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov9|' | grep -o '|' | wc -l
done
```

```
The total number of shared orthogroups is:
22,522
The total number of genes in shared orthogroups is:
363,776
The total number of orthogroups is:
2,919
The total number of genes in orthogroups is:
4,406
The total number of UK1 orthogroups is:
36
The total number of genes in UK1 orthogroups is:
164
The total number of UK2 orthogroups is:
104
The total number of genes in UK2 orthogroups is:
503
The total number of UK3 orthogroups is:
22
The total number of genes in UK3 orthogroups is:
121
```

##4.5.b Plot venn diagrams:

```bash
ProgDir=/home/adamst/git_repos/scripts/phytophthora_fragariae
$ProgDir/UK1_Pf_venn_diag.r --inp $WorkDir/Orthogroups.tab --out $WorkDir/UK1_orthogroups.pdf
$ProgDir/UK2_Pf_venn_diag.r --inp $WorkDir/Orthogroups.tab --out $WorkDir/UK2_orthogroups.pdf
$ProgDir/UK3_Pf_venn_diag.r --inp $WorkDir/Orthogroups.tab --out $WorkDir/UK3_orthogroups.pdf
```

Output was a pdf file of the venn diagram.

The following additional information was also provided. The format of the following lines is as follows:

Isolate name (total number of orthogroups) number of unique singleton genes number of unique groups of inparalogs

###UK race 1 focused analysis

```
A4
The total number of orthogroups and singleton genes in this isolate:  19,050
The total number of orthogroups and singleton genes not in the venn diagram:  3,675
The total number of singleton genes not in the venn diagram:  1,319
NOV-5
The total number of orthogroups and singleton genes in this isolate:  19,063
The total number of orthogroups and singleton genes not in the venn diagram:  2,368
The total number of singleton genes not in the venn diagram:  1,317
NOV-27
The total number of orthogroups and singleton genes in this isolate:  19,072
The total number of orthogroups and singleton genes not in the venn diagram:  3,697
The total number of singleton genes not in the venn diagram:  1,218
NOV-71
The total number of orthogroups and singleton genes in this isolate:  18,945
The total number of orthogroups and singleton genes not in the venn diagram:  3,570
The total number of singleton genes not in the venn diagram:  1,288
BC-16
The total number of orthogroups and singleton genes in this isolate:  20,096
The total number of orthogroups and singleton genes not in the venn diagram:  4,721
The total number of singleton genes not in the venn diagram:  2,593
NOV-9
The total number of orthogroups and singleton genes in this isolate:  18,942
The total number of orthogroups and singleton genes not in the venn diagram:  3,567
The total number of singleton genes not in the venn diagram:  1,231
BC-1
The total number of orthogroups and singleton genes in this isolate:  19,004
The total number of orthogroups and singleton genes not in the venn diagram:  2,322
The total number of singleton genes not in the venn diagram:  1,228
```

###UK race 2 focused analysis

```
A4
The total number of orthogroups and singleton genes in this isolate:  19,050
The total number of orthogroups and singleton genes not in the venn diagram:  1,648
The total number of singleton genes not in the venn diagram:  1,319
NOV-5
The total number of orthogroups and singleton genes in this isolate:  19,063
The total number of orthogroups and singleton genes not in the venn diagram:  2,992
The total number of singleton genes not in the venn diagram:  1,317
NOV-27
The total number of orthogroups and singleton genes in this isolate:  19,072
The total number of orthogroups and singleton genes not in the venn diagram:  3,001
The total number of singleton genes not in the venn diagram:  1,218
NOV-71
The total number of orthogroups and singleton genes in this isolate:  18,945
The total number of orthogroups and singleton genes not in the venn diagram:  2,874
The total number of singleton genes not in the venn diagram:  1,288
BC-16
The total number of orthogroups and singleton genes in this isolate:  20,096
The total number of orthogroups and singleton genes not in the venn diagram:  1,722
The total number of singleton genes not in the venn diagram:  2,593
NOV-9
The total number of orthogroups and singleton genes in this isolate:  18,942
The total number of orthogroups and singleton genes not in the venn diagram:  2,871
The total number of singleton genes not in the venn diagram:  1,231
BC-1
The total number of orthogroups and singleton genes in this isolate:  19,004
The total number of orthogroups and singleton genes not in the venn diagram:  2,871
The total number of singleton genes not in the venn diagram:  1,228
```

###UK race 3 focused analysis

```
A4
The total number of orthogroups and singleton genes in this isolate:  19,050
The total number of orthogroups and singleton genes not in the venn diagram:  3,513
The total number of singleton genes not in the venn diagram:  1,319
NOV-5
The total number of orthogroups and singleton genes in this isolate:  19,063
The total number of orthogroups and singleton genes not in the venn diagram:  3,526
The total number of singleton genes not in the venn diagram:  1,317
NOV-27
The total number of orthogroups and singleton genes in this isolate:  19,072
The total number of orthogroups and singleton genes not in the venn diagram:  2,292
The total number of singleton genes not in the venn diagram:  1,218
NOV-71
The total number of orthogroups and singleton genes in this isolate:  18,945
The total number of orthogroups and singleton genes not in the venn diagram:  2,146
The total number of singleton genes not in the venn diagram:  1,288
BC-16
The total number of orthogroups and singleton genes in this isolate:  20,096
The total number of orthogroups and singleton genes not in the venn diagram:  4,559
The total number of singleton genes not in the venn diagram:  2,593
NOV-9
The total number of orthogroups and singleton genes in this isolate:  18,942
The total number of orthogroups and singleton genes not in the venn diagram:  2,189
The total number of singleton genes not in the venn diagram:  1,231
BC-1
The total number of orthogroups and singleton genes in this isolate:  19,004
The total number of orthogroups and singleton genes not in the venn diagram:  3,405
The total number of singleton genes not in the venn diagram:  1,228
```

#Analysis of orthogroups unique to UK race 2 (Strains BC-16 & A4)

##The genes unique to Race 2 were identified within the orthology analysis

##First variables were set:

```bash
WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
UK2UniqDir=$WorkDir/UK2_unique
Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
GoodProts=$WorkDir/goodProteins/goodProteins.fasta
Final_genes_Bc16=gene_pred/annotation/P.fragariae/Bc16/Bc16_genes_incl_ORFeffectors.pep.fasta
Final_genes_A4=gene_pred/annotation/P.fragariae/A4/A4_genes_incl_ORFeffectors.pep.fasta
Uniq_UK2_groups=$UK2UniqDir/UK2_uniq_orthogroups.txt
mkdir -p $UK2UniqDir
```

#Orthogroups only containing Race 2 genes were extracted:

##Bars are to prevent incorrect filtering

```bash
for num in 1
do
    cat $Orthogroups | grep -v -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Bc1|' -e 'Nov9|' | grep -e 'A4|' | grep -e 'Bc16|' > $Uniq_UK2_groups
    echo "The number of orthogroups unique to Race UK2 are:"
    cat $Uniq_UK2_groups | wc -l
    echo "The following number genes are contained in these orthogroups:"
    cat $Uniq_UK2_groups | grep -v -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Bc1|' -e 'Nov9|' | grep -e 'A4|' | grep -e 'Bc16|' | grep -o '|' | wc -l
done
```

```
The number of orthogroups unique to Race 2 are:
43
The following number genes are contained in these orthogroups:
201
```

#Race 2 unique RxLR families

#Race 2 RxLR genes were parsed to the same format as the gene names used in the analysis:

```bash
for num in 1
do
    RxLR_Names_Bc16=analysis/RxLR_effectors/combined_evidence/P.fragariae/Bc16/Bc16_Total_RxLR_motif_hmm.txt
    RxLR_Names_A4=analysis/RxLR_effectors/combined_evidence/P.fragariae/A4/A4_Total_RxLR_motif_hmm.txt
    WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
    RxLR_Dir=$WorkDir/UKR2_RxLR
    Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
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
4,859
Of these, the following number were found in orthogroups:
4,763
These were distributed through the following number of Orthogroups:
2,070
The following RxLRs were found in Race 2 unique orthogroups:
7
These orthogroups contain the following number of RxLRs:
16
The following RxLRs were found in P.fragariae unique orthogroups:
2,070
These orthogroups contain the following number of RxLRs:
4,763
```

#The Race 2 RxLR genes that were not found in orthogroups were identified:

```bash
for num in 1
do
    RxLR_UK2_uniq=$RxLR_Dir/UK2_unique_RxLRs.txt
    cat $RxLR_ID | grep -v -w -f $RxLR_Orthogroup_hits > $RxLR_UK2_uniq
    echo "The number of UK2 unique RxLRs are:"
    cat $RxLR_UK2_uniq | wc -l
    RxLR_Seq_Bc16=analysis/RxLR_effectors/combined_evidence/P.fragariae/Bc16/Bc16_final_RxLR.fa
    RxLR_Seq_A4=analysis/RxLR_effectors/combined_evidence/P.fragariae/A4/A4_final_RxLR.fa
    Final_genes_Bc16=gene_pred/annotation/P.fragariae/Bc16/Bc16_genes_incl_ORFeffectors.pep.fasta
    Final_genes_A4=gene_pred/annotation/P.fragariae/A4/A4_genes_incl_ORFeffectors.pep.fasta
    Bc16_RxLR_UK2_uniq_fa=$RxLR_Dir/Bc16_UK2_unique_RxLRs.fa
    A4_RxLR_UK2_uniq_fa=$RxLR_Dir/A4_UK2_unique_RxLRs.fa
    Bc16_to_extract=$RxLR_Dir/Bc16_to_extract.txt
    A4_to_extract=$RxLR_Dir/A4_to_extract.txt
    cat $RxLR_UK2_uniq | grep 'Bc16|' | cut -f2 -d "|" > $Bc16_to_extract
    cat $RxLR_UK2_uniq | grep 'A4|' | cut -f2 -d "|" > $A4_to_extract
    cat $Final_genes_Bc16 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Bc16_to_extract | grep -E -v '^--' > $Bc16_RxLR_UK2_uniq_fa
    cat $Final_genes_A4 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $A4_to_extract | grep -E -v '^--' > $A4_RxLR_UK2_uniq_fa
    echo "The number of BC-16 genes extracted is:"
    cat $Bc16_RxLR_UK2_uniq_fa | grep '>' | wc -l
    echo "The number of A4 genes extracted is:"
    cat $A4_RxLR_UK2_uniq_fa | grep '>' | wc -l
done
```

```
The number of UK2 unique RxLRs are:
96
The number of BC-16 genes extracted is:
69
The number of A4 genes extracted is:
48
```

##Extracting fasta files for orthogroups containing Race 2 putative RxLRs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR2_RxLR/UK2_RxLR_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR2_RxLR/orthogroups_fasta_UK2_RxLR
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```


##Extracting fasta files for P. fragariae orthogroups containing Race 2 putative RxLRs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR2_RxLR/Pf_RxLR_Orthogroups_hits.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR2_RxLR/orthogroups_fasta_Pf_RxLR
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

##Race 2 unique Crinkler families

#Race 2 crinkler genes were parsed to the same format as the gene names used in the analysis:

```bash
for num in 1
do
    CRN_Names_Bc16=analysis/CRN_effectors/hmmer_CRN/P.fragariae/Bc16/Bc16_final_CRN.txt
    CRN_Names_A4=analysis/CRN_effectors/hmmer_CRN/P.fragariae/A4/A4_final_CRN.txt
    WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
    CRN_Dir=$WorkDir/UK2_CRN
    Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
    CRN_ID_UK2=$CRN_Dir/UK2_CRN_hmmer_IDs.txt
    mkdir -p $CRN_Dir
    cat $CRN_Names_Bc16 | sed -r 's/^/Bc16|/g' > $CRN_ID_UK2
    cat $CRN_Names_A4 | sed -r 's/^/A4|/g' >> $CRN_ID_UK2
done
```

#Ortholog groups containing CRN proteins were identified using the following commands:

```bash
for num in 1
do
    echo "The number of CRNs searched for is:"
    cat $CRN_ID_UK2 | wc -l
    echo "Of these, the following number were found in orthogroups:"
    CRN_Orthogroup_hits_UK2=$CRN_Dir/UK2_CRN_Orthogroups_hits.txt
    cat $Orthogroups | grep -o -w -f $CRN_ID_UK2 > $CRN_Orthogroup_hits_UK2
    cat $CRN_Orthogroup_hits_UK2 | wc -l
    echo "These were distributed through the following number of Orthogroups:"
    CRN_Orthogroup_UK2=$CRN_Dir/UK2_CRN_Orthogroups.txt
    cat $Orthogroups | grep -w -f $CRN_ID_UK2 > $CRN_Orthogroup_UK2
    cat $CRN_Orthogroup_UK2 | wc -l
    echo "The following CRNs were found in Race 2 unique orthogroups:"
    CRN_UK2_uniq_groups=$CRN_Dir/UK2_uniq_CRN_Orthogroups_hits.txt
    cat $CRN_Orthogroup_UK2 | grep -v -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Bc1|' -e 'Nov9|' | grep -e 'A4|' | grep -e 'Bc16|' > $CRN_UK2_uniq_groups
    cat $CRN_UK2_uniq_groups | wc -l
    echo "The following CRNs were found in P.fragariae unique orthogroups:"
    CRN_Pf_uniq_groups=$CRN_Dir/Pf_CRN_Orthogroups_hits.txt
    cat $CRN_Orthogroup_UK2 > $CRN_Pf_uniq_groups
    cat $CRN_Pf_uniq_groups | wc -l
    echo "These orthogroups contain the following number of CRNs:"
    cat $CRN_Pf_uniq_groups | grep -w -o -f $CRN_ID_UK2 | wc -l
done
```

```
The number of CRNs searched for is:
231
Of these, the following number were found in orthogroups:
231
These were distributed through the following number of Orthogroups:
72
The following CRNs were found in Race 2 unique orthogroups:
0
The following CRNs were found in P.fragariae unique orthogroups:
72
These orthogroups contain the following number of CRNs:
231
```


#The Race 2 CRN genes not found in orthogroups were identified:

```bash
for num in 1
do
    CRN_UK2_uniq=$CRN_Dir/UK2_unique_CRNs.txt
    cat $CRN_ID_UK2 | grep -v -w -f $CRN_Orthogroup_hits_UK2 > $CRN_UK2_uniq
    echo "The number of UK2 unique CRNs are:"
    cat $CRN_UK2_uniq | wc -l
    CRN_Seq_Bc16=analysis/CRN_effectors/hmmer_CRN/P.fragariae/Bc16/Bc16_final_CRN.fa
    CRN_Seq_A4=analysis/CRN_effectors/hmmer_CRN/P.fragariae/A4/A4_final_CRN.fa
    Final_genes_Bc16=gene_pred/annotation/P.fragariae/Bc16/Bc16_genes_incl_ORFeffectors.pep.fasta
    Final_genes_A4=gene_pred/annotation/P.fragariae/A4/A4_genes_incl_ORFeffectors.pep.fasta
    Bc16_CRN_UK2_uniq_fa=$CRN_Dir/Bc16_UK2_unique_CRNs.fa
    A4_CRN_UK2_uniq_fa=$CRN_Dir/A4_UK2_unique_CRNs.fa
    Bc16_to_extract=$CRN_Dir/Bc16_to_extract.txt
    A4_to_extract=$CRN_Dir/A4_to_extract.txt
    cat $CRN_UK2_uniq | grep 'Bc16|' | cut -f2 -d "|" > $Bc16_to_extract
    cat $CRN_UK2_uniq | grep 'A4|' | cut -f2 -d "|" > $A4_to_extract
    cat $Final_genes_Bc16 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $CRN_UK2_uniq | grep -E -v '^--' > $Bc16_CRN_UK2_uniq_fa
    cat $Final_genes_A4 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $CRN_UK2_uniq | grep -E -v '^--' > $A4_CRN_UK2_uniq_fa
    echo "The number of BC-16 genes extracted is:"
    cat $Bc16_CRN_UK2_uniq_fa | grep '>' | wc -l
    echo "The number of A4 genes extracted is:"
    cat $A4_CRN_UK2_uniq_fa | grep '>' | wc -l
done
```

```
The number of UK2 unique CRNs are:
0
The number of BC-16 genes extracted is:
0
The number of A4 genes extracted is:
0
```

##Extracting fasta files for orthogroups containing Race 2 putative CRNs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK2_CRN/UK2_CRN_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK2_CRN/orthogroups_fasta_UK2_CRN
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

##Extracting fasta files for P. fragariae orthogroups containing Race 2 putative CRNs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK2_CRN/Pf_CRN_Orthogroups_hits.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK2_CRN/orthogroups_fasta_Pf_CRN
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

##Race 2 unique Apoplastic effector families

#Race 2 Apoplastic effectors were parsed to the same format as the gene names used in the analysis:

```bash
for num in 1
do
    ApoP_Names_Bc16=analysis/ApoplastP/P.fragariae/Bc16/Bc16_Total_ApoplastP.txt
    ApoP_Names_A4=analysis/ApoplastP/P.fragariae/A4/A4_Total_ApoplastP.txt
    WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
    ApoP_Dir=$WorkDir/UK2_ApoP
    Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
    ApoP_ID_UK2=$ApoP_Dir/UK2_ApoP_IDs.txt
    mkdir -p $ApoP_Dir
    cat $ApoP_Names_Bc16 | sed -r 's/^/Bc16|/g' > $ApoP_ID_UK2
    cat $ApoP_Names_A4 | sed -r 's/^/A4|/g' >> $ApoP_ID_UK2
done
```

#Ortholog groups containing apoplastic effectors were identified using the following commands:

```bash
for num in 1
do
    echo "The number of apoplastic effectors searched for is:"
    cat $ApoP_ID_UK2 | wc -l
    echo "Of these, the following number were found in orthogroups:"
    ApoP_Orthogroup_hits_UK2=$ApoP_Dir/UK2_ApoP_Orthogroups_hits.txt
    cat $Orthogroups | grep -o -w -f $ApoP_ID_UK2 > $ApoP_Orthogroup_hits_UK2
    cat $ApoP_Orthogroup_hits_UK2 | wc -l
    echo "These were distributed through the following number of Orthogroups:"
    ApoP_Orthogroup_UK2=$ApoP_Dir/UK2_ApoP_Orthogroups.txt
    cat $Orthogroups | grep -w -f $ApoP_ID_UK2 > $ApoP_Orthogroup_UK2
    cat $ApoP_Orthogroup_UK2 | wc -l
    echo "The following apoplastic effectors were found in Race 2 unique orthogroups:"
    ApoP_UK2_uniq_groups=$ApoP_Dir/UK2_uniq_ApoP_Orthogroups_hits.txt
    cat $ApoP_Orthogroup_UK2 | grep -v -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Bc1|' -e 'Nov9|' | grep -e 'A4|' | grep -e 'Bc16|' > $ApoP_UK2_uniq_groups
    cat $ApoP_UK2_uniq_groups | wc -l
    echo "The following apoplastic effectors were found in P.fragariae unique orthogroups:"
    ApoP_Pf_uniq_groups=$ApoP_Dir/Pf_ApoP_Orthogroups_hits.txt
    cat $ApoP_Orthogroup_UK2 > $ApoP_Pf_uniq_groups
    cat $ApoP_Pf_uniq_groups | wc -l
    echo "These orthogroups contain the following number of apoplastic effectors:"
    cat $ApoP_Pf_uniq_groups | grep -w -o -f $ApoP_ID_UK2 | wc -l
done
```

```
The number of apoplastic effectors searched for is:
23,464
Of these, the following number were found in orthogroups:
2,952
These were distributed through the following number of Orthogroups:
1,181
The following apoplastic effectors were found in Race 2 unique orthogroups:
5
The following apoplastic effectors were found in P.fragariae unique orthogroups:
1,181
These orthogroups contain the following number of apoplastic effectors:
2,952
```


#The Race 2 apoplastic effectors not found in orthogroups were identified:

```bash
for num in 1
do
    ApoP_UK2_uniq=$ApoP_Dir/UK2_unique_ApoP.txt
    cat $ApoP_ID_UK2 | grep -v -w -f $ApoP_Orthogroup_hits_UK2 > $ApoP_UK2_uniq
    echo "The number of UK2 unique apoplastic effectors are:"
    cat $ApoP_UK2_uniq | wc -l
    ApoP_Seq_Bc16=analysis/ApoplastP/P.fragariae/Bc16/Bc16_final_ApoplastP.fa
    ApoP_Seq_A4=analysis/ApoplastP/P.fragariae/A4/A4_final_ApoplastP.fa
    Final_genes_Bc16=gene_pred/annotation/P.fragariae/Bc16/Bc16_genes_incl_ORFeffectors.pep.fasta
    Final_genes_A4=gene_pred/annotation/P.fragariae/A4/A4_genes_incl_ORFeffectors.pep.fasta
    Bc16_ApoP_UK2_uniq_fa=$ApoP_Dir/Bc16_UK2_unique_ApoP.fa
    A4_ApoP_UK2_uniq_fa=$ApoP_Dir/A4_UK2_unique_ApoP.fa
    Bc16_to_extract=$ApoP_Dir/Bc16_to_extract.txt
    A4_to_extract=$ApoP_Dir/A4_to_extract.txt
    cat $ApoP_UK2_uniq | grep 'Bc16|' | cut -f2 -d "|" > $Bc16_to_extract
    cat $ApoP_UK2_uniq | grep 'A4|' | cut -f2 -d "|" > $A4_to_extract
    cat $Final_genes_Bc16 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Bc16_to_extract | grep -E -v '^--' > $Bc16_ApoP_UK2_uniq_fa
    cat $Final_genes_A4 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $A4_to_extract | grep -E -v '^--' > $A4_ApoP_UK2_uniq_fa
    echo "The number of BC-16 genes extracted is:"
    cat $Bc16_ApoP_UK2_uniq_fa | grep '>' | wc -l
    echo "The number of A4 genes extracted is:"
    cat $A4_ApoP_UK2_uniq_fa | grep '>' | wc -l
done
```

```
The number of UK2 unique apoplastic effectors are:
20,512
The number of BC-16 genes extracted is:
11,192
The number of A4 genes extracted is:
9,341

These numbers seem excessively large
```

##Extracting fasta files for orthogroups containing Race 2 putative apoplastic effectors

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK2_ApoP/UK2_ApoP_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK2_ApoP/orthogroups_fasta_UK2_ApoP
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

##Extracting fasta files for P. fragariae orthogroups containing Race 2 putative apoplastic effectors

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK2_ApoP/Pf_ApoP_Orthogroups_hits.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK2_ApoP/orthogroups_fasta_Pf_ApoP
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

#Race 2 unique secreted proteins

#Race 2 secreted protein genes were parsed to the same format as the gene names used in the analysis:

```bash
for num in 1
do
    Sec_Names_Bc16=gene_pred/combined_sigP_CQ/P.fragariae/Bc16/Bc16_secreted.txt
    Sec_Names_A4=gene_pred/combined_sigP_CQ/P.fragariae/A4/A4_secreted.txt
    Sec_Names_Bc16_ORFs=gene_pred/combined_sigP_ORF/P.fragariae/Bc16/Bc16_all_secreted_merged.txt
    Sec_Names_A4_ORFs=gene_pred/combined_sigP_ORF/P.fragariae/A4/A4_all_secreted_merged.txt
    WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
    Sec_Dir=$WorkDir/UKR2_Secreted
    Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
    Sec_ID=$Sec_Dir/UKR2_aug_Sec_IDs.txt
    mkdir -p $Sec_Dir
    cat $Sec_Names_Bc16 | sed -r 's/^/Bc16|/g' > $Sec_ID
    cat $Sec_Names_A4 | sed -r 's/^/A4|/g' >> $Sec_ID
    cat $Sec_Names_Bc16_ORFs | sed -r 's/^/Bc16|/g' | sed -r 's/$/.t1/g' >> $Sec_ID
    cat $Sec_Names_A4_ORFs | sed -r 's/^/A4|/g' | sed -r 's/$/.t1/g' >> $Sec_ID
done
```

#Ortholog groups containing Secreted proteins were identified using the following commands:

```bash
for num in 1
do
    echo "The number of secreted proteins searched for is:"
    cat $Sec_ID | wc -l
    echo "Of these, the following number were found in orthogroups:"
    Sec_Orthogroup_hits=$Sec_Dir/UK2_Sec_Orthogroups_hits.txt
    cat $Orthogroups | grep -o -w -f $Sec_ID > $Sec_Orthogroup_hits
    cat $Sec_Orthogroup_hits | wc -l
    echo "These were distributed through the following number of Orthogroups:"
    Sec_Orthogroup=$Sec_Dir/UK2_Sec_Orthogroups.txt
    cat $Orthogroups | grep -w -f $Sec_ID > $Sec_Orthogroup
    cat $Sec_Orthogroup | wc -l
    echo "The following secreted proteins were found in Race 2 unique orthogroups:"
    Sec_UK2_uniq_groups=$Sec_Dir/UK2_uniq_Sec_Orthogroups_hits.txt
    cat $Sec_Orthogroup | grep -v -e 'Nov5|' -e 'Nov27|' -e 'Nov71|' -e 'Bc1|' -e 'Nov9|' | grep -e 'A4|' | grep -e 'Bc16|' > $Sec_UK2_uniq_groups
    cat $Sec_UK2_uniq_groups | wc -l
    echo "These orthogroups contain the following number of secreted proteins:"
    cat $Sec_UK2_uniq_groups | grep -w -o -f $Sec_ID | wc -l
    echo "The following secreted proteins were found in P.fragariae unique orthogroups:"
    Sec_Pf_uniq_groups=$Sec_Dir/Pf_Sec_Orthogroups_hits.txt
    cat $Sec_Orthogroup > $Sec_Pf_uniq_groups
    cat $Sec_Pf_uniq_groups | wc -l
    echo "These orthogroups contain the following number of Secreted proteins:"
    cat $Sec_Pf_uniq_groups | grep -w -o -f $Sec_ID | wc -l
done
```

```
The number of secreted proteins searched for is:
72,134
Of these, the following number were found in orthogroups:
10,949
These were distributed through the following number of Orthogroups:
4,521
The following secreted proteins were found in Race 2 unique orthogroups:
9
These orthogroups contain the following number of secreted proteins:
18
The following secreted proteins were found in P.fragariae unique orthogroups:
4,521
These orthogroups contain the following number of Secreted proteins:
10,949
```

#The Race 2 secreted protein genes that were not found in orthogroups were identified:

```bash
for num in 1
do
    Sec_UK2_uniq=$Sec_Dir/UK2_unique_Sec.txt
    cat $Sec_ID | grep -v -w -f $Sec_Orthogroup_hits > $Sec_UK2_uniq
    echo "The number of UK2 unique secreted proteins are:"
    cat $Sec_UK2_uniq | wc -l
    Final_genes_Bc16=gene_pred/annotation/P.fragariae/Bc16/Bc16_genes_incl_ORFeffectors.pep.fasta
    Final_genes_A4=gene_pred/annotation/P.fragariae/A4/A4_genes_incl_ORFeffectors.pep.fasta
    Bc16_Sec_UK2_uniq_fa=$Sec_Dir/Bc16_UK2_unique_Secs.fa
    A4_Sec_UK2_uniq_fa=$Sec_Dir/A4_UK2_unique_Secs.fa
    Bc16_to_extract=$Sec_Dir/Bc16_to_extract.txt
    A4_to_extract=$Sec_Dir/A4_to_extract.txt
    cat $Sec_UK2_uniq | grep 'Bc16|' | cut -f2 -d "|" > $Bc16_to_extract
    cat $Sec_UK2_uniq | grep 'A4|' | cut -f2 -d "|" > $A4_to_extract
    cat $Final_genes_Bc16 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Bc16_to_extract | grep -E -v '^--' > $Bc16_Sec_UK2_uniq_fa
    cat $Final_genes_A4 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $A4_to_extract | grep -E -v '^--' > $A4_Sec_UK2_uniq_fa
    echo "The number of BC-16 genes extracted is:"
    cat $Bc16_Sec_UK2_uniq_fa | grep '>' | wc -l
    echo "The number of A4 genes extracted is:"
    cat $A4_Sec_UK2_uniq_fa | grep '>' | wc -l
done
```

```
The number of UK2 unique secreted proteins are:
61,185
The number of BC-16 genes extracted is:
10,579
The number of A4 genes extracted is:
8,775
```

##Extracting fasta files for orthogroups containing Race 2 putative secreted proteins

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR2_Secreted/UK2_Sec_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR2_Secreted/orthogroups_fasta_UK2_Sec
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```


##Extracting fasta files for P. fragariae orthogroups containing Race 2 putative secreted proteins

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR2_Secreted/Pf_Sec_Orthogroups_hits.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR2_Secreted/orthogroups_fasta_Pf_Sec
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

#Analysis of orthogroups unique to UK race 1 (Strains BC-1 & NOV-5)

##The genes unique to Race 1 were identified within the orthology analysis

##First variables were set:

```bash
WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
UK1UniqDir=$WorkDir/UK1_unique
Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
GoodProts=$WorkDir/goodProteins/goodProteins.fasta
Final_genes_Bc1=gene_pred/annotation/P.fragariae/Bc1/Bc1_genes_incl_ORFeffectors.pep.fasta
Final_genes_Nov5=gene_pred/annotation/P.fragariae/Nov5/Nov5_genes_incl_ORFeffectors.pep.fasta
Uniq_UK1_groups=$UK1UniqDir/UK1_uniq_orthogroups.txt
mkdir -p $UK1UniqDir
```

#Orthogroups only containing Race 1 genes were extracted:

##Bars are to prevent incorrect filtering

```bash
for num in 1
do
    cat $Orthogroups | grep -v -e 'A4|' -e 'Nov27|' -e 'Nov71|' -e 'Bc16|' -e 'Nov9|' | grep -e 'Nov5|' | grep -e 'Bc1|' > $Uniq_UK1_groups
    echo "The number of orthogroups unique to Race UK1 are:"
    cat $Uniq_UK1_groups | wc -l
    echo "The following number genes are contained in these orthogroups:"
    cat $Uniq_UK1_groups | grep -v -e 'A4|' -e 'Nov27|' -e 'Nov71|' -e 'Bc16|' -e 'Nov9|' | grep -e 'Nov5|' | grep -e 'Bc1|' | grep -o '|' | wc -l
done
```

```
The number of orthogroups unique to Race 1 are:
23
The following number genes are contained in these orthogroups:
99
```

#Race 1 unique RxLR families

#Race 1 RxLR genes were parsed to the same format as the gene names used in the analysis:

```bash
for num in 1
do
    RxLR_Names_Bc1=analysis/RxLR_effectors/combined_evidence/P.fragariae/Bc1/Bc1_Total_RxLR_motif_hmm.txt
    RxLR_Names_Nov5=analysis/RxLR_effectors/combined_evidence/P.fragariae/Nov5/Nov5_Total_RxLR_motif_hmm.txt
    WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
    RxLR_Dir=$WorkDir/UK1_RxLR
    Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
    RxLR_ID=$RxLR_Dir/UK1_aug_RxLR_IDs.txt
    mkdir -p $RxLR_Dir
    cat $RxLR_Names_Bc1 | sed -r 's/^/Bc1|/g' > $RxLR_ID
    cat $RxLR_Names_Nov5 | sed -r 's/^/Nov5|/g' >> $RxLR_ID
done
```

#Ortholog groups containing RxLR proteins were identified using the following commands:

```bash
for num in 1
do
    echo "The number of RxLRs searched for is:"
    cat $RxLR_ID | wc -l
    echo "Of these, the following number were found in orthogroups:"
    RxLR_Orthogroup_hits=$RxLR_Dir/UK1_RxLR_Orthogroups_hits.txt
    cat $Orthogroups | grep -o -w -f $RxLR_ID > $RxLR_Orthogroup_hits
    cat $RxLR_Orthogroup_hits | wc -l
    echo "These were distributed through the following number of Orthogroups:"
    RxLR_Orthogroup=$RxLR_Dir/UK1_RxLR_Orthogroups.txt
    cat $Orthogroups | grep -w -f $RxLR_ID > $RxLR_Orthogroup
    cat $RxLR_Orthogroup | wc -l
    echo "The following RxLRs were found in Race 1 unique orthogroups:"
    RxLR_UK1_uniq_groups=$RxLR_Dir/UK1_uniq_RxLR_Orthogroups_hits.txt
    cat $RxLR_Orthogroup | grep -v -e 'A4|' -e 'Nov27|' -e 'Nov71|' -e 'Bc16|' -e 'Nov9|' | grep -e 'Nov5|' | grep -e 'Bc1|' > $RxLR_UK1_uniq_groups
    cat $RxLR_UK1_uniq_groups | wc -l
    echo "These orthogroups contain the following number of RxLRs:"
    cat $RxLR_UK1_uniq_groups | grep -w -o -f $RxLR_ID | wc -l
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
4,571
Of these, the following number were found in orthogroups:
4,487
These were distributed through the following number of Orthogroups:
2,005
The following RxLRs were found in Race 1 unique orthogroups:
1
These orthogroups contain the following number of RxLRs:
2
The following RxLRs were found in P.fragariae unique orthogroups:
2,005
These orthogroups contain the following number of RxLRs:
4,487
```

#The Race 1 RxLR genes that were not found in orthogroups were identified:

```bash
for num in 1
do
    RxLR_UK1_uniq=$RxLR_Dir/UK1_unique_RxLRs.txt
    cat $RxLR_ID | grep -v -w -f $RxLR_Orthogroup_hits > $RxLR_UK1_uniq
    echo "The number of UK1 unique RxLRs are:"
    cat $RxLR_UK1_uniq | wc -l
    RxLR_Seq_Bc1=analysis/RxLR_effectors/combined_evidence/P.fragariae/Bc1/Bc1_final_RxLR.fa
    RxLR_Seq_Nov5=analysis/RxLR_effectors/combined_evidence/P.fragariae/Nov5/Nov5_final_RxLR.fa
    Final_genes_Bc1=gene_pred/annotation/P.fragariae/Bc1/Bc1_genes_incl_ORFeffectors.pep.fasta
    Final_genes_Nov5=gene_pred/annotation/P.fragariae/Nov5/Nov5_genes_incl_ORFeffectors.pep.fasta
    Bc1_RxLR_UK1_uniq_fa=$RxLR_Dir/Bc1_UK1_unique_RxLRs.fa
    Nov5_RxLR_UK1_uniq_fa=$RxLR_Dir/Nov5_UK1_unique_RxLRs.fa
    Bc1_to_extract=$RxLR_Dir/Bc1_to_extract.txt
    Nov5_to_extract=$RxLR_Dir/Nov5_to_extract.txt
    cat $RxLR_UK1_uniq | grep 'Bc1|' | cut -f2 -d "|" > $Bc1_to_extract
    cat $RxLR_UK1_uniq | grep 'Nov5|' | cut -f2 -d "|" > $Nov5_to_extract
    cat $Final_genes_Bc1 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Bc1_to_extract | grep -E -v '^--' > $Bc1_RxLR_UK1_uniq_fa
    cat $Final_genes_Nov5 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Nov5_to_extract | grep -E -v '^--' > $Nov5_RxLR_UK1_uniq_fa
    echo "The number of BC-1 genes extracted is:"
    cat $Bc1_RxLR_UK1_uniq_fa | grep '>' | wc -l
    echo "The number of NOV-5 genes extracted is:"
    cat $Nov5_RxLR_UK1_uniq_fa | grep '>' | wc -l
done
```

```
The number of UK1 unique RxLRs are:
84
The number of BC-1 genes extracted is:
53
The number of NOV-5 genes extracted is:
49
```

##Extracting fasta files for orthogroups containing Race 1 putative RxLRs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK1_RxLR/UK1_RxLR_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK1_RxLR/orthogroups_fasta_UK1_RxLR
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```


##Extracting fasta files for P. fragariae orthogroups containing Race 1 putative RxLRs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK1_RxLR/Pf_RxLR_Orthogroups_hits.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK1_RxLR/orthogroups_fasta_Pf_RxLR
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

##Race 1 unique Crinkler families

#Race 1 crinkler genes were parsed to the same format as the gene names used in the analysis:

```bash
for num in 1
do
    CRN_Names_Bc1=analysis/CRN_effectors/hmmer_CRN/P.fragariae/Bc1/Bc1_final_CRN.txt
    CRN_Names_Nov5=analysis/CRN_effectors/hmmer_CRN/P.fragariae/Nov5/Nov5_final_CRN.txt
    WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
    CRN_Dir=$WorkDir/UK1_CRN
    Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
    CRN_ID_UK1=$CRN_Dir/UK1_CRN_hmmer_IDs.txt
    mkdir -p $CRN_Dir
    cat $CRN_Names_Bc1 | sed -r 's/^/Bc1|/g' > $CRN_ID_UK1
    cat $CRN_Names_Nov5 | sed -r 's/^/Nov5|/g' >> $CRN_ID_UK1
done
```

#Ortholog groups containing CRN proteins were identified using the following commands:

```bash
for num in 1
do
    echo "The number of CRNs searched for is:"
    cat $CRN_ID_UK1 | wc -l
    echo "Of these, the following number were found in orthogroups:"
    CRN_Orthogroup_hits_UK1=$CRN_Dir/UK1_CRN_Orthogroups_hits.txt
    cat $Orthogroups | grep -o -w -f $CRN_ID_UK1 > $CRN_Orthogroup_hits_UK1
    cat $CRN_Orthogroup_hits_UK1 | wc -l
    echo "These were distributed through the following number of Orthogroups:"
    CRN_Orthogroup_UK1=$CRN_Dir/UK1_CRN_Orthogroups.txt
    cat $Orthogroups | grep -w -f $CRN_ID_UK1 > $CRN_Orthogroup_UK1
    cat $CRN_Orthogroup_UK1 | wc -l
    echo "The following CRNs were found in Race 1 unique orthogroups:"
    CRN_UK1_uniq_groups=$CRN_Dir/UK1_uniq_CRN_Orthogroups_hits.txt
    cat $CRN_Orthogroup_UK1 | grep -v -e 'A4|' -e 'Nov27|' -e 'Nov71|' -e 'Bc16|' -e 'Nov9|' | grep -e 'Nov5|' | grep -e 'Bc1|' > $CRN_UK1_uniq_groups
    cat $CRN_UK1_uniq_groups | wc -l
    echo "The following CRNs were found in P.fragariae unique orthogroups:"
    CRN_Pf_uniq_groups=$CRN_Dir/Pf_CRN_Orthogroups_hits.txt
    cat $CRN_Orthogroup_UK1 > $CRN_Pf_uniq_groups
    cat $CRN_Pf_uniq_groups | wc -l
    echo "These orthogroups contain the following number of CRNs:"
    cat $CRN_Pf_uniq_groups | grep -w -o -f $CRN_ID_UK1 | wc -l
done
```

```
The number of CRNs searched for is:
216
Of these, the following number were found in orthogroups:
216
These were distributed through the following number of Orthogroups:
71
The following CRNs were found in Race 1 unique orthogroups:
0
The following CRNs were found in P.fragariae unique orthogroups:
71
These orthogroups contain the following number of CRNs:
216
```

#The Race 1 CRN genes not found in orthogroups were identified:

```bash
for num in 1
do
    CRN_UK1_uniq=$CRN_Dir/UK1_unique_CRNs.txt
    cat $CRN_ID_UK1 | grep -v -w -f $CRN_Orthogroup_hits_UK1 > $CRN_UK1_uniq
    echo "The number of Race 1 unique CRNs are:"
    cat $CRN_UK1_uniq | wc -l
    CRN_Seq_Bc1=analysis/CRN_effectors/hmmer_CRN/P.fragariae/Bc1/Bc1_final_CRN.fa
    CRN_Seq_Nov5=analysis/CRN_effectors/hmmer_CRN/P.fragariae/Nov5/Nov5_final_CRN.fa
    Final_genes_Bc1=gene_pred/annotation/P.fragariae/Bc1/Bc1_genes_incl_ORFeffectors.pep.fasta
    Final_genes_Nov5=gene_pred/annotation/P.fragariae/Nov5/Nov5_genes_incl_ORFeffectors.pep.fasta
    Bc1_CRN_UK1_uniq_fa=$CRN_Dir/Bc1_UK1_unique_CRNs.fa
    Nov5_CRN_UK1_uniq_fa=$CRN_Dir/Nov5_UK1_unique_CRNs.fa
    Bc1_to_extract=$CRN_Dir/Bc1_to_extract.txt
    Nov5_to_extract=$CRN_Dir/Nov5_to_extract.txt
    cat $CRN_UK1_uniq | grep 'Bc1|' | cut -f2 -d "|" > $Bc1_to_extract
    cat $CRN_UK1_uniq | grep 'Nov5|' | cut -f2 -d "|" > $Nov5_to_extract
    cat $Final_genes_Bc1 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Bc1_to_extract | grep -E -v '^--' > $Bc1_CRN_UK1_uniq_fa
    cat $Final_genes_Nov5 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Nov5_to_extract | grep -E -v '^--' > $Nov5_CRN_UK1_uniq_fa
    echo "The number of BC-1 genes extracted is:"
    cat $Bc1_CRN_UK1_uniq_fa | grep '>' | wc -l
    echo "The number of NOV-5 genes extracted is:"
    cat $Nov5_CRN_UK1_uniq_fa | grep '>' | wc -l
done
```

```
The number of Race 1 unique CRNs are:
0
The number of BC-1 genes extracted is:
0
The number of NOV-5 genes extracted is:
0
```

##Extracting fasta files for orthogroups containing Race 1 putative CRNs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK1_CRN/UK1_CRN_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK1_CRN/orthogroups_fasta_UK1_CRN
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

##Extracting fasta files for P. fragariae orthogroups containing Race 1 putative CRNs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK1_CRN/Pf_CRN_Orthogroups_hits.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK1_CRN/orthogroups_fasta_Pf_CRN
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

##Race 1 unique Apoplastic effector families

#Race 1 Apoplastic effectors were parsed to the same format as the gene names used in the analysis:

```bash
for num in 1
do
    ApoP_Names_Bc1=analysis/ApoplastP/P.fragariae/Bc1/Bc1_Total_ApoplastP.txt
    ApoP_Names_Nov5=analysis/ApoplastP/P.fragariae/Nov5/Nov5_Total_ApoplastP.txt
    WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
    ApoP_Dir=$WorkDir/UK1_ApoP
    Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
    ApoP_ID_UK1=$ApoP_Dir/UK1_ApoP_IDs.txt
    mkdir -p $ApoP_Dir
    cat $ApoP_Names_Bc1 | sed -r 's/^/Bc1|/g' > $ApoP_ID_UK1
    cat $ApoP_Names_Nov5 | sed -r 's/^/Nov5|/g' >> $ApoP_ID_UK1
done
```

#Ortholog groups containing apoplastic effectors were identified using the following commands:

```bash
for num in 1
do
    echo "The number of apoplastic effectors searched for is:"
    cat $ApoP_ID_UK1 | wc -l
    echo "Of these, the following number were found in orthogroups:"
    ApoP_Orthogroup_hits_UK1=$ApoP_Dir/UK1_ApoP_Orthogroups_hits.txt
    cat $Orthogroups | grep -o -w -f $ApoP_ID_UK1 > $ApoP_Orthogroup_hits_UK1
    cat $ApoP_Orthogroup_hits_UK1 | wc -l
    echo "These were distributed through the following number of Orthogroups:"
    ApoP_Orthogroup_UK1=$ApoP_Dir/UK1_ApoP_Orthogroups.txt
    cat $Orthogroups | grep -w -f $ApoP_ID_UK1 > $ApoP_Orthogroup_UK1
    cat $ApoP_Orthogroup_UK1 | wc -l
    echo "The following apoplastic effectors were found in Race 1 unique orthogroups:"
    ApoP_UK1_uniq_groups=$ApoP_Dir/UK1_uniq_ApoP_Orthogroups_hits.txt
    cat $ApoP_Orthogroup_UK1 | grep -v -e 'Bc16|' -e 'Nov27|' -e 'Nov71|' -e 'A4|' -e 'Nov9|' | grep -e 'Bc1|' | grep -e 'Nov5|' > $ApoP_UK1_uniq_groups
    cat $ApoP_UK1_uniq_groups | wc -l
    echo "The following apoplastic effectors were found in P.fragariae unique orthogroups:"
    ApoP_Pf_uniq_groups=$ApoP_Dir/Pf_ApoP_Orthogroups_hits.txt
    cat $ApoP_Orthogroup_UK1 > $ApoP_Pf_uniq_groups
    cat $ApoP_Pf_uniq_groups | wc -l
    echo "These orthogroups contain the following number of apoplastic effectors:"
    cat $ApoP_Pf_uniq_groups | grep -w -o -f $ApoP_ID_UK1 | wc -l
done
```

```
The number of apoplastic effectors searched for is:
21,393
Of these, the following number were found in orthogroups:
2,670
These were distributed through the following number of Orthogroups:
1,143
The following apoplastic effectors were found in Race 1 unique orthogroups:
1
The following apoplastic effectors were found in P.fragariae unique orthogroups:
1,143
These orthogroups contain the following number of apoplastic effectors:
2,670
```


#The Race 1 apoplastic effectors not found in orthogroups were identified:

```bash
for num in 1
do
    ApoP_UK1_uniq=$ApoP_Dir/UK1_unique_ApoP.txt
    cat $ApoP_ID_UK1 | grep -v -w -f $ApoP_Orthogroup_hits_UK1 > $ApoP_UK1_uniq
    echo "The number of UK1 unique apoplastic effectors are:"
    cat $ApoP_UK1_uniq | wc -l
    ApoP_Seq_Bc1=analysis/ApoplastP/P.fragariae/Bc1/Bc1_final_ApoplastP.fa
    ApoP_Seq_Nov5=analysis/ApoplastP/P.fragariae/Nov5/Nov5_final_ApoplastP.fa
    Final_genes_Bc1=gene_pred/annotation/P.fragariae/Bc1/Bc1_genes_incl_ORFeffectors.pep.fasta
    Final_genes_Nov5=gene_pred/annotation/P.fragariae/Nov5/Nov5_genes_incl_ORFeffectors.pep.fasta
    Bc1_ApoP_UK1_uniq_fa=$ApoP_Dir/Bc1_UK1_unique_ApoP.fa
    Nov5_ApoP_UK1_uniq_fa=$ApoP_Dir/Nov5_UK1_unique_ApoP.fa
    Bc1_to_extract=$ApoP_Dir/Bc1_to_extract.txt
    Nov5_to_extract=$ApoP_Dir/Nov5_to_extract.txt
    cat $ApoP_UK1_uniq | grep 'Bc1|' | cut -f2 -d "|" > $Bc1_to_extract
    cat $ApoP_UK1_uniq | grep 'Nov5|' | cut -f2 -d "|" > $Nov5_to_extract
    cat $Final_genes_Bc1 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Bc1_to_extract | grep -E -v '^--' > $Bc1_ApoP_UK1_uniq_fa
    cat $Final_genes_Nov5 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Nov5_to_extract | grep -E -v '^--' > $Nov5_ApoP_UK1_uniq_fa
    echo "The number of BC-1 genes extracted is:"
    cat $Bc1_ApoP_UK1_uniq_fa | grep '>' | wc -l
    echo "The number of Nov5 genes extracted is:"
    cat $Nov5_ApoP_UK1_uniq_fa | grep '>' | wc -l
done
```

```
The number of UK1 unique apoplastic effectors are:
18,723
The number of BC-1 genes extracted is:
9,412
The number of Nov5 genes extracted is:
9,329
```

##Extracting fasta files for orthogroups containing Race 1 putative apoplastic effectors

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK1_ApoP/UK1_ApoP_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK1_ApoP/orthogroups_fasta_UK1_ApoP
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

##Extracting fasta files for P. fragariae orthogroups containing Race 1 putative apoplastic effectors

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK1_ApoP/Pf_ApoP_Orthogroups_hits.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK1_ApoP/orthogroups_fasta_Pf_ApoP
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

#Race 1 unique secreted proteins

#Race 1 secreted protein genes were parsed to the same format as the gene names used in the analysis:

```bash
for num in 1
do
    Sec_Names_Bc1=gene_pred/combined_sigP_CQ/P.fragariae/Bc1/Bc1_secreted.txt
    Sec_Names_Nov5=gene_pred/combined_sigP_CQ/P.fragariae/Nov5/Nov5_secreted.txt
    Sec_Names_Bc1_ORFs=gene_pred/combined_sigP_ORF/P.fragariae/Bc1/Bc1_all_secreted_merged.txt
    Sec_Names_Nov5_ORFs=gene_pred/combined_sigP_ORF/P.fragariae/Nov5/Nov5_all_secreted_merged.txt
    WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
    Sec_Dir=$WorkDir/UKR1_Secreted
    Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
    Sec_ID=$Sec_Dir/UKR1_aug_Sec_IDs.txt
    mkdir -p $Sec_Dir
    cat $Sec_Names_Bc1 | sed -r 's/^/Bc1|/g' > $Sec_ID
    cat $Sec_Names_Nov5 | sed -r 's/^/Nov5|/g' >> $Sec_ID
    cat $Sec_Names_Bc1_ORFs | sed -r 's/^/Bc1|/g' | sed -r 's/$/.t1/g' >> $Sec_ID
    cat $Sec_Names_Nov5_ORFs | sed -r 's/^/Nov5|/g' | sed -r 's/$/.t1/g' >> $Sec_ID
done
```

#Ortholog groups containing Secreted proteins were identified using the following commands:

```bash
for num in 1
do
    echo "The number of secreted proteins searched for is:"
    cat $Sec_ID | wc -l
    echo "Of these, the following number were found in orthogroups:"
    Sec_Orthogroup_hits=$Sec_Dir/UK1_Sec_Orthogroups_hits.txt
    cat $Orthogroups | grep -o -w -f $Sec_ID > $Sec_Orthogroup_hits
    cat $Sec_Orthogroup_hits | wc -l
    echo "These were distributed through the following number of Orthogroups:"
    Sec_Orthogroup=$Sec_Dir/UK1_Sec_Orthogroups.txt
    cat $Orthogroups | grep -w -f $Sec_ID > $Sec_Orthogroup
    cat $Sec_Orthogroup | wc -l
    echo "The following secreted proteins were found in Race 1 unique orthogroups:"
    Sec_UK1_uniq_groups=$Sec_Dir/UK1_uniq_Sec_Orthogroups_hits.txt
    cat $Sec_Orthogroup | grep -v -e 'A4|' -e 'Nov27|' -e 'Nov71|' -e 'Bc16|' -e 'Nov9|' | grep -e 'Nov5|' | grep -e 'Bc1|' > $Sec_UK1_uniq_groups
    cat $Sec_UK1_uniq_groups | wc -l
    echo "These orthogroups contain the following number of secreted proteins:"
    cat $Sec_UK1_uniq_groups | grep -w -o -f $Sec_ID | wc -l
    echo "The following secreted proteins were found in P.fragariae unique orthogroups:"
    Sec_Pf_uniq_groups=$Sec_Dir/Pf_Sec_Orthogroups_hits.txt
    cat $Sec_Orthogroup > $Sec_Pf_uniq_groups
    cat $Sec_Pf_uniq_groups | wc -l
    echo "These orthogroups contain the following number of Secreted proteins:"
    cat $Sec_Pf_uniq_groups | grep -w -o -f $Sec_ID | wc -l
done
```

```
The number of secreted proteins searched for is:
66,470
Of these, the following number were found in orthogroups:
10,268
These were distributed through the following number of Orthogroups:
4,335
The following secreted proteins were found in Race 1 unique orthogroups:
2
These orthogroups contain the following number of secreted proteins:
4
The following secreted proteins were found in P.fragariae unique orthogroups:
4,335
These orthogroups contain the following number of Secreted proteins:
10,268
```

#The Race 1 secreted protein genes that were not found in orthogroups were identified:

```bash
for num in 1
do
    Sec_UK1_uniq=$Sec_Dir/UK1_unique_Sec.txt
    cat $Sec_ID | grep -v -w -f $Sec_Orthogroup_hits > $Sec_UK1_uniq
    echo "The number of UK1 unique secreted proteins are:"
    cat $Sec_UK1_uniq | wc -l
    Final_genes_Bc1=gene_pred/annotation/P.fragariae/Bc1/Bc1_genes_incl_ORFeffectors.pep.fasta
    Final_genes_Nov5=gene_pred/annotation/P.fragariae/Nov5/Nov5_genes_incl_ORFeffectors.pep.fasta
    Bc1_Sec_UK1_uniq_fa=$Sec_Dir/Bc1_UK1_unique_Secs.fa
    Nov5_Sec_UK1_uniq_fa=$Sec_Dir/Nov5_UK1_unique_Secs.fa
    Bc1_to_extract=$Sec_Dir/Bc1_to_extract.txt
    Nov5_to_extract=$Sec_Dir/Nov5_to_extract.txt
    cat $Sec_UK1_uniq | grep 'Bc1|' | cut -f2 -d "|" > $Bc1_to_extract
    cat $Sec_UK1_uniq | grep 'Nov5|' | cut -f2 -d "|" > $Nov5_to_extract
    cat $Final_genes_Bc1 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Bc1_to_extract | grep -E -v '^--' > $Bc1_Sec_UK1_uniq_fa
    cat $Final_genes_Nov5 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Nov5_to_extract | grep -E -v '^--' > $Nov5_Sec_UK1_uniq_fa
    echo "The number of BC-1 genes extracted is:"
    cat $Bc1_Sec_UK1_uniq_fa | grep '>' | wc -l
    echo "The number of Nov5 genes extracted is:"
    cat $Nov5_Sec_UK1_uniq_fa | grep '>' | wc -l
done
```

```
The number of UK1 unique secreted proteins are:
56,202
The number of BC-1 genes extracted is:
8,825
The number of Nov5 genes extracted is:
8,758
```

##Extracting fasta files for orthogroups containing Race 1 putative secreted proteins

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR1_Secreted/UK1_Sec_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR1_Secreted/orthogroups_fasta_UK1_Sec
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

##Extracting fasta files for P. fragariae orthogroups containing Race 1 putative secreted proteins

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR1_Secreted/Pf_Sec_Orthogroups_hits.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR1_Secreted/orthogroups_fasta_Pf_Sec
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

#Analysis of orthogroups unique to UK race 3 (Strains NOV-27, NOV-71 & NOV-9)

##The genes unique to Race 3 were identified within the orthology analysis

##First variables were set:

```bash
WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
UK3UniqDir=$WorkDir/UK3_unique
Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
GoodProts=$WorkDir/goodProteins/goodProteins.fasta
Final_genes_Nov27=gene_pred/annotation/P.fragariae/Nov27/Nov27_genes_incl_ORFeffectors.pep.fasta
Final_genes_Nov71=gene_pred/annotation/P.fragariae/Nov71/Nov71_genes_incl_ORFeffectors.pep.fasta
Final_genes_Nov9=gene_pred/annotation/P.fragariae/Nov9/Nov9_genes_incl_ORFeffectors.pep.fasta
Uniq_UK3_groups=$UK3UniqDir/UK3_uniq_orthogroups.txt
mkdir -p $UK3UniqDir
```

#Orthogroups only containing Race 3 genes were extracted:

##Bars are to prevent incorrect filtering

```bash
for num in 1
do
    cat $Orthogroups | grep -v -e 'A4|' -e 'Nov5|' -e 'Bc1|' -e 'Bc16|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov9|' > $Uniq_UK3_groups
    echo "The number of orthogroups unique to Race UK3 are:"
    cat $Uniq_UK3_groups | wc -l
    echo "The following number genes are contained in these orthogroups:"
    cat $Uniq_UK3_groups | grep -v -e 'A4|' -e 'Nov5|' -e 'Bc1|' -e 'Bc16|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov9|' | grep -o '|' | wc -l
done
```

```
The number of orthogroups unique to Race 3 are:
20
The following number genes are contained in these orthogroups:
89
```

#Race 3 unique RxLR families

#Race 3 RxLR genes were parsed to the same format as the gene names used in the analysis:

```bash
for num in 1
do
    RxLR_Names_Nov27=analysis/RxLR_effectors/combined_evidence/P.fragariae/Nov27/Nov27_Total_RxLR_motif_hmm.txt
    RxLR_Names_Nov71=analysis/RxLR_effectors/combined_evidence/P.fragariae/Nov71/Nov71_Total_RxLR_motif_hmm.txt
    RxLR_Names_Nov9=analysis/RxLR_effectors/combined_evidence/P.fragariae/Nov9/Nov9_Total_RxLR_motif_hmm.txt
    WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
    RxLR_Dir=$WorkDir/UK3_RxLR
    Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
    RxLR_ID=$RxLR_Dir/UK3_aug_RxLR_EER_IDs.txt
    mkdir -p $RxLR_Dir
    cat $RxLR_Names_Nov27 | sed -r 's/^/Nov27|/g' > $RxLR_ID
    cat $RxLR_Names_Nov71 | sed -r 's/^/Nov71|/g' >> $RxLR_ID
    cat $RxLR_Names_Nov9 | sed -r 's/^/Nov9|/g' >> $RxLR_ID
done
```

#Ortholog groups containing RxLR proteins were identified using the following commands:

```bash
for num in 1
do
    echo "The number of RxLRs searched for is:"
    cat $RxLR_ID | wc -l
    echo "Of these, the following number were found in orthogroups:"
    RxLR_Orthogroup_hits=$RxLR_Dir/UK3_RxLR_Orthogroups_hits.txt
    cat $Orthogroups | grep -o -w -f $RxLR_ID > $RxLR_Orthogroup_hits
    cat $RxLR_Orthogroup_hits | wc -l
    echo "These were distributed through the following number of Orthogroups:"
    RxLR_Orthogroup=$RxLR_Dir/UK3_RxLR_Orthogroups.txt
    cat $Orthogroups | grep -w -f $RxLR_ID > $RxLR_Orthogroup
    cat $RxLR_Orthogroup | wc -l
    echo "The following RxLRs were found in Race 3 unique orthogroups:"
    RxLR_UK3_uniq_groups=$RxLR_Dir/UK3_uniq_RxLR_Orthogroups_hits.txt
    cat $RxLR_Orthogroup | grep -v -e 'A4|' -e 'Nov5|' -e 'Bc1|' -e 'Bc16|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov9|' > $RxLR_UK3_uniq_groups
    cat $RxLR_UK3_uniq_groups | wc -l
    echo "These orthogroups contain the following number of RxLRs:"
    cat $RxLR_UK3_uniq_groups | grep -w -o -f $RxLR_ID | wc -l
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
6,854
Of these, the following number were found in orthogroups:
6,739
These were distributed through the following number of Orthogroups:
2,036
The following RxLRs were found in Race 3 unique orthogroups:
1
These orthogroups contain the following number of RxLRs:
3
The following RxLRs were found in P.fragariae unique orthogroups:
2,036
These orthogroups contain the following number of RxLRs:
6,739
```

#The Race 3 RxLR genes that were not found in orthogroups were identified:

```bash
for num in 1
do
    RxLR_UK3_uniq=$RxLR_Dir/UK3_unique_RxLRs.txt
    cat $RxLR_ID | grep -v -w -f $RxLR_Orthogroup_hits > $RxLR_UK3_uniq
    echo "The number of UK3 unique RxLRs are:"
    cat $RxLR_UK3_uniq | wc -l
    RxLR_Seq_Nov27=analysis/RxLR_effectors/combined_evidence/P.fragariae/Nov27/Nov27_final_RxLR.fa
    RxLR_Seq_Nov71=analysis/RxLR_effectors/combined_evidence/P.fragariae/Nov71/Nov71_final_RxLR.fa
    RxLR_Seq_Nov9=analysis/RxLR_effectors/combined_evidence/P.fragariae/Nov9/Nov9_final_RxLR.fa
    Final_genes_Nov27=gene_pred/annotation/P.fragariae/Nov27/Nov27_genes_incl_ORFeffectors.pep.fasta
    Final_genes_Nov71=gene_pred/annotation/P.fragariae/Nov71/Nov71_genes_incl_ORFeffectors.pep.fasta
    Final_genes_Nov9=gene_pred/annotation/P.fragariae/Nov9/Nov9_genes_incl_ORFeffectors.pep.fasta
    Nov27_RxLR_UK3_uniq_fa=$RxLR_Dir/Nov27_UK3_unique_RxLRs.fa
    Nov71_RxLR_UK3_uniq_fa=$RxLR_Dir/Nov71_UK3_unique_RxLRs.fa
    Nov9_RxLR_UK3_uniq_fa=$RxLR_Dir/Nov9_UK3_unique_RxLRs.fa
    Nov27_to_extract=$RxLR_Dir/Nov27_to_extract.txt
    Nov71_to_extract=$RxLR_Dir/Nov71_to_extract.txt
    Nov9_to_extract=$RxLR_Dir/Nov9_to_extract.txt
    cat $RxLR_UK3_uniq | grep 'Nov27|' | cut -f2 -d "|" > $Nov27_to_extract
    cat $RxLR_UK3_uniq | grep 'Nov71|' | cut -f2 -d "|" > $Nov71_to_extract
    cat $RxLR_UK3_uniq | grep 'Nov9|' | cut -f2 -d "|" > $Nov9_to_extract
    cat $Final_genes_Nov27 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Nov27_to_extract | grep -E -v '^--' > $Nov27_RxLR_UK3_uniq_fa
    cat $Final_genes_Nov71 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Nov71_to_extract | grep -E -v '^--' > $Nov71_RxLR_UK3_uniq_fa
    cat $Final_genes_Nov9 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Nov9_to_extract | grep -E -v '^--' > $Nov9_RxLR_UK3_uniq_fa
    echo "The number of NOV-27 genes extracted is:"
    cat $Nov27_RxLR_UK3_uniq_fa | grep '>' | wc -l
    echo "The number of NOV-71 genes extracted is:"
    cat $Nov71_RxLR_UK3_uniq_fa | grep '>' | wc -l
    echo "The number of NOV-9 genes extracted is:"
    cat $Nov9_RxLR_UK3_uniq_fa | grep '>' | wc -l
done
```

```
The number of UK3 unique RxLRs are:
115
The number of NOV-27 genes extracted is:
45
The number of NOV-71 genes extracted is:
47
The number of NOV-9 genes extracted is:
48
```

##Extracting fasta files for orthogroups containing Race 3 putative RxLRs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK3_RxLR/UK3_RxLR_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK3_RxLR/orthogroups_fasta_UK1_RxLR
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```


##Extracting fasta files for P. fragariae orthogroups containing Race 3 putative RxLRs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK3_RxLR/Pf_RxLR_Orthogroups_hits.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK3_RxLR/orthogroups_fasta_Pf_RxLR
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

##Race 3 unique Crinkler families

#Race 3 crinkler genes were parsed to the same format as the gene names used in the analysis:

```bash
for num in 1
do
    CRN_Names_Nov27=analysis/CRN_effectors/hmmer_CRN/P.fragariae/Nov27/Nov27_final_CRN.txt
    CRN_Names_Nov71=analysis/CRN_effectors/hmmer_CRN/P.fragariae/Nov71/Nov71_final_CRN.txt
    CRN_Names_Nov9=analysis/CRN_effectors/hmmer_CRN/P.fragariae/Nov9/Nov9_final_CRN.txt
    WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
    CRN_Dir=$WorkDir/UK3_CRN
    Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
    CRN_ID_UK3=$CRN_Dir/UK3_CRN_hmmer_IDs.txt
    mkdir -p $CRN_Dir
    cat $CRN_Names_Nov27 | sed 's/^/Nov27|/g' > $CRN_ID_UK3
    cat $CRN_Names_Nov71 | sed 's/^/Nov71|/g' >> $CRN_ID_UK3
    cat $CRN_Names_Nov9 | sed 's/^/Nov9|/g' >> $CRN_ID_UK3
done
```

#Ortholog groups containing CRN proteins were identified using the following commands:

```bash
for num in 1
do
    echo "The number of CRNs searched for is:"
    cat $CRN_ID_UK3 | wc -l
    echo "Of these, the following number were found in orthogroups:"
    CRN_Orthogroup_hits_UK3=$CRN_Dir/UK3_CRN_Orthogroups_hits.txt
    cat $Orthogroups | grep -o -w -f $CRN_ID_UK3 > $CRN_Orthogroup_hits_UK3
    cat $CRN_Orthogroup_hits_UK3 | wc -l
    echo "These were distributed through the following number of Orthogroups:"
    CRN_Orthogroup_UK3=$CRN_Dir/UK3_CRN_Orthogroups.txt
    cat $Orthogroups | grep -w -f $CRN_ID_UK3 > $CRN_Orthogroup_UK3
    cat $CRN_Orthogroup_UK3 | wc -l
    echo "The following CRNs were found in Race 3 unique orthogroups:"
    CRN_UK3_uniq_groups=$CRN_Dir/UK3_uniq_CRN_Orthogroups_hits.txt
    cat $CRN_Orthogroup_UK3 | grep -v -e 'A4|' -e 'Nov5|' -e 'Bc1|' -e 'Bc16|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov9|' > $CRN_UK3_uniq_groups
    cat $CRN_UK3_uniq_groups | wc -l
    echo "The following CRNs were found in P.fragariae unique orthogroups:"
    CRN_Pf_uniq_groups=$CRN_Dir/Pf_CRN_Orthogroups_hits.txt
    cat $CRN_Orthogroup_UK3 > $CRN_Pf_uniq_groups
    cat $CRN_Pf_uniq_groups | wc -l
    echo "These orthogroups contain the following number of CRNs:"
    cat $CRN_Pf_uniq_groups | grep -w -o -f $CRN_ID_UK3 | wc -l
done
```

```
The number of CRNs searched for is:
326
Of these, the following number were found in orthogroups:
326
These were distributed through the following number of Orthogroups:
73
The following CRNs were found in Race 3 unique orthogroups:
0
The following CRNs were found in P.fragariae unique orthogroups:
73
These orthogroups contain the following number of CRNs:
326
```

#The Race 3 CRN genes not found in orthogroups were identified:

```bash
for num in 1
do
    CRN_UK3_uniq=$CRN_Dir/UK3_unique_CRNs.txt
    cat $CRN_ID_UK3 | grep -v -w -f $CRN_Orthogroup_hits_UK3 > $CRN_UK3_uniq
    echo "The number of Race 3 unique CRNs are:"
    cat $CRN_UK3_uniq | wc -l
    Final_genes_Nov27=gene_pred/annotation/P.fragariae/Nov27/Nov27_genes_incl_ORFeffectors.pep.fasta
    Final_genes_Nov71=gene_pred/annotation/P.fragariae/Nov71/Nov71_genes_incl_ORFeffectors.pep.fasta
    Final_genes_Nov9=gene_pred/annotation/P.fragariae/Nov9/Nov9_genes_incl_ORFeffectors.pep.fasta
    Nov27_CRN_UK3_uniq_fa=$CRN_Dir/Nov27_UK3_unique_CRNs.fa
    Nov71_CRN_UK3_uniq_fa=$CRN_Dir/Nov71_UK3_unique_CRNs.fa
    Nov9_CRN_UK3_uniq_fa=$CRN_Dir/Nov9_UK3_unique_CRNs.fa
    Nov27_to_extract=$CRN_Dir/Nov27_to_extract.txt
    Nov71_to_extract=$CRN_Dir/Nov71_to_extract.txt
    Nov9_to_extract=$CRN_Dir/Nov9_to_extract.txt
    cat $CRN_UK3_uniq | grep 'Nov27|' | cut -f2 -d "|" > $Nov27_to_extract
    cat $CRN_UK3_uniq | grep 'Nov71|' | cut -f2 -d "|" > $Nov71_to_extract
    cat $CRN_UK3_uniq | grep 'Nov9|' | cut -f2 -d "|" > $Nov9_to_extract
    cat $Final_genes_Nov27 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Nov27_to_extract | grep -E -v '^--' > $Nov27_CRN_UK3_uniq_fa
    cat $Final_genes_Nov71 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Nov71_to_extract | grep -E -v '^--' > $Nov71_CRN_UK3_uniq_fa
    cat $Final_genes_Nov9 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Nov9_to_extract | grep -E -v '^--' > $Nov9_CRN_UK3_uniq_fa
    echo "The number of NOV-27 genes extracted is:"
    cat $Nov27_CRN_UK3_uniq_fa | grep '>' | wc -l
    echo "The number of NOV-71 genes extracted is:"
    cat $Nov71_CRN_UK3_uniq_fa | grep '>' | wc -l
    echo "The number of NOV-9 genes extracted is:"
    cat $Nov9_CRN_UK3_uniq_fa | grep '>' | wc -l
done
```

```
The number of Race 3 unique CRNs are:
0
The number of NOV-27 genes extracted is:
0
The number of NOV-71 genes extracted is:
0
The number of NOV-9 genes extracted is:
0
```

##Extracting fasta files for orthogroups containing Race 3 putative CRNs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK3_CRN/UK3_CRN_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK3_CRN/orthogroups_fasta_UK3_CRN
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

##Extracting fasta files for P. fragariae orthogroups containing Race 3 putative CRNs

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK3_CRN/Pf_CRN_Orthogroups_hits.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK1_CRN/orthogroups_fasta_Pf_CRN
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

##Race 3 unique Apoplastic effector families

#Race 3 Apoplastic effectors were parsed to the same format as the gene names used in the analysis:

```bash
for num in 1
do
    ApoP_Names_Nov27=analysis/ApoplastP/P.fragariae/Nov27/Nov27_Total_ApoplastP.txt
    ApoP_Names_Nov71=analysis/ApoplastP/P.fragariae/Nov71/Nov71_Total_ApoplastP.txt
    ApoP_Names_Nov9=analysis/ApoplastP/P.fragariae/Nov9/Nov9_Total_ApoplastP.txt
    WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
    ApoP_Dir=$WorkDir/UK3_ApoP
    Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
    ApoP_ID_UK3=$ApoP_Dir/UK3_ApoP_IDs.txt
    mkdir -p $ApoP_Dir
    cat $ApoP_Names_Nov27 | sed -r 's/^/Nov27|/g' > $ApoP_ID_UK3
    cat $ApoP_Names_Nov71 | sed -r 's/^/Nov71|/g' >> $ApoP_ID_UK3
    cat $ApoP_Names_Nov9 | sed -r 's/^/Nov9|/g' >> $ApoP_ID_UK3
done
```

#Ortholog groups containing apoplastic effectors were identified using the following commands:

```bash
for num in 1
do
    echo "The number of apoplastic effectors searched for is:"
    cat $ApoP_ID_UK3 | wc -l
    echo "Of these, the following number were found in orthogroups:"
    ApoP_Orthogroup_hits_UK3=$ApoP_Dir/UK3_ApoP_Orthogroups_hits.txt
    cat $Orthogroups | grep -o -w -f $ApoP_ID_UK3 > $ApoP_Orthogroup_hits_UK3
    cat $ApoP_Orthogroup_hits_UK3 | wc -l
    echo "These were distributed through the following number of Orthogroups:"
    ApoP_Orthogroup_UK3=$ApoP_Dir/UK3_ApoP_Orthogroups.txt
    cat $Orthogroups | grep -w -f $ApoP_ID_UK3 > $ApoP_Orthogroup_UK3
    cat $ApoP_Orthogroup_UK3 | wc -l
    echo "The following apoplastic effectors were found in Race 3 unique orthogroups:"
    ApoP_UK3_uniq_groups=$ApoP_Dir/UK3_uniq_ApoP_Orthogroups_hits.txt
    cat $ApoP_Orthogroup_UK3 | grep -v -e 'Nov5|' -e 'A4|' -e 'Bc16|' -e 'Bc1|' | grep -e 'Nov27|' | grep -e 'Nov71|' | grep -e 'Nov9|' > $ApoP_UK3_uniq_groups
    cat $ApoP_UK3_uniq_groups | wc -l
    echo "The following apoplastic effectors were found in P.fragariae unique orthogroups:"
    ApoP_Pf_uniq_groups=$ApoP_Dir/Pf_ApoP_Orthogroups_hits.txt
    cat $ApoP_Orthogroup_UK3 > $ApoP_Pf_uniq_groups
    cat $ApoP_Pf_uniq_groups | wc -l
    echo "These orthogroups contain the following number of apoplastic effectors:"
    cat $ApoP_Pf_uniq_groups | grep -w -o -f $ApoP_ID_UK3 | wc -l
done
```

```
The number of apoplastic effectors searched for is:
32,146
Of these, the following number were found in orthogroups:
4,067
These were distributed through the following number of Orthogroups:
1,171
The following apoplastic effectors were found in Race 3 unique orthogroups:
0
The following apoplastic effectors were found in P.fragariae unique orthogroups:
1,171
These orthogroups contain the following number of apoplastic effectors:
4,067
```


#The Race 3 apoplastic effectors not found in orthogroups were identified:

```bash
for num in 1
do
    ApoP_UK3_uniq=$ApoP_Dir/UK3_unique_ApoP.txt
    cat $ApoP_ID_UK3 | grep -v -w -f $ApoP_Orthogroup_hits_UK3 > $ApoP_UK3_uniq
    echo "The number of UK3 unique apoplastic effectors are:"
    cat $ApoP_UK3_uniq | wc -l
    ApoP_Seq_Nov27=analysis/ApoplastP/P.fragariae/Nov27/Nov27_final_ApoplastP.fa
    ApoP_Seq_Nov71=analysis/ApoplastP/P.fragariae/Nov71/Nov71_final_ApoplastP.fa
    ApoP_Seq_Nov9=analysis/ApoplastP/P.fragariae/Nov9/Nov9_final_ApoplastP.fa
    Final_genes_Nov27=gene_pred/annotation/P.fragariae/Nov27/Nov27_genes_incl_ORFeffectors.pep.fasta
    Final_genes_Nov71=gene_pred/annotation/P.fragariae/Nov71/Nov71_genes_incl_ORFeffectors.pep.fasta
    Final_genes_Nov9=gene_pred/annotation/P.fragariae/Nov9/Nov9_genes_incl_ORFeffectors.pep.fasta
    Nov27_ApoP_UK3_uniq_fa=$ApoP_Dir/Nov27_UK3_unique_ApoP.fa
    Nov71_ApoP_UK3_uniq_fa=$ApoP_Dir/Nov71_UK3_unique_ApoP.fa
    Nov9_ApoP_UK3_uniq_fa=$ApoP_Dir/Nov9_UK3_unique_ApoP.fa
    Nov27_to_extract=$ApoP_Dir/Nov27_to_extract.txt
    Nov71_to_extract=$ApoP_Dir/Nov71_to_extract.txt
    Nov9_to_extract=$ApoP_Dir/Nov9_to_extract.txt
    cat $ApoP_UK3_uniq | grep 'Nov27|' | cut -f2 -d "|" > $Nov27_to_extract
    cat $ApoP_UK3_uniq | grep 'Nov71|' | cut -f2 -d "|" > $Nov71_to_extract
    cat $ApoP_UK3_uniq | grep 'Nov9|' | cut -f2 -d "|" > $Nov9_to_extract
    cat $Final_genes_Nov27 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $ApoP_UK3_uniq | grep -E -v '^--' > $Nov27_ApoP_UK3_uniq_fa
    cat $Final_genes_Nov71 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $ApoP_UK3_uniq | grep -E -v '^--' > $Nov71_ApoP_UK3_uniq_fa
    cat $Final_genes_Nov9 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $ApoP_UK3_uniq | grep -E -v '^--' > $Nov9_ApoP_UK3_uniq_fa
    echo "The number of NOV-27 genes extracted is:"
    cat $Nov27_ApoP_UK3_uniq_fa | grep '>' | wc -l
    echo "The number of NOV-71 genes extracted is:"
    cat $Nov71_ApoP_UK3_uniq_fa | grep '>' | wc -l
    echo "The number of NOV-9 genes extracted is:"
    cat $Nov9_ApoP_UK3_uniq_fa | grep '>' | wc -l
done
```

```
The number of UK3 unique apoplastic effectors are:
28,079
The number of NOV-27 genes extracted is:
0
The number of NOV-71 genes extracted is:
0
The number of NOV-9 genes extracted is:
0
```

##Extracting fasta files for orthogroups containing Race 3 putative apoplastic effectors

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK3_ApoP/UK3_ApoP_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK3_ApoP/orthogroups_fasta_UK3_ApoP
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

##Extracting fasta files for P. fragariae orthogroups containing Race 3 putative apoplastic effectors

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK3_ApoP/Pf_ApoP_Orthogroups_hits.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK3_ApoP/orthogroups_fasta_Pf_ApoP
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

#Race 3 unique secreted proteins

#Race 3 secreted protein genes were parsed to the same format as the gene names used in the analysis:

```bash
for num in 1
do
    Sec_Names_Nov27=gene_pred/combined_sigP_CQ/P.fragariae/Nov27/Nov27_secreted.txt
    Sec_Names_Nov71=gene_pred/combined_sigP_CQ/P.fragariae/Nov71/Nov71_secreted.txt
    Sec_Names_Nov9=gene_pred/combined_sigP_CQ/P.fragariae/Nov9/Nov9_secreted.txt
    Sec_Names_Nov27_ORFs=gene_pred/combined_sigP_ORF/P.fragariae/Nov27/Nov27_all_secreted_merged.txt
    Sec_Names_Nov71_ORFs=gene_pred/combined_sigP_ORF/P.fragariae/Nov71/Nov71_all_secreted_merged.txt
    Sec_Names_Nov9_ORFs=gene_pred/combined_sigP_ORF/P.fragariae/Nov9/Nov9_all_secreted_merged.txt
    WorkDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
    Sec_Dir=$WorkDir/UKR3_Secreted
    Orthogroups=$WorkDir/All_Strains_plus_rubi_no_removal_orthogroups.txt
    Sec_ID=$Sec_Dir/UKR3_aug_Sec_IDs.txt
    mkdir -p $Sec_Dir
    cat $Sec_Names_Nov27 | sed -r 's/^/Nov27|/g' > $Sec_ID
    cat $Sec_Names_Nov71 | sed -r 's/^/Nov71|/g' >> $Sec_ID
    cat $Sec_Names_Nov9 | sed -r 's/^/Nov9|/g' >> $Sec_ID
    cat $Sec_Names_Nov27_ORFs | sed -r 's/^/Nov27|/g' | sed -r 's/$/.t1/g' >> $Sec_ID
    cat $Sec_Names_Nov71_ORFs | sed -r 's/^/Nov71|/g' | sed -r 's/$/.t1/g' >> $Sec_ID
    cat $Sec_Names_Nov9_ORFs | sed -r 's/^/Nov9|/g' | sed -r 's/$/.t1/g' >> $Sec_ID
done
```

#Ortholog groups containing Secreted proteins were identified using the following commands:

```bash
for num in 1
do
    echo "The number of secreted proteins searched for is:"
    cat $Sec_ID | wc -l
    echo "Of these, the following number were found in orthogroups:"
    Sec_Orthogroup_hits=$Sec_Dir/UK3_Sec_Orthogroups_hits.txt
    cat $Orthogroups | grep -o -w -f $Sec_ID > $Sec_Orthogroup_hits
    cat $Sec_Orthogroup_hits | wc -l
    echo "These were distributed through the following number of Orthogroups:"
    Sec_Orthogroup=$Sec_Dir/UK3_Sec_Orthogroups.txt
    cat $Orthogroups | grep -w -f $Sec_ID > $Sec_Orthogroup
    cat $Sec_Orthogroup | wc -l
    echo "The following secreted proteins were found in Race 3 unique orthogroups:"
    Sec_UK3_uniq_groups=$Sec_Dir/UK3_uniq_Sec_Orthogroups_hits.txt
    cat $Sec_Orthogroup | grep -v -e 'A4|' -e 'Bc1|' -e 'Nov5|' -e 'Bc16|' | grep -e 'Nov9|' | grep -e 'Nov27|' | grep -e 'Nov71|' > $Sec_UK3_uniq_groups
    cat $Sec_UK3_uniq_groups | wc -l
    echo "These orthogroups contain the following number of secreted proteins:"
    cat $Sec_UK3_uniq_groups | grep -w -o -f $Sec_ID | wc -l
    echo "The following secreted proteins were found in P.fragariae unique orthogroups:"
    Sec_Pf_uniq_groups=$Sec_Dir/Pf_Sec_Orthogroups_hits.txt
    cat $Sec_Orthogroup > $Sec_Pf_uniq_groups
    cat $Sec_Pf_uniq_groups | wc -l
    echo "These orthogroups contain the following number of Secreted proteins:"
    cat $Sec_Pf_uniq_groups | grep -w -o -f $Sec_ID | wc -l
done
```

```
The number of secreted proteins searched for is:
99,722
Of these, the following number were found in orthogroups:
15,551
These were distributed through the following number of Orthogroups:
4,497
The following secreted proteins were found in Race 3 unique orthogroups:
3
These orthogroups contain the following number of secreted proteins:
9
The following secreted proteins were found in P.fragariae unique orthogroups:
4,497
These orthogroups contain the following number of Secreted proteins:
15,551
```

#The Race 3 secreted protein genes that were not found in orthogroups were identified:

```bash
for num in 1
do
    Sec_UK3_uniq=$Sec_Dir/UK3_unique_Sec.txt
    cat $Sec_ID | grep -v -w -f $Sec_Orthogroup_hits > $Sec_UK3_uniq
    echo "The number of UK3 unique secreted proteins are:"
    cat $Sec_UK3_uniq | wc -l
    Final_genes_Nov27=gene_pred/annotation/P.fragariae/Nov27/Nov27_genes_incl_ORFeffectors.pep.fasta
    Final_genes_Nov71=gene_pred/annotation/P.fragariae/Nov71/Nov71_genes_incl_ORFeffectors.pep.fasta
    Final_genes_Nov9=gene_pred/annotation/P.fragariae/Nov9/Nov9_genes_incl_ORFeffectors.pep.fasta
    Nov27_Sec_UK3_uniq_fa=$Sec_Dir/Nov27_UK3_unique_Secs.fa
    Nov71_Sec_UK3_uniq_fa=$Sec_Dir/Nov71_UK3_unique_Secs.fa
    Nov9_Sec_UK3_uniq_fa=$Sec_Dir/Nov9_UK3_unique_Secs.fa
    Nov27_to_extract=$Sec_Dir/Nov27_to_extract.txt
    Nov71_to_extract=$Sec_Dir/Nov71_to_extract.txt
    Nov9_to_extract=$Sec_Dir/Nov9_to_extract.txt
    cat $Sec_UK3_uniq | grep 'Nov27|' | cut -f2 -d "|" > $Nov27_to_extract
    cat $Sec_UK3_uniq | grep 'Nov71|' | cut -f2 -d "|" > $Nov71_to_extract
    cat $Sec_UK3_uniq | grep 'Nov9|' | cut -f2 -d "|" > $Nov9_to_extract
    cat $Final_genes_Nov27 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Nov27_to_extract | grep -E -v '^--' > $Nov27_Sec_UK3_uniq_fa
    cat $Final_genes_Nov71 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Nov71_to_extract | grep -E -v '^--' > $Nov71_Sec_UK3_uniq_fa
    cat $Final_genes_Nov9 | sed -e 's/\(^>.*$\)/#\1#/' | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d' | grep -w -A1 -f $Nov9_to_extract | grep -E -v '^--' > $Nov9_Sec_UK3_uniq_fa
    echo "The number of NOV-27 genes extracted is:"
    cat $Nov27_Sec_UK3_uniq_fa | grep '>' | wc -l
    echo "The number of NOV-71 genes extracted is:"
    cat $Nov71_Sec_UK3_uniq_fa | grep '>' | wc -l
    echo "The number of NOV-9 genes extracted is:"
    cat $Nov9_Sec_UK3_uniq_fa | grep '>' | wc -l
done
```

```
The number of UK3 unique secreted proteins are:
84,171
The number of NOV-27 genes extracted is:
8,707
The number of NOV-71 genes extracted is:
8,752
The number of NOV-9 genes extracted is:
8,893
```

##Extracting fasta files for orthogroups containing Race 3 putative secreted proteins

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR3_Secreted/UK3_Sec_Orthogroups.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR3_Secreted/orthogroups_fasta_UK3_Sec
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```


##Extracting fasta files for P. fragariae orthogroups containing Race 3 putative secreted proteins

```bash
for num in 1
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR3_Secreted/Pf_Sec_Orthogroups_hits.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UKR3_Secreted/orthogroups_fasta_Pf_Sec
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

#Extract fasta files for all unique orthogroups, including non-effector groups

```bash
for OrthogroupTxt in $(ls analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/UK*_unique/*)
do
    Race=$(echo $OrthogroupTxt | rev | cut -f2 -d '/' | rev)
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/group_fastas/$Race
    mkdir -p $OutDir
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    echo $Race
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```

#Produce a count table of the number of genes for each strain in each groups

```bash
ProgDir=/home/adamst/git_repos/scripts/phytophthora_fragariae
Taxon_code=All_Strains_plus_rubi_no_removal
OrthoMCL_output=analysis/orthology/orthomcl/$Taxon_code/"$Taxon_code"_orthogroups.txt
OutName=analysis/orthology/orthomcl/$Taxon_code/"$Taxon_code"_count_table.tsv
$ProgDir/parse_orthogroups.py --orthogroups $OrthoMCL_output --out_dir $OutName
```

##Analyse this count table for expanded groups and write orthogroups to a text file 'UKX_expanded.txt'

```bash
cd analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal
python /home/adamst/git_repos/scripts/phytophthora_fragariae/orthology_counts.py
```

###Reformat the lists and extract full orthogroup details

```bash
for file in $(ls UK*_expanded.txt)
do
    while IFS=' ' read -r line
    do
        echo $line | sed 's/O/o/g' | sed 's/ //g' >> tmp.txt
    done < "$file"
    Start=$(basename "$file" .txt)
    New_File="$Start"_modified.txt
    while IFS=' ' read -r line
    do
        grep -w "$line" All_Strains_plus_rubi_no_removal_orthogroups.txt >> $New_File
    done < tmp.txt
    rm tmp.txt
done
```

##Extract FASTA files of expanded orthogroups

```bash
for Race in UK1 UK2 UK3
do
    ProgDir=/home/adamst/git_repos/tools/pathogen/orthology/orthoMCL
    OrthogroupTxt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/"$Race"_expanded_modified.txt
    GoodProt=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/goodProteins/goodProteins.fasta
    OutDir=analysis/orthology/orthomcl/All_Strains_plus_rubi_no_removal/"$Race"_expanded
    mkdir -p $OutDir
    $ProgDir/orthoMCLgroups2fasta.py --orthogroups $OrthogroupTxt --fasta $GoodProt --out_dir $OutDir
done
```
