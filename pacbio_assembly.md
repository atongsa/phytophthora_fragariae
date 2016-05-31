##Data extraction

for P. fragariae data:

```bash
cd /home/groups/harrisonlab/project_files/phytophthora_fragariae
RawDatDir=/home/harrir/projects/pacbio_test/p_frag
mkdir -p raw_dna/pacbio/P.fragariae/Bc16
cp -r $RawDatDir/C07_1 raw_dna/pacbio/P.fragariae/Bc16/.
cp -r $RawDatDir/D07_1 raw_dna/pacbio/P.fragariae/Bc16/.
cp -r $RawDatDir/E07_1 raw_dna/pacbio/P.fragariae/Bc16/.
cp -r $RawDatDir/F07_1 raw_dna/pacbio/P.fragariae/Bc16/.
OutDir=raw_dna/pacbio/P.fragariae/Bc16/extracted
mkdir -p $OutDir
cat raw_dna/pacbio/P.fragariae/Bc16/*/Analysis_Results/*.subreads.fastq > $OutDir/concatenated_pacbio.fastq
```

#Canu Assembly

Canu assembly - ran both at genome size of 65m and 95m

```bash
Reads=$(ls raw_dna/pacbio/*/*/extracted/concatenated_pacbio.fastq)
GenomeSz="95m"
Strain=$(echo $Reads | rev | cut -f3 -d '/' | rev)
Organism=$(echo $Reads | rev | cut -f4 -d '/' | rev)
Prefix="$Strain"_canu
OutDir="assembly/canu/$Organism/$Strain/95m"
ProgDir=~/git_repos/tools/seq_tools/assemblers/canu
qsub $ProgDir/submit_canu.sh $Reads $GenomeSz $Prefix $OutDir
```

Assemblies were polished using Pilon

<!-- First, concatenate trimmed reads as have data from two runs of the same library

```bash
IlluminaDirF=qc_dna/paired/P.fragariae/Bc16/F
IlluminaDirR=qc_dna/paired/P.fragariae/Bc16/R
mkdir -p $IlluminaDirF/concatenated
mkdir -p $IlluminaDirR/concatenated
ConcatenatedF=$IlluminaDirF/concatenated/Bc16_cat_F.fq
ConcatenatedR=$IlluminaDirR/concatenated/Bc16_cat_R.fq
cat $IlluminaDirF/Bc16_S1_L001_R1_001_trim.fq.gz > $ConcatenatedF
cat $IlluminaDirF/Bc16_S2_L001_R1_001_160129_trim.fq.gz >> $ConcatenatedF
cat $IlluminaDirR/Bc16_S1_L001_R2_001_trim.fq.gz > $ConcatenatedR
cat $IlluminaDirR/Bc16_S2_L001_R2_001_160129_trim.fq.gz >> $ConcatenatedR
``` -->

Run pilon using each set of reads

```bash
Assembly=assembly/canu/P.fragariae/Bc16/95m/Bc16_canu.contigs.fasta
Organism=P.fragariae
Strain=Bc16
IlluminaDirF=qc_dna/paired/P.fragariae/Bc16/F
IlluminaDirR=qc_dna/paired/P.fragariae/Bc16/R
TrimF1_Read=$IlluminaDirF/Bc16_S1_L001_R1_001_trim.fq.gz
TrimR1_Read=$IlluminaDirR/Bc16_S1_L001_R2_001_trim.fq.gz
OutDir=assembly/canu/$Organism/$Strain/polished/95m/Bc16_S1_L001_R2_001
ProgDir=/home/adamst/git_repos/tools/seq_tools/assemblers/pilon
qsub $ProgDir/sub_pilon.sh $Assembly $TrimF1_Read $TrimR1_Read $OutDir
```

#Spades Assembly

```bash
for PacBioDat in $(ls raw_dna/pacbio/*/*/extracted/concatenated_pacbio.fastq)
do
    Organism=$(echo $PacBioDat | rev | cut -f4 -d '/' | rev)
    Strain=$(echo $PacBioDat | rev | cut -f3 -d '/' | rev)
    IlluminaDir=$(ls -d qc_dna/paired/$Organism/$Strain)
    TrimF1_Read=$(ls $IlluminaDir/F/Bc16_S1_L001_R1_001_trim.fq.gz)
    TrimR1_Read=$(ls $IlluminaDir/R/Bc16_S1_L001_R2_001_trim.fq.gz)
    TrimF2_Read=$(ls $IlluminaDir/F/Bc16_S2_L001_R1_001_160129_trim.fq.gz)
    TrimR2_Read=$(ls $IlluminaDir/R/Bc16_S2_L001_R2_001_160129_trim.fq.gz)
    OutDir=assembly/spades_pacbio/$Organism/"$Strain"
    echo $TrimR1_Read
    echo $TrimR1_Read
    echo $TrimF2_Read
    echo $TrimR2_Read
    ProgDir=/home/armita/git_repos/emr_repos/tools/seq_tools/assemblers/spades/multiple_libraries
    qsub $ProgDir/subSpades_2lib_pacbio.sh $PacBioDat $TrimF1_Read $TrimR1_Read $TrimF2_Read $TrimR2_Read $OutDir 50
done
```

#Filter out contigs < 500bp

```bash
Contigs=assembly/spades_pacbio/P.fragariae/Bc16/contigs.fasta
AssemblyDir=$(dirname $Contigs)
mkdir $AssemblyDir/filtered_contigs
FilterDir=/home/armita/git_repos/emr_repos/tools/seq_tools/assemblers/abyss
$FilterDir/filter_abyss_contigs.py $Contigs 500 > $AssemblyDir/filtered_contigs/contigs_min_500bp.fasta
```

#Merging pacbio and hybrid assemblies

```bash
for PacBioAssembly in $(ls assembly/canu/*/*/polished/95m/*/pilon.fasta)
do
    Organism=P.fragariae
    Strain=Bc16
    Reads=$(echo $PacBioAssembly | rev | cut -f2 -d '/' | rev)
    HybridAssembly=$(ls assembly/spades_pacbio/$Organism/$Strain/contigs.fasta)
    OutDir=assembly/merged_canu_spades/$Organism/$Strain/95m/$Reads
    ProgDir=/home/armita/git_repos/emr_repos/tools/seq_tools/assemblers/quickmerge
    echo $HybridAssembly
    qsub $ProgDir/sub_quickmerge.sh $PacBioAssembly $HybridAssembly $OutDir
done
```
This merged assembly was polished using Pilon

```bash
for Assembly in $(ls assembly/merged_canu_spades/P.fragariae/Bc16/*/merged.fasta)
do
    Organism=P.fragariae
    Strain=Bc16
    Reads=$(echo $Assembly | rev | cut -f2 -d '/' | rev)
    IlluminaDir=$(ls -d qc_dna/paired/$Organism/$Strain)
    TrimF1_Read=$(ls $IlluminaDir/F/"$Reads"_trim.fq.gz)
    TrimR1_Read=$(ls $IlluminaDir/R/"$Reads"_trim.fq.gz)
    OutDir=assembly/merged_canu_spades/$Organism/$Strain/polished/$Reads
    ProgDir=/home/armita/git_repos/emr_repos/tools/seq_tools/assemblers/pilon
    qsub $ProgDir/sub_pilon.sh $Assembly $TrimF1_Read $TrimR1_Read $OutDir
done
```

Contigs were renamed in accordance with ncbi recomendations.

  ProgDir=~/git_repos/emr_repos/tools/seq_tools/assemblers/assembly_qc/remove_contaminants
  touch tmp.csv
  # for Assembly in $(ls assembly/merged_canu_spades/*/*/polished/pilon.fasta); do
  for Assembly in $(ls assembly/pacbio_test/F.oxysporum_fsp_cepae/Fus2_pacbio_merged/polished/pilon.fasta); do
    Organism=$(echo $Assembly | rev | cut -f4 -d '/' | rev)  
    Strain=$(echo $Assembly | rev | cut -f3 -d '/' | rev)
    # OutDir=assembly/merged_canu_spades/$Organism/$Strain/filtered_contigs
    OutDir=assembly/pacbio_test/$Organism/$Strain/filtered_contigs
    mkdir -p $OutDir
    $ProgDir/remove_contaminants.py --inp $Assembly --out $OutDir/"$Strain"_contigs_renamed.fasta --coord_file tmp.csv
  done
  rm tmp.csv
Assembly stats were collected using quast

  ProgDir=/home/armita/git_repos/emr_repos/tools/seq_tools/assemblers/assembly_qc/quast
  # for Assembly in $(ls assembly/merged_canu_spades/*/*/filtered_contigs/Fus2_contigs_renamed.fasta); do
  for Assembly in $(ls assembly/pacbio_test/F.oxysporum_fsp_cepae/Fus2_pacbio_merged/filtered_contigs/Fus2_pacbio_merged_contigs_renamed.fasta); do
    Strain=$(echo $Assembly | rev | cut -f2 -d '/' | rev)
    Organism=$(echo $Assembly | rev | cut -f3 -d '/' | rev)  
    OutDir=$(dirname $Assembly)
    qsub $ProgDir/sub_quast.sh $Assembly $OutDir
  done
