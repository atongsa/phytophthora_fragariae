#Maria carried out an RBB, I have narrowed down to eight candidates. The presence of these needs to be confirmed in the other race 2 isolate, A4 with the same method.

##Set inital variables

```bash
scripts=/home/sobczm/bin/popgen/other
input=/home/groups/harrisonlab/project_files/phytophthora_fragariae/BLAST/UK2_check
mkdir -p $input
```

##Set up directory with required fasta files

###Copy relevant assemblies

Target header list created manually as Bc16_targets.txt

```bash
#A4 genome
cp gene_pred/annotation/P.fragariae/A4/A4_genes_incl_ORFeffectors.gene.fasta $input

#Bc16 genome
cp gene_pred/annotation/P.fragariae/Bc16/Bc16_genes_incl_ORFeffectors.gene.fasta $input
```

##Make nucleotide BLAST db of all genomes.

```bash
cd $input
for assembly in *.fasta
do
    makeblastdb -in $assembly -input_type fasta -dbtype nucl -title "${assembly%.*}"_nucl.db -parse_seqids -out "${assembly%.*}"_nucl.db
done
```

##Run BLAST of A4 gene set against BC16

```bash
db=Bc16_genes_incl_ORFeffectors.gene_nucl.db
for query in A4_genes_incl_ORFeffectors.gene.fasta
do
    blastn -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen sstrand"  -num_threads 1 -max_target_seqs 100 -evalue 0.0000000001 -query $query -db $db >> ${query}_vs_${db}
done
```

##And vice versa

```bash
query=Bc16_genes_incl_ORFeffectors.gene.fasta
for db in A4_genes_incl_ORFeffectors.gene_nucl.db
do
    blastn -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen sstrand"  -num_threads 1 -max_target_seqs 100 -evalue 0.0000000001 -query $query -db $db >> ${query}_vs_${db}
done
```

##Identify RBB matches

```bash
for Strain in A4
do
    python $scripts/rbb.py Bc16_genes_incl_ORFeffectors.gene.fasta_vs_${Strain}_genes_incl_ORFeffectors.gene_nucl.db ${Strain}_genes_incl_ORFeffectors.gene.fasta_vs_Bc16_genes_incl_ORFeffectors.gene_nucl.db >Bc16_vs_${Strain}.tophits
done
```

##Fish out only RLXLR RBB hits

```bash
my_list=""
for Strain in A4
do
    my_list+=" Bc16_vs_${Strain}.tophits"
done
```

##Analyse RBB matches.

```bash
python $scripts/analyse_rbb.py Bc16_targets.txt $my_list
```
