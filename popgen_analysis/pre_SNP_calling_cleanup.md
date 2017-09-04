#Sets up correct formatting for SNP calling analysis

```bash
input=/home/groups/harrisonlab/project_files/phytophthora_fragariae/analysis/genome_alignment/bowtie
scripts=/home/adamst/git_repos/scripts/popgen/snp
```

##Repeat alignments for new FALCON assembly of BC-16

###Single run of data

```bash
Reference=repeat_masked/quiver_results/Bc16/filtered_contigs_repmask/polished_contigs_unmasked.fa
for StrainPath in $(ls -d qc_dna/paired/P.*/* | grep -v -e 'Nov71' -e 'Bc1' -e 'Nov9' -e '62471' -e 'Bc16')
do
    ProgDir=/home/adamst/git_repos/tools/seq_tools/assemblers/spades
    Strain=$(echo $StrainPath | rev | cut -f1 -d '/' | rev)
    Organism=$(echo $StrainPath | rev | cut -f2 -d '/' | rev)
    F_Read=$(ls $StrainPath/F/*_trim.fq.gz)
    R_Read=$(ls $StrainPath/R/*_trim.fq.gz)
    echo $F_Read
    echo $R_Read
    OutDir=analysis/genome_alignment/bowtie/$Organism/$Strain/vs_Bc16_FALCON
    mkdir -p $OutDir
    ProgDir=/home/adamst/git_repos/tools/seq_tools/genome_alignment
    qsub $ProgDir/bowtie/sub_bowtie.sh $Reference $F_Read $R_Read $OutDir
done
```

###Two runs of data

```bash
Reference=repeat_masked/quiver_results/Bc16/filtered_contigs_repmask/polished_contigs_unmasked.fa
for StrainPath in $(ls -d qc_dna/paired/P.*/* | grep -e 'Nov71')
do
    ProgDir=/home/adamst/git_repos/tools/seq_tools/assemblers/spades
    Strain=$(echo $StrainPath | rev | cut -f1 -d '/' | rev)
    Organism=$(echo $StrainPath | rev | cut -f2 -d '/' | rev)
    F1_Read=$(ls $StrainPath/F/*_trim.fq.gz | head -n1 | tail -n1);
    R1_Read=$(ls $StrainPath/R/*_trim.fq.gz | head -n1 | tail -n1);
    F2_Read=$(ls $StrainPath/F/*_trim.fq.gz | head -n2 | tail -n1);
    R2_Read=$(ls $StrainPath/R/*_trim.fq.gz | head -n2 | tail -n1);
    echo $F1_Read
    echo $R1_Read
    echo $F2_Read
    echo $R2_Read
    OutDir=analysis/genome_alignment/bowtie/$Organism/$Strain/vs_Bc16_FALCON
    mkdir -p $OutDir
    ProgDir=/home/armita/git_repos/emr_repos/tools/seq_tools/genome_alignment
    qsub $ProgDir/bowtie/sub_bowtie_2lib.sh $Reference $F1_Read $R1_Read $F2_Read $R2_Read $OutDir
done
```

###Three runs of data

```bash
Reference=repeat_masked/quiver_results/Bc16/filtered_contigs_repmask/polished_contigs_unmasked.fa
for StrainPath in $(ls -d qc_dna/paired/P.*/* | grep -e 'Bc1' -e 'Nov9' | grep -v 'Bc16')
do
    ProgDir=/home/adamst/git_repos/tools/seq_tools/assemblers/spades
    Strain=$(echo $StrainPath | rev | cut -f1 -d '/' | rev)
    Organism=$(echo $StrainPath | rev | cut -f2 -d '/' | rev)
    F1_Read=$(ls $StrainPath/F/*_trim.fq.gz | head -n1 | tail -n1);
    R1_Read=$(ls $StrainPath/R/*_trim.fq.gz | head -n1 | tail -n1);
    F2_Read=$(ls $StrainPath/F/*_trim.fq.gz | head -n2 | tail -n1);
    R2_Read=$(ls $StrainPath/R/*_trim.fq.gz | head -n2 | tail -n1);
    F3_Read=$(ls $StrainPath/F/*_trim.fq.gz | head -n3 | tail -n1);
    R3_Read=$(ls $StrainPath/R/*_trim.fq.gz | head -n3 | tail -n1);
    echo $F1_Read
    echo $R1_Read
    echo $F2_Read
    echo $R2_Read
    echo $F3_Read
    echo $R3_Read
    OutDir=analysis/genome_alignment/bowtie/$Organism/$Strain/vs_Bc16_FALCON
    mkdir -p $OutDir
    ProgDir=/home/armita/git_repos/emr_repos/tools/seq_tools/genome_alignment
    qsub $ProgDir/bowtie/sub_bowtie_3lib.sh $Reference $F1_Read $R1_Read $F2_Read $R2_Read $F3_Read $R3_Read $OutDir
done
```

###For *P. rubi* isolates

```bash
Reference=repeat_masked/quiver_results/Bc16/filtered_contigs_repmask/polished_contigs_unmasked.fa
for StrainPath in $(ls -d ../phytophthora_rubi/qc_dna/paired/P.*/*)
do
    ProgDir=/home/adamst/git_repos/tools/seq_tools/assemblers/spades
    Strain=$(echo $StrainPath | rev | cut -f1 -d '/' | rev)
    Organism=$(echo $StrainPath | rev | cut -f2 -d '/' | rev)
    F_Read=$(ls $StrainPath/F/*_trim.fq.gz)
    R_Read=$(ls $StrainPath/R/*_trim.fq.gz)
    echo $F_Read
    echo $R_Read
    OutDir=analysis/genome_alignment/bowtie/$Organism/$Strain/vs_Bc16_FALCON
    ProgDir=/home/adamst/git_repos/tools/seq_tools/genome_alignment
    qsub $ProgDir/bowtie/sub_bowtie.sh $Reference $F_Read $R_Read $OutDir
done
```

## Rename input mapping files in each folder by prefixing with the strain ID

```bash
cd $input/*/A4/vs_Bc16_FALCON
for filename in polished_contigs_unmasked.fa_aligned.sam
do
    mv "$filename" "A4_$filename"
done

cd $input/*/Bc1/vs_Bc16_FALCON
for filename in polished_contigs_unmasked.fa_aligned.sam
do
    mv "$filename" "Bc1_$filename"
done

cd $input/*/Bc23/vs_Bc16_FALCON
for filename in polished_contigs_unmasked.fa_aligned.sam
do
    mv "$filename" "Bc23_$filename"
done

cd $input/*/Nov27/vs_Bc16_FALCON
for filename in polished_contigs_unmasked.fa_aligned.sam
do
    mv "$filename" "Nov27_$filename"
done

cd $input/*/Nov5/vs_Bc16_FALCON
for filename in polished_contigs_unmasked.fa_aligned.sam
do
    mv "$filename" "Nov5_$filename"
done

cd $input/*/Nov71/vs_Bc16_FALCON
for filename in polished_contigs_unmasked.fa_aligned.sam
do
    mv "$filename" "Nov71_$filename"
done

cd $input/*/Nov77/vs_Bc16_FALCON
for filename in polished_contigs_unmasked.fa_aligned.sam
do
    mv "$filename" "Nov77_$filename"
done

cd $input/*/Nov9/vs_Bc16_FALCON
for filename in polished_contigs_unmasked.fa_aligned.sam
do
    mv "$filename" "Nov9_$filename"
done

cd $input/*/ONT3/vs_Bc16_FALCON
for filename in polished_contigs_unmasked.fa_aligned.sam
do
    mv "$filename" "ONT3_$filename"
done

cd $input/*/SCRP245_v2/vs_Bc16_FALCON
for filename in polished_contigs_unmasked.fa_aligned.sam
do
    mv "$filename" "SCRP245_v2_$filename"
done

cd $input/*/SCRP249/vs_Bc16_FALCON
for filename in polished_contigs_unmasked.fa_aligned.sam
do
    mv "$filename" "SCRP249_$filename"
done

cd $input/*/SCRP324/vs_Bc16_FALCON
for filename in polished_contigs_unmasked.fa_aligned.sam
do
    mv "$filename" "SCRP324_$filename"
done

cd $input/*/SCRP333/vs_Bc16_FALCON
for filename in polished_contigs_unmasked.fa_aligned.sam
do
    mv "$filename" "SCRP333_$filename"
done
```

## Remove multimapping reads, discordant reads. PCR and optical duplicates, and add read group and sample name to each mapped read (preferably, the shortest ID possible)
Convention used:
qsub $scripts/sub_pre_snp_calling.sh <INPUT SAM FILE> <SAMPLE_ID>

```bash
qsub $scripts/sub_pre_snp_calling.sh $input/*/A4/vs_Bc16_FALCON/A4_polished_contigs_unmasked.fa_aligned.sam A4
qsub $scripts/sub_pre_snp_calling.sh $input/*/Bc1/vs_Bc16_FALCON/Bc1_polished_contigs_unmasked.fa_aligned.sam Bc1
qsub $scripts/sub_pre_snp_calling.sh $input/*/Bc16/vs_Bc16_FALCON/Bc16_polished_contigs_unmasked.fa_aligned.sam Bc16
qsub $scripts/sub_pre_snp_calling.sh $input/*/Bc23/vs_Bc16_FALCON/Bc23_polished_contigs_unmasked.fa_aligned.sam Bc23
qsub $scripts/sub_pre_snp_calling.sh $input/*/Nov27/vs_Bc16_FALCON/Nov27_polished_contigs_unmasked.fa_aligned.sam Nov27
qsub $scripts/sub_pre_snp_calling.sh $input/*/Nov5/vs_Bc16_FALCON/Nov5_polished_contigs_unmasked.fa_aligned.sam Nov5
qsub $scripts/sub_pre_snp_calling.sh $input/*/Nov71/vs_Bc16_FALCON/Nov71_polished_contigs_unmasked.fa_aligned.sam Nov71
qsub $scripts/sub_pre_snp_calling.sh $input/*/Nov77/vs_Bc16_FALCON/Nov77_polished_contigs_unmasked.fa_aligned.sam Nov77
qsub $scripts/sub_pre_snp_calling.sh $input/*/Nov9/vs_Bc16_FALCON/Nov9_polished_contigs_unmasked.fa_aligned.sam Nov9
qsub $scripts/sub_pre_snp_calling.sh $input/*/ONT3/vs_Bc16_FALCON/ONT3_polished_contigs_unmasked.fa_aligned.sam ONT3
qsub $scripts/sub_pre_snp_calling.sh $input/*/SCRP245_v2/vs_Bc16_FALCON/SCRP245_v2_polished_contigs_unmasked.fa_aligned.sam SCRP245_v2
qsub $scripts/sub_pre_snp_calling.sh $input/*/SCRP249/vs_Bc16_FALCON/SCRP249_polished_contigs_unmasked.fa_aligned.sam SCRP249
qsub $scripts/sub_pre_snp_calling.sh $input/*/SCRP324/vs_Bc16_FALCON/SCRP324_polished_contigs_unmasked.fa_aligned.sam SCRP324
qsub $scripts/sub_pre_snp_calling.sh $input/*/SCRP333/vs_Bc16_FALCON/SCRP333_polished_contigs_unmasked.fa_aligned.sam SCRP333
```

##Copy outputs from cleanup to alignment folder

```bash
for Strain in A4 Bc1 Bc23 Nov27 Nov5 Nov71 Nov77 Nov9 ONT3 SCRP245_v2 SCRP249 SCRP324 SCRP333
do
    Bam="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup.bam
    rgBam="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup_rg.bam
    Bai="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup_rg.bam.bai
    Txt="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup.txt
    Directory=analysis/genome_alignment/bowtie/*/$Strain/vs_Bc16_unmasked_max1200/
    mv $Bam $Directory
    mv $rgBam $Directory
    mv $Bai $Directory
    mv $Txt $Directory
done
Strain=Bc16
Bam="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup.bam
rgBam="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup_rg.bam
Bai="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup_rg.bam.bai
Txt="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup.txt
Directory=analysis/genome_alignment/bowtie/*/$Strain/vs_Bc16_unmasked_max1200_SNP/
mv $Bam $Directory
mv $rgBam $Directory
mv $Bai $Directory
mv $Txt $Directory
```
