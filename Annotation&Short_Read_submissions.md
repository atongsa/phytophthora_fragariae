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

#### Check gffs for duplication and rename genes

There should not be any duplicatd features - but sanity check.
Renaming is definitely needed and a log file is needed to ensure results of
analyses can still be interpreted. Also create fasta files.

ID duplicate features, ApoplastP means some ORFs are identical to Augustus
genes, check all hits from this script manually in Geneious

```bash
# P.frag
for Gff in $(ls gene_pred/annotation/P.fragariae/*/*_genes_incl_ORFeffectors.gff3)
do
    Organism=$(echo $Gff | rev | cut -d '/' -f3 | rev)
    Isolate=$(echo $Gff | rev | cut -d '/' -f2 | rev)
    echo "$Organism - $Isolate"
    OutDir=$(dirname $Gff)
    ProgDir=/home/adamst/git_repos/tools/gene_prediction/codingquary
    # Check for duplicate features
    $ProgDir/ID_dup_features.py --inp_gff $Gff > $OutDir/Duplicates.txt
done

# P.rubi
for Gff in $(ls ../phytophthora_rubi/gene_pred/annotation/P.rubi/*/*_genes_incl_ORFeffectors.gff3)
do
    Organism=$(echo $Gff | rev | cut -d '/' -f3 | rev)
    Isolate=$(echo $Gff | rev | cut -d '/' -f2 | rev)
    echo "$Organism - $Isolate"
    OutDir=$(dirname $Gff)
    ProgDir=/home/adamst/git_repos/tools/gene_prediction/codingquary
    # Check for duplicate features
    $ProgDir/ID_dup_features.py --inp_gff $Gff > $OutDir/Duplicates.txt
done
```

Use Bedtools to identify locations where ORF effectors overlap Augustus/CQ
predicted genes.

```bash
# P.frag
for GeneGff in $(ls gene_pred/final/*/*/final/final_genes_appended_renamed.gff3)
do
    Isolate=$(echo $GeneGff | rev | cut -d '/' -f3 | rev)
    Organism=$(echo $GeneGff | rev | cut -d '/' -f4 | rev)
    MergeDir=$(ls -d analysis/ApoplastP/$Organism/$Isolate)
    FinalDir=$(ls -d gene_pred/annotation/$Organism/$Isolate)
    RxLR_No_ApoP=$MergeDir/"$Isolate"_RxLR_No_ApoP_ORFs.gff
    RxLR_Plus_ApoP=$MergeDir/"$Isolate"_RxLR_Plus_ApoP_ORFs.gff
    CRN_No_ApoP=$MergeDir/"$Isolate"_CRN_No_ApoP_ORFs.gff
    CRN_Plus_ApoP=$MergeDir/"$Isolate"_CRN_Plus_ApoP_ORFs.gff
    ApoP_No_RxLR_CRN=$MergeDir/"$Isolate"_ApoP_No_RxLR_CRN_ORFs.gff
    bedtools intersect -wo -a $GeneGff -b $RxLR_No_ApoP | grep -e "AUGUSTUS.gene" | grep "RxLR_ORF.gene" | cut -f1,9,18 > $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $RxLR_No_ApoP | grep -e "CodingQuarry_v2.0.gene" | grep "RxLR_ORF.gene" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $RxLR_Plus_ApoP | grep -e "AUGUSTUS.gene" | grep "RxLR_ORF_+_ApoplastP_ORF.gene" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $RxLR_Plus_ApoP | grep -e "CodingQuarry_v2.0.gene" | grep "RxLR_ORF_+_ApoplastP_ORF.gene" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $CRN_No_ApoP | grep -e "AUGUSTUS.gene" | grep "CRN_ORF" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $CRN_No_ApoP | grep -e "CodingQuarry_v2.0.gene" | grep "CRN_ORF" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $CRN_Plus_ApoP | grep -e "AUGUSTUS.gene" | grep "CRN_ORF_+_ApoplastP_ORF" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $CRN_Plus_ApoP | grep -e "CodingQuarry_v2.0.gene" | grep "CRN_ORF_+_ApoplastP_ORF" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $ApoP_No_RxLR_CRN | grep -e "AUGUSTUS.gene" | grep "ApoplastP_ORF" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $ApoP_No_RxLR_CRN | grep -e "CodingQuarry_v2.0.gene" | grep "ApoplastP_ORF" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
done

# P.rubi
for GeneGff in $(ls ../phytophtora_rubi/gene_pred/final/*/*/final/final_genes_appended_renamed.gff3)
do
    Isolate=$(echo $GeneGff | rev | cut -d '/' -f3 | rev)
    Organism=$(echo $GeneGff | rev | cut -d '/' -f4 | rev)
    MergeDir=$(ls -d ../phytophtora_rubi/analysis/ApoplastP/$Organism/$Isolate)
    FinalDir=$(ls -d ../phytophtora_rubi/gene_pred/annotation/$Organism/$Isolate)
    RxLR_No_ApoP=$MergeDir/"$Isolate"_RxLR_No_ApoP_ORFs.gff
    RxLR_Plus_ApoP=$MergeDir/"$Isolate"_RxLR_Plus_ApoP_ORFs.gff
    CRN_No_ApoP=$MergeDir/"$Isolate"_CRN_No_ApoP_ORFs.gff
    CRN_Plus_ApoP=$MergeDir/"$Isolate"_CRN_Plus_ApoP_ORFs.gff
    ApoP_No_RxLR_CRN=$MergeDir/"$Isolate"_ApoP_No_RxLR_CRN_ORFs.gff
    bedtools intersect -wo -a $GeneGff -b $RxLR_No_ApoP | grep -e "AUGUSTUS.gene" | grep "RxLR_ORF.gene" | cut -f1,9,18 > $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $RxLR_No_ApoP | grep -e "CodingQuarry_v2.0.gene" | grep "RxLR_ORF.gene" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $RxLR_Plus_ApoP | grep -e "AUGUSTUS.gene" | grep "RxLR_ORF_+_ApoplastP_ORF.gene" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $RxLR_Plus_ApoP | grep -e "CodingQuarry_v2.0.gene" | grep "RxLR_ORF_+_ApoplastP_ORF.gene" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $CRN_No_ApoP | grep -e "AUGUSTUS.gene" | grep "CRN_ORF" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $CRN_No_ApoP | grep -e "CodingQuarry_v2.0.gene" | grep "CRN_ORF" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $CRN_Plus_ApoP | grep -e "AUGUSTUS.gene" | grep "CRN_ORF_+_ApoplastP_ORF" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $CRN_Plus_ApoP | grep -e "CodingQuarry_v2.0.gene" | grep "CRN_ORF_+_ApoplastP_ORF" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $ApoP_No_RxLR_CRN | grep -e "AUGUSTUS.gene" | grep "ApoplastP_ORF" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
    bedtools intersect -wo -a $GeneGff -b $ApoP_No_RxLR_CRN | grep -e "CodingQuarry_v2.0.gene" | grep "ApoplastP_ORF" | cut -f1,9,18 >> $FinalDir/Overlaps.txt
done
```

Lists of genes to remove were made in same directory as overlap file using nano

Rename the cleaned up gff

```bash
# P.frag
for Gff in $(ls gene_pred/annotation/P.fragariae/*/*_genes_incl_ORFeffectors.gff3)
do
    Organism=$(echo $Gff | rev | cut -d '/' -f3 | rev)
    Isolate=$(echo $Gff | rev | cut -d '/' -f2 | rev)
    echo "$Organism - $Isolate"
    OutDir=$(dirname $Gff)
    ProgDir=/home/adamst/git_repos/tools/gene_prediction/codingquary
    Renamed_Gff=$OutDir/"$Isolate"_genes_incl_ORFeffectors_renamed.gff3
    LogFile=$OutDir/"$Isolate"_genes_appended_renamed.log
    # Rename genes
    $ProgDir/gff_rename_genes.py --inp_gff $Filtered_Gff --conversion_log $LogFile > $Renamed_Gff
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
    # Create Fasta files
    $ProgDir/gff2fasta.pl $Assembly $Renamed_Gff $OutDir/"$Isolate"_genes_incl_ORFeffectors_renamed
    # Corrects * for stop codons to X that NCBI prefer
    sed -i 's/\*/X/g' $OutDir/"$Isolate"_genes_incl_ORFeffectors_renamed.pep.fasta
done

# P.rubi
for Gff in $(ls ../phytophthora_rubi/gene_pred/annotation/P.rubi/*/*_genes_incl_ORFeffectors.gff3)
do
    Organism=$(echo $Gff | rev | cut -d '/' -f3 | rev)
    Isolate=$(echo $Gff | rev | cut -d '/' -f2 | rev)
    echo "$Organism - $Isolate"
    OutDir=$(dirname $Gff)
    ProgDir=/home/adamst/git_repos/tools/gene_prediction/codingquary
    Renamed_Gff=$OutDir/"$Isolate"_genes_incl_ORFeffectors_renamed.gff3
    LogFile=$OutDir/"$Isolate"_genes_appended_renamed.log
    # Rename genes
    $ProgDir/gff_rename_genes.py --inp_gff $Filtered_Gff --conversion_log $LogFile > $Renamed_Gff
    if [ -f repeat_masked/$Organism/$Isolate/ncbi_edits_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls repeat_masked/$Organism/$Isolate/ncbi_edits_repmask/*_softmasked.fa)
        echo $Assembly
    elif [ -f repeat_masked/$Organism/$Isolate/deconseq_Paen_repmask/*_softmasked.fa ]
    then
        Assembly=$(ls repeat_masked/$Organism/$Isolate/deconseq_Paen_repmask/*_softmasked.fa)
        echo $Assembly
    fi
    # Create Fasta files
    $ProgDir/gff2fasta.pl $Assembly $Renamed_Gff $OutDir/"$Isolate"_genes_incl_ORFeffectors_renamed
    # Corrects * for stop codons to X that NCBI prefer
    sed -i 's/\*/X/g' $OutDir/"$Isolate"_genes_incl_ORFeffectors_renamed.pep.fasta
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
```
