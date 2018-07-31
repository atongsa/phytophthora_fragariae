# Commands to prepare gene annotations and raw reads for submission to NCBI

This appears to be a complex procedure, following Andy's commands in
phytophthora repository.
Bioprojects & Biosamples have already been created.
This is for *P. fragariae* and *P. rubi*

## Submission steps

Fasta files were uploaded initially to allow for contamination screen
(See Genbank_corrections.md), however as the MiSeq genomes were submitted as a
batch submission, I have been advised there is no way to update them and the
whole submission has to be repeated.

### Make a table for locus tags

```bash
printf "PF001 SAMN07449679 A4
PF002 SAMN07449680 BC-1
PF003 SAMN07449681 BC-16
PF004 SAMN07449682 BC-23
PF005 SAMN07449683 NOV-27
PF006 SAMN07449684 NOV-5
PF007 SAMN07449685 NOV-71
PF008 SAMN07449686 NOV-77
PF009 SAMN07449687 NOV-9
PF010 SAMN07449688 ONT-3
PF011 SAMN07449689 SCRP245
PR001 SAMN07449690 SCRP249
PR002 SAMN07449691 SCRP324
PR003 SAMN07449692 SCRP333" > genome_submission/Pf_Pr_locus_tags.txt
```

## Prepare files for submission

### Directory structure created

```bash
# P.frag Illumina genomes

for Isolate in A4 Bc1 Bc16 Bc23 Nov27 Nov5 Nov71 Nov77 Nov9 ONT3 SCRP245_v2
do
    Organism=P.fragariae
    echo "$Organism - $Isolate"
    OutDir=genome_submission/$Organism/$Isolate
    mkdir -p $OutDir
done

# P.rubi Illumina genomes

for Isolate in SCRP249 SCRP324 SCRP333
do
    Organism=P.rubi
    echo "$Organism - $Isolate"
    OutDir=genome_submission/$Organism/$Isolate
    mkdir -p $OutDir
done
```

### Sbt file

A template was created from the genbank template tool for A4. The Biosample
was then modified for each isolate. File transferred by scp and modified with
nano. URL below:

```
http://www.ncbi.nlm.nih.gov/WebSub/template.cgi
```

#### Setting variables

Variables containing the locations of files and options for scripts were set

```bash
AnnieDir=/home/armita/prog/annie/genomeannotation-annie-c1e848b
ProgDir=/home/adamst/git_repos/tools/genbank_submission
LabID=AdamsNIABEMR
```

#### Correct duplicate genes - preferentially keep effector calls

```bash
# P.frag
for Gff in $(ls gene_pred/annotation/*/*/*_genes_incl_ORFeffectors.gff3)
do
    Species=$(echo $Gff | rev | cut -f3 -d '/' | rev)
    Isolate=$(echo $Gff | rev | cut -f2 -d '/' | rev)
    echo "$Species - $Isolate"
    Gff_out=gene_pred/annotation/$Species/$Isolate/"$Isolate"_genes_incl_ORFeffectors_nodup.gff3
    Aug_ApoP=analysis/ApoplastP/$Species/$Isolate/*_ApoplastP_headers.txt
    ORF_ApoP=analysis/ApoplastP/$Species/$Isolate/*_ApoplastP_ORF_merged_headers.txt
    Unclear_Genes=gene_pred/annotation/$Species/$Isolate/Unclear_duplicates.txt
    ProgDir=/home/adamst/git_repos/scripts/phytophthora_fragariae
    python $ProgDir/Parse_ApoP_duplicates.py --gff_in $Gff --gff_out $Gff_out --Aug_ApoP $Aug_ApoP --ORF_ApoP $ORF_ApoP --Unclear_Genes $Unclear_Genes
done

# P.rubi
for Gff in $(ls ../phytophthora_rubi/gene_pred/annotation/*/*/*_genes_incl_ORFeffectors.gff3)
do
    Species=$(echo $Gff | rev | cut -f3 -d '/' | rev)
    Isolate=$(echo $Gff | rev | cut -f2 -d '/' | rev)
    echo "$Species - $Isolate"
    Gff_out=../phytophthora_rubi/gene_pred/annotation/$Species/$Isolate/"$Isolate"_genes_incl_ORFeffectors_nodup.gff3
    Aug_ApoP=../phytophthora_rubi/analysis/ApoplastP/$Species/$Isolate/*_ApoplastP_headers.txt
    ORF_ApoP=../phytophthora_rubi/analysis/ApoplastP/$Species/$Isolate/*_ApoplastP_ORF_merged_headers.txt
    Unclear_Genes=../phytophthora_rubi/gene_pred/annotation/$Species/$Isolate/Unclear_duplicates.txt
    ProgDir=/home/adamst/git_repos/scripts/phytophthora_fragariae
    python $ProgDir/Parse_ApoP_duplicates.py --gff_in $Gff --gff_out $Gff_out --Aug_ApoP $Aug_ApoP --ORF_ApoP $ORF_ApoP --Unclear_Genes $Unclear_Genes
done
```

#### Bedtools used to identify intersecting gene models and effector ORFs

```bash
# P.frag
for Gff in $(ls gene_pred/final/*/*/final/final_genes_appended.gff3)
do
    Species=$(echo $Gff | rev | cut -f4 -d '/' | rev)
    Isolate=$(echo $Gff | rev | cut -f3 -d '/' | rev)
    echo "$Species - $Isolate"
    OutDir=gene_pred/annotation/$Species/$Isolate
    MergeDir=analysis/ApoplastP/$Species/$Isolate
    RxLR_No_ApoP=$MergeDir/"$Isolate"_RxLR_No_ApoP_ORFs.gff
    RxLR_Plus_ApoP=$MergeDir/"$Isolate"_RxLR_Plus_ApoP_ORFs.gff
    CRN_No_ApoP=$MergeDir/"$Isolate"_CRN_No_ApoP_ORFs.gff
    CRN_Plus_ApoP=$MergeDir/"$Isolate"_CRN_Plus_ApoP_ORFs.gff
    ApoP_No_RxLR_CRN=$MergeDir/"$Isolate"_ApoP_No_RxLR_CRN_ORFs.gff
    # RxLR_No_ApoP
    bedtools intersect -wo -a $Gff -b $RxLR_No_ApoP | grep -e "AUGUSTUS.gene" -e "CodingQuarry_v2.0.gene" -e "PGNCodingQuarry_v2.0" | grep "RxLR_ORF.gene" | cut -f1,9,18 | sed 's/ID=//g' | tr -d ';' > $OutDir/RxLR_No_ApoP_ORFs_intersecting_non-effector_genes.txt
    # RxLR_Plus_ApoP
    bedtools intersect -wo -a $Gff -b $RxLR_Plus_ApoP | grep -e "AUGUSTUS.gene" -e "CodingQuarry_v2.0.gene" -e "PGNCodingQuarry_v2.0" | grep "RxLR_ORF_+_ApoplastP_ORF.gene" | cut -f1,9,18 | sed 's/ID=//g' | tr -d ';' > $OutDir/RxLR_Plus_ApoP_ORFs_intersecting_non-effector_genes.txt
    # CRN_No_ApoP
    bedtools intersect -wo -a $Gff -b $CRN_No_ApoP | grep -e "AUGUSTUS.gene" -e "CodingQuarry_v2.0.gene" -e "PGNCodingQuarry_v2.0" | grep "CRN_ORF.gene" | cut -f1,9,18 | sed 's/ID=//g' | tr -d ';' > $OutDir/CRN_No_ApoP_ORFs_intersecting_non-effector_genes.txt
    # CRN_Plus_ApoP
    bedtools intersect -wo -a $Gff -b $CRN_Plus_ApoP | grep -e "AUGUSTUS.gene" -e "CodingQuarry_v2.0.gene" -e "PGNCodingQuarry_v2.0" | grep "CRN_ORF_+_ApoplastP_ORF.gene" | cut -f1,9,18 | sed 's/ID=//g' | tr -d ';' > $OutDir/CRN_Plus_ApoP_ORFs_intersecting_non-effector_genes.txt
    # ApoP_No_RxLR_CRN
    bedtools intersect -wo -a $Gff -b $ApoP_No_RxLR_CRN | grep -e "AUGUSTUS.gene" -e "CodingQuarry_v2.0.gene" -e "PGNCodingQuarry_v2.0" | grep "ApoplastP_ORF.gene" | cut -f1,9,18 | sed 's/ID=//g' | tr -d ';' > $OutDir/ApoP_No_RxLR_CRN_ORFs_intersecting_non-effector_genes.txt
done

# P.rubi
for Gff in $(ls ../phytophthora_rubi/gene_pred/final/*/*/final/final_genes_appended.gff3)
do
    Species=$(echo $Gff | rev | cut -f4 -d '/' | rev)
    Isolate=$(echo $Gff | rev | cut -f3 -d '/' | rev)
    echo "$Species - $Isolate"
    OutDir=../phytophthora_rubi/gene_pred/annotation/$Species/$Isolate
    MergeDir=../phytophthora_rubi/analysis/ApoplastP/$Species/$Isolate
    RxLR_No_ApoP=$MergeDir/"$Isolate"_RxLR_No_ApoP_ORFs.gff
    RxLR_Plus_ApoP=$MergeDir/"$Isolate"_RxLR_Plus_ApoP_ORFs.gff
    CRN_No_ApoP=$MergeDir/"$Isolate"_CRN_No_ApoP_ORFs.gff
    CRN_Plus_ApoP=$MergeDir/"$Isolate"_CRN_Plus_ApoP_ORFs.gff
    ApoP_No_RxLR_CRN=$MergeDir/"$Isolate"_ApoP_No_RxLR_CRN_ORFs.gff
    # RxLR_No_ApoP
    bedtools intersect -wo -a $Gff -b $RxLR_No_ApoP | grep -e "AUGUSTUS.gene" -e "CodingQuarry_v2.0.gene" -e "PGNCodingQuarry_v2.0" | grep "RxLR_ORF.gene" | cut -f1,9,18 | sed 's/ID=//g' | tr -d ';' > $OutDir/RxLR_No_ApoP_ORFs_intersecting_non-effector_genes.txt
    # RxLR_Plus_ApoP
    bedtools intersect -wo -a $Gff -b $RxLR_Plus_ApoP | grep -e "AUGUSTUS.gene" -e "CodingQuarry_v2.0.gene" -e "PGNCodingQuarry_v2.0" | grep "RxLR_ORF_+_ApoplastP_ORF.gene" | cut -f1,9,18 | sed 's/ID=//g' | tr -d ';' > $OutDir/RxLR_Plus_ApoP_ORFs_intersecting_non-effector_genes.txt
    # CRN_No_ApoP
    bedtools intersect -wo -a $Gff -b $CRN_No_ApoP | grep -e "AUGUSTUS.gene" -e "CodingQuarry_v2.0.gene" -e "PGNCodingQuarry_v2.0" | grep "CRN_ORF.gene" | cut -f1,9,18 | sed 's/ID=//g' | tr -d ';' > $OutDir/CRN_No_ApoP_ORFs_intersecting_non-effector_genes.txt
    # CRN_Plus_ApoP
    bedtools intersect -wo -a $Gff -b $CRN_Plus_ApoP | grep -e "AUGUSTUS.gene" -e "CodingQuarry_v2.0.gene" -e "PGNCodingQuarry_v2.0" | grep "CRN_ORF_+_ApoplastP_ORF.gene" | cut -f1,9,18 | sed 's/ID=//g' | tr -d ';' > $OutDir/CRN_Plus_ApoP_ORFs_intersecting_non-effector_genes.txt
    # ApoP_No_RxLR_CRN
    bedtools intersect -wo -a $Gff -b $ApoP_No_RxLR_CRN | grep -e "AUGUSTUS.gene" -e "CodingQuarry_v2.0.gene" -e "PGNCodingQuarry_v2.0" | grep "ApoplastP_ORF.gene" | cut -f1,9,18 | sed 's/ID=//g' | tr -d ';' > $OutDir/ApoP_No_RxLR_CRN_ORFs_intersecting_non-effector_genes.txt
done
```

#### Remove genes to ensure no overlapping predictions

```bash
# P.frag
for Gff in $(ls gene_pred/annotation/*/*/*_genes_incl_ORFeffectors_nodup.gff3)
do
    Isolate=$(echo $Gff | rev | cut -f2 -d '/' | rev)
    Species=$(echo $Gff | rev | cut -f3 -d '/' | rev)
    echo "$Species - $Isolate"
    OutDir=$(dirname $Gff)
    cat $OutDir/RxLR_No_ApoP_ORFs_intersecting_non-effector_genes.txt $OutDir/RxLR_Plus_ApoP_ORFs_intersecting_non-effector_genes.txt $OutDir/CRN_No_ApoP_ORFs_intersecting_non-effector_genes.txt $OutDir/CRN_Plus_ApoP_ORFs_intersecting_non-effector_genes.txt $OutDir/ApoP_No_RxLR_CRN_ORFs_intersecting_non-effector_genes.txt | cut -f3 > $OutDir/exclude_list.txt
    PreFilter=$(cat $Gff | grep -w 'gene' | wc -l)
    FilterList=$(cat $OutDir/exclude_list.txt | wc -l)
    UniqueFilterList=$(cat $OutDir/exclude_list.txt | sort | uniq | wc -l)
    GenesRemoved=$(cat $Gff | grep -w -f $OutDir/exclude_list.txt | grep -w 'gene' | wc -l)
    cat $Gff | grep -w -v -f $OutDir/exclude_list.txt > $OutDir/"$Isolate"_genes_incl_ORFeffectors_filtered.gff3
    FinalGenes=$(cat $OutDir/"$Isolate"_genes_incl_ORFeffectors_filtered.gff3 | grep -w 'gene' | wc -l)
    printf "$Species\t$Isolate\t$PreFilter\t$FilterList\t$UniqueFilterList\t$GenesRemoved\t$FinalGenes\n"
done

# P.rubi
for Gff in $(ls ../phytophthora_rubi/gene_pred/annotation/*/*/*_genes_incl_ORFeffectors_nodup.gff3)
do
    Isolate=$(echo $Gff | rev | cut -f2 -d '/' | rev)
    Species=$(echo $Gff | rev | cut -f3 -d '/' | rev)
    echo "$Species - $Isolate"
    OutDir=$(dirname $Gff)
    cat $OutDir/RxLR_No_ApoP_ORFs_intersecting_non-effector_genes.txt $OutDir/RxLR_Plus_ApoP_ORFs_intersecting_non-effector_genes.txt $OutDir/CRN_No_ApoP_ORFs_intersecting_non-effector_genes.txt $OutDir/CRN_Plus_ApoP_ORFs_intersecting_non-effector_genes.txt $OutDir/ApoP_No_RxLR_CRN_ORFs_intersecting_non-effector_genes.txt | cut -f3 > $OutDir/exclude_list.txt
    PreFilter=$(cat $Gff | grep -w 'gene' | wc -l)
    FilterList=$(cat $OutDir/exclude_list.txt | wc -l)
    UniqueFilterList=$(cat $OutDir/exclude_list.txt | sort | uniq | wc -l)
    GenesRemoved=$(cat $Gff | grep -w -f $OutDir/exclude_list.txt | grep -w 'gene' | wc -l)
    cat $Gff | grep -w -v -f $OutDir/exclude_list.txt > $OutDir/"$Isolate"_genes_incl_ORFeffectors_filtered.gff3
    FinalGenes=$(cat $OutDir/"$Isolate"_genes_incl_ORFeffectors_filtered.gff3 | grep -w 'gene' | wc -l)
    printf "$Species\t$Isolate\t$PreFilter\t$FilterList\t$UniqueFilterList\t$GenesRemoved\t$FinalGenes\n"
done
```

```
Species Isolate PreFilter   FilterList  UniqueFilterList    GenesRemoved    FinalGenes
```

#### Check for further duplication, rename the genes and extract fasta files

```bash
# P.frag
for Gff in $(ls gene_pred/annotation/*/*/*_genes_incl_ORFeffectors_filtered.gff3)
do
    Isolate=$(echo $Gff | rev | cut -f2 -d '/' | rev)
    Species=$(echo $Gff | rev | cut -f3 -d '/' | rev)
    echo "$Species - $Isolate"
    OutDir=$(dirname $Gff)
    Gff_Filtered=$OutDir/filtered_duplicates.gff
    ProgDir=/home/adamst/git_repos/tools/gene_prediction/codingquary
    $ProgDir/remove_dup_features.py --inp_gff $Gff -out_gff $Gff_Filtered
    Gff_Renamed=$OutDir/"$Isolate"_genes_incl_ORFeffectors_renamed.gff3
    Log_File=$OutDir/Renaming_log.log
    $ProgDir/gff_rename_genes.py --inp_gff $Gff_Filtered --conversion_log $Log_File > $Gff_Renamed
    rm $Gff_Filtered
    if [ -f repeat_masked/$Organism/$Strain/ncbi_edits_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls repeat_masked/$Organism/$Strain/ncbi_edits_repmask/*_softmasked.fa)
        echo $Assembly
    elif [ -f repeat_masked/$Organism/$Strain/deconseq_Paen_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls repeat_masked/$Organism/$Strain/deconseq_Paen_repmask/*_softmasked.fa)
        echo $Assembly
    else
        Assembly=$(ls repeat_masked/quiver_results/polished/filtered_contigs_repmask/*_softmasked.fa)
        echo $Assembly
    fi
    $ProgDir/gff2fasta.pl $Assembly $GffRenamed $OutDir/"$Isolate"_genes_incl_ORFeffectors_renamed
    # Perl script uses * for stop codons, NCBI want X
    sed -i 's/\*/X/g' $OutDir/"$Isolate"_genes_incl_ORFeffectors_renamed.pep.fasta
done

# P.rubi
for Gff in $(ls ../phytophthora_rubi/gene_pred/annotation/*/*/*_genes_incl_ORFeffectors_filtered.gff3)
do
    Isolate=$(echo $Gff | rev | cut -f2 -d '/' | rev)
    Species=$(echo $Gff | rev | cut -f3 -d '/' | rev)
    echo "$Species - $Isolate"
    OutDir=$(dirname $Gff)
    Gff_Filtered=$OutDir/filtered_duplicates.gff
    ProgDir=/home/adamst/git_repos/tools/gene_prediction/codingquary
    $ProgDir/remove_dup_features.py --inp_gff $Gff -out_gff $Gff_Filtered
    Gff_Renamed=$OutDir/"$Isolate"_genes_incl_ORFeffectors_renamed.gff3
    Log_File=$OutDir/Renaming_log.log
    $ProgDir/gff_rename_genes.py --inp_gff $Gff_Filtered --conversion_log $Log_File > $Gff_Renamed
    rm $Gff_Filtered
    if [ -f repeat_masked/$Organism/$Strain/ncbi_edits_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls repeat_masked/$Organism/$Strain/ncbi_edits_repmask/*_softmasked.fa)
        echo $Assembly
    elif [ -f repeat_masked/$Organism/$Strain/deconseq_Paen_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls repeat_masked/$Organism/$Strain/deconseq_Paen_repmask/*_softmasked.fa)
        echo $Assembly
    fi
    $ProgDir/gff2fasta.pl $Assembly $GffRenamed $OutDir/"$Isolate"_genes_incl_ORFeffectors_renamed
    # Perl script uses * for stop codons, NCBI want X
    sed -i 's/\*/X/g' $OutDir/"$Isolate"_genes_incl_ORFeffectors_renamed.pep.fasta
done
```

##### Collect statistics

```bash
# P.frag
for Transcriptome in $(ls gene_pred/annotation/*/*/*_genes_incl_ORFeffectors_renamed.pep.fasta)
do
    Isolate=$(echo $Transcriptome | rev | cut -f2 -d '/' | rev)
    Species=$(echo $Transcriptome | rev | cut -f3 -d '/' | rev)
    Gff=$(echo $Transcriptome | sed 's/.pep.fasta/.gff3/g')
    Genes=$(cat $Gff | grep -w 'gene' | wc -l)
    Proteins=$(cat $Transcriptome | grep '>' | wc -l)
    printf "$Species\t$Isolate\t$Genes\t$Proteins"
done

# P.rubi
for Transcriptome in $(ls ../phytophthora_rubi/gene_pred/annotation/*/*/*_genes_incl_ORFeffectors_renamed.pep.fasta)
do
    Isolate=$(echo $Transcriptome | rev | cut -f2 -d '/' | rev)
    Species=$(echo $Transcriptome | rev | cut -f3 -d '/' | rev)
    Gff=$(echo $Transcriptome | sed 's/.pep.fasta/.gff3/g')
    Genes=$(cat $Gff | grep -w 'gene' | wc -l)
    Proteins=$(cat $Transcriptome | grep '>' | wc -l)
    printf "$Species\t$Isolate\t$Genes\t$Proteins"
done
```

### Generating .tbl file using GAG

The Genome Annotation Generator (GAG.py) can convert gffs to .tbl files
It can also add interpro & swissprot annotations using Annie

#### Extracting annotations (Annie)

Interpro & Swissprot annotation were extracted using Annie. Output was filtered
to keep only annotations with references to NCBI approved databases
NOTE: transcripts must be re-labeled as mRNA

```bash
# P.frag isolates
for Isolate in A4 Bc1 Bc16 Bc23 Nov27 Nov5 Nov71 Nov77 Nov9 ONT3 SCRP245_v2
do
    Organism=P.fragariae
    echo "$Organism - $Isolate"
    OutDir=genome_submission/$Organism/$Isolate
    Gff=$(ls gene_pred/annotation/$Organism/$Isolate/"$Isolate"_genes_incl_ORFeffectors.gff3)
    InterProTab=$(ls gene_pred/interproscan/$Organism/$Isolate/greedy/"$Isolate"_interproscan.tsv)
    SwissProtBlast=$(ls gene_pred/swissprot/$Organism/$Isolate/greedy/swissprot_vJul2016_tophit_parsed.tbl)
    SwissProtFasta=/home/groups/harrisonlab/uniprot/swissprot/uniprot_sprot.fasta
    python $AnnieDir/annie.py -ipr $InterProTab -g $GffFile -b $SwissProtBlast -db $SwissProtFasta -o $OutDir/annie_output.csv --fix_bad_products
    ProgDir=/home/adamst/git_repos/tools/genbank_submission
    $ProgDir/edit_tbl_file/annie_corrector.py --inp_csv $OutDir/annie_output.csv --out_csv $OutDir/annie_corrected_output.csv
done

# P.rubi isolates
for Isolate in SCRP249 SCRP324 SCRP333
do
    Organism=P.fragariae
    echo "$Organism - $Isolate"
    OutDir=genome_submission/$Organism/$Isolate
    Gff=$(ls ../phytophthora_rubi/gene_pred/annotation/$Organism/$Isolate/"$Isolate"_genes_incl_ORFeffectors.gff3)
    InterProTab=$(ls ../phytophthora_rubi/gene_pred/interproscan/$Organism/$Isolate/greedy/"$Isolate"_interproscan.tsv)
    SwissProtBlast=$(ls ../phytophthora_rubi/gene_pred/swissprot/$Organism/$Isolate/greedy/swissprot_vJul2016_tophit_parsed.tbl)
    SwissProtFasta=/home/groups/harrisonlab/uniprot/swissprot/uniprot_sprot.fasta
    python $AnnieDir/annie.py -ipr $InterProTab -g $GffFile -b $SwissProtBlast -db $SwissProtFasta -o $OutDir/annie_output.csv --fix_bad_products
    ProgDir=/home/adamst/git_repos/tools/genbank_submission
    $ProgDir/edit_tbl_file/annie_corrector.py --inp_csv $OutDir/annie_output.csv --out_csv $OutDir/annie_corrected_output.csv
done
```

#### Running GAG

GAG was run using the modified GFF as well as the output of annie. Outputs database references incorrectly, so these are modified

```bash
# P.frag
for Isolate in A4 Bc1 Bc16 Bc23 Nov27 Nov5 Nov71 Nov77 Nov9 ONT3 SCRP245_v2
do
    Organism=P.fragariae
    echo "$Organism - $Isolate"
    if [ -f repeat_masked/$Organism/$Isolate/ncbi_edits_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls repeat_masked/$Organism/$Isolate/ncbi_edits_repmask/*_softmasked.fa)
        echo $Assembly
    elif [ -f repeat_masked/$Organism/$Isolate/deconseq_Paen_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls repeat_masked/$Organism/$Isolate/deconseq_Paen_repmask/*_softmasked.fa)
        echo $Assembly
    else
        Assembly=$(ls repeat_masked/quiver_results/polished/filtered_contigs_repmask/*_softmasked.fa)
        echo $Assembly
    fi
    OutDir=genome_submission/$Organism/$Isolate
    Gff=$(ls gene_pred/annotation/$Organism/$Isolate/"$Isolate"_genes_incl_ORFeffectors.gff3)
    mkdir -p $OutDir/gag/round_1
    gag.py -f $Assembly -g $Gff -a $OutDir/annie_corrected_output.csv --fix_start_stop -o $OutDir/gag/round_1 2>&1 | tee $OutDir/gag_log_1.txt
    sed -i 's/Dbxref/db_xref/g' $OutDir/gag/round_1/genome.tbl
done

# P.rubi
for Isolate in SCRP249 SCRP34 SCRP333
do
    Organism=P.rubi
    echo "$Organism - $Isolate"
    if [ -f ../phytophthora_rubi/repeat_masked/$Organism/$Isolate/ncbi_edits_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls ../phytophthora_rubi/repeat_masked/$Organism/$Isolate/ncbi_edits_repmask/*_softmasked.fa)
        echo $Assembly
    elif [ -f ../phytophthora_rubi/repeat_masked/$Organism/$Isolate/deconseq_Paen_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls ../phytophthora_rubi/repeat_masked/$Organism/$Isolate/deconseq_Paen_repmask/*_softmasked.fa)
        echo $Assembly
    fi
    OutDir=genome_submission/$Organism/$Isolate
    Gff=$(ls ../phytophthora_rubi/gene_pred/annotation/$Organism/$Isolate/"$Isolate"_genes_incl_ORFeffectors.gff3)
    mkdir -p $OutDir/gag/round_1
    gag.py -f $Assembly -g $Gff -a $OutDir/annie_corrected_output.csv --fix_start_stop -o $OutDir/gag/round_1 2>&1 | tee $OutDir/gag_log_1.txt
    sed -i 's/Dbxref/db_xref/g' $OutDir/gag/round_1/genome.tbl
done
```

### tbl2asn round 1

tbl2asn was run to collect error reports on the current formatting.
All input files must be in same dir with same basename

```bash
# P.frag
for Isolate in A4 Bc1 Bc16 Bc23 Nov27 Nov5 Nov71 Nov77 Nov9 ONT3 SCRP245_v2
do
    Organism=P.fragariae
    echo "$Organism - $Isolate"
    OutDir=genome_submission/$Organism/$Isolate
    if [ -f repeat_masked/$Organism/$Isolate/ncbi_edits_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls repeat_masked/$Organism/$Isolate/ncbi_edits_repmask/*_softmasked.fa)
        echo $Assembly
    elif [ -f repeat_masked/$Organism/$Isolate/deconseq_Paen_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls repeat_masked/$Organism/$Isolate/deconseq_Paen_repmask/*_softmasked.fa)
        echo $Assembly
    else
        Assembly=$(ls repeat_masked/quiver_results/polished/filtered_contigs_repmask/*_softmasked.fa)
        echo $Assembly
    fi
    cp $Assembly $OutDir/gag/round_1/genome.fsa
    SbtFile=genome_submission/$Organism/$Isolate/template.sbt
    mkdir -p $OutDir/tbl2asn/round_1
    tbl2asn -p $OutDir/gag/round_1/. -t $OutDir/gag/round_1/template.sbt -r $OutDir/tbl2asn/round_1 -M n -X E -Z $OutDir/gag/round_1/discrep.txt -j "[organism=$Organism] [strain=$Isolate]"
done

# P.rubi
for Isolate in SCRP249 SCRP324 SCRP333
do
    Organism=P.rubi
    echo "$Organism - $Isolate"
    OutDir=genome_submission/$Organism/$Isolate
    if [ -f ../pythophthora_rubi/repeat_masked/$Organism/$Isolate/ncbi_edits_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls ../pythophthora_rubi/repeat_masked/$Organism/$Isolate/ncbi_edits_repmask/*_softmasked.fa)
        echo $Assembly
    elif [ -f ../pythophthora_rubi/repeat_masked/$Organism/$Isolate/deconseq_Paen_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls ../pythophthora_rubi/repeat_masked/$Organism/$Isolate/deconseq_Paen_repmask/*_softmasked.fa)
        echo $Assembly
    fi
    cp $Assembly $OutDir/gag/round_1/genome.fsa
    SbtFile=genome_submission/$Organism/$Isolate/template.sbt
    mkdir -p $OutDir/tbl2asn/round_1
    tbl2asn -p $OutDir/gag/round_1/. -t $OutDir/gag/round_1/template.sbt -r $OutDir/tbl2asn/round_1 -M n -X E -Z $OutDir/gag/round_1/discrep.txt -j "[organism=$Organism] [strain=$Isolate]"
done
```
