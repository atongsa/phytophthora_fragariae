#Preparing alignments and finding best-fit nucleotide sequence evolution models

```bash
path=/home/groups/harrisonlab/project_files/phytophthora_fragariae/phylogeny
scripts=/home/adamst/git_repos/scripts/popgen/phylogenetics
```

#Make MAFFT alignments

```bash
cd $path
mkdir busco_alignments
mv BUSCO*.fasta $path/busco_alignments
cd $path/busco_alignments

qsub $scripts/sub_mafft_alignment.sh 
```

## For closely related organisms (same species): identify genes with high nucleotide diversity and average number of pairwise differences, medium number of segregating sites
## (avoid alignments with low homology and lots of phylogenetically uninformative singletons).
#For analyses involving cross-species comparisons involving highly diverged sequences with high nucleotide diversity  
# (e.g. 0.1<Pi<0.4), looking for genes with the lowest number of segregating sites.

python $scripts/calculate_nucleotide_diversity.py "*aligned.fasta"

mkdir -p $path/beast_runs/results
mv sequence_stats.txt excel_stats.txt $path/beast_runs/results

## Copy FASTA files of the candidate genes for the phylogeny into
mkdir -p $path/beast_runs/candidates

## Visually inspect the alignments of select genes (genes_selected_for_phylogeny.txt) to be used in
## constructing the phylogenies and trim them as necessary in MEGA7.
## Copy the 20 relevant trimmed alignment FASTA files into
mkdir -p $path/beast_runs/candidates/trimmed

##PartitionFinder (nucleotide sequence evolution model)

config_template=/home/sobczm/bin/PartitionFinder1.1.1/partition_finder.cfg
ct=$(basename "$config_template")

cd $path/beast_runs/candidates/trimmed
mkdir NEXUS

# prepare directory for PartitionFinder run:
for f in *.fa*
do
dos2unix $f
c="$(cat $f | awk 'NR%2==0' | awk '{print length($1)}' | head -1)"
p="${f%.fa*}.phy"
n="${f%.fa*}.NEXUS"
dir="${f%.fa*}"

mkdir $dir
cp $config_template $dir

# Substitute the name of the alignment file and the sequence length in the config file to become correct for the current run.
sed -i 's,^\(alignment = \).*,\1'"$p;"',' $dir/$ct
sed -i 's,^\(Gene1_pos1 = \).*,\1'"1-$c\\\3;"',' $dir/$ct
sed -i 's,^\(Gene1_pos2 = \).*,\1'"2-$c\\\3;"',' $dir/$ct
sed -i 's,^\(Gene1_pos3 = \).*,\1'"3-$c\\\3;"',' $dir/$ct

# Convert FASTA to phylip for the Partition Finder run
perl $scripts/fasta2phylip.pl $f>$p
mv $p $dir

# Convert FASTA to NEXUS for the BEAST run
perl $scripts/Fasta2Nexus.pl $f>$n
mv $n NEXUS

qsub $scripts/sub_partition_finder.sh $dir

done
