# Further analysis of linkage disequilibrium using the LDhat suite

Caveat - the model for recombination hotspots is based on human data

## Installation and profile modifications

Not required for other users

```bash
cd  /home/adamst/prog
git clone https://github.com/auton1/LDhat.git

cd LDhat
make
make clean
```

A manual is included for usage of LDhat:

```bash
/home/adamst/prog/LDhat/manual.pdf
```

In order to use LDhat, add the following line to your profile
Prepending is necessary as convert is also the name of a part of core unix

```bash
PATH=/home/adamst/prog/LDhat:${PATH}
```

## Convert vcf file to correct format for LDhat

Requires a phased vcf (see Pf_linkage_disequilibrium.md) for diploids
Haploids do not require phasing
Treat each contig as a separate "chromosome"

```bash
input=LDhat/UK123
mkdir -p $input
cd $input

vcftools=/home/sobczm/bin/vcftools/bin
input_vcf=../../summary_stats/polished_contigs_unmasked_UK123_filtered.recode_haplo.vcf
Out_prefix=polished_contigs_unmasked_UK123_haplo

contigs=$(cat $input_vcf | grep -v "#" | cut -f1 | cut -f2 -d "_" | sort -n | uniq)
for num in $(echo $contigs)
do
    contig_name=$(echo contig_"$num")
    Out_prefix=$(echo ldhat_"$contig_name")
    mkdir -p $contig_name
    $vcftools/vcftools --vcf $input_vcf --out $Out_prefix --chr $contig_name --phased --ldhat
    mv ldhat_"$contig_name".log $contig_name/.
    mv ldhat_"$contig_name".ldhat.locs $contig_name/.
    mv ldhat_"$contig_name".ldhat.sites $contig_name/.
done
```

## Use pairwise to build a lookup table and calculate some statistics

The following commands must be run in a screen session running a qlogin job
Requires some user input on the command line

My recommendations:

```
Unless another source of evidence available, use the suggested value of theta
Minor changes in theta do not seem to have an effect
4Ner should range between 20 - 100
No. of points on grid should range between 21 - 201
Larger values of 4Ner & No. of points take longer, but are more accurate

After generation of the table, use default grid value for recombination rate
If estimates at extreme of grid, change the defaults - can exceed above limits

Ignore sliding window analyses - interval is better

Use option 2 for rmin to write output to a file not just screen

Allow estimation of 4Ner by moment method

Test for recombination
```

The main thing needed from pairwise is the lookup table
The rest are mostly improved upon by interval & rhomap

```bash
for input_dir in $(ls -d contig_*)
do
    cd $input_dir
    seq_file=*.ldhat.sites
    loc_file=*.ldhat.locs
    pairwise -seq $seq_file -loc $loc_file
    cd ../
done
```

Manually copy and paste all output written to screen to a log.txt file

## Use complete to refine the lookup table

Use the same 4Ner_max, no of points and theta as in pairwise, stored in log file
Done separately for each contig

```bash
for input_dir in $(ls -d contig_*)
do
    n=$(cat $input_dir/ldhat_contig_*.ldhat.sites | grep '>' | wc -l)
    four_Ner_max=$(cat $input_dir/log.txt | grep -e 'Max 4Ner for grid (suggest 100):' | cut -f2 -d ':')
    no_points=$(cat $input_dir/log.txt | grep -e 'Number of points on grid (suggest 101, min=2):' | cut -f2 -d ':')
    theta=$(cat $input_dir/log.txt | grep -e 'Input theta per site (suggest Watterson estimate of ' | cut -f2 -d ':')
    ProgDir=/home/adamst/git_repos/scripts/phytophthora_fragariae/popgen_analysis
    Jobs=$(qstat | grep 'sub_comple' | grep 'qw' | wc -l)
    while [ $Jobs -gt 1 ]
    do
        sleep 1m
        printf "."
        Jobs=$(qstat | grep 'sub_comple' | grep 'qw' | wc -l)
    done
    printf "\n"
    qsub $ProgDir/sub_complete.sh $input_dir $n $four_Ner_max $no_points $theta
done
```

## Run interval to estimate the recombination rate

This only uses the crossing over model with a bayesian rjMCMC approach

```bash
for input_dir in $(ls -d contig_*)
do
    mv $input_dir/new_lk.txt $input_dir/exhaustive_lk.txt
    sequence_data=ldhat_"$input_dir".ldhat.sites
    location_data=ldhat_"$input_dir".ldhat.locs
    lookup_table=exhaustive_lk.txt
    #10,000,000 is the recommended number of iterations in the manual
    iterations=10000000
    # Sample rate keeps every xth result of the markov chain
    sample_rate=2000
    # Values from 0 - 50 are recommended, 5 is okay for humans
    # If you have data on expected recombination rate
    # run simulations with different penalities to test which is least 'noisy'
    block_penalty=5
    ProgDir=/home/adamst/git_repos/scripts/phytophthora_fragariae/popgen_analysis
    Jobs=$(qstat | grep 'sub_interv' | grep 'qw' | wc -l)
    while [ $Jobs -gt 1 ]
    do
        sleep 1m
        printf "."
        Jobs=$(qstat | grep 'sub_interv' | grep 'qw' | wc -l)
    done
    printf "\n"
    qsub $ProgDir/sub_interval.sh $input_dir $sequence_data $location_data $lookup_table $iterations $block_penalty $sample_rate
done
```

### Visualise output of interval using stat

Average values are stored in the output log files from sge
Ensure all the jobs in one loop are finished before starting the other
They both produce output files of the same name initially due to source code

```bash
for input_dir in $(ls -d contig_*)
do
    cd $input_dir
    rates_file=rates.txt
    # Specify number of iterations to discard
    # 100,000 iterations is recommended min
    # So divide 100,000 by sampling rate for burn-in value
    burn_in=50
    location_file=ldhat_"$input_dir".ldhat.locs
    ProgDir=/home/adamst/git_repos/scripts/phytophthora_fragariae/popgen_analysis
    Jobs=$(qstat | grep 'sub_stat' | grep 'qw' | wc -l)
    while [ $Jobs -gt 1 ]
    do
        sleep 1m
        printf "."
        Jobs=$(qstat | grep 'sub_stat' | grep 'qw' | wc -l)
    done
    qsub $ProgDir/sub_stat_rates.sh $rates_file $burn_in $location_file
    cd ../
done

for input_dir in $(ls -d contig_*)
do
    cd $input_dir
    bounds_file=bounds.txt
    # Specify number of iterations to discard
    # 100,000 iterations is recommended min
    # So divide 100,000 by sampling rate for burn-in value
    burn_in=50
    location_file=ldhat_"$input_dir".ldhat.locs
    ProgDir=/home/adamst/git_repos/scripts/phytophthora_fragariae/popgen_analysis
    Jobs=$(qstat | grep 'sub_stat' | grep 'qw' | wc -l)
    while [ $Jobs -gt 1 ]
    do
        sleep 1m
        printf "."
        Jobs=$(qstat | grep 'sub_stat' | grep 'qw' | wc -l)
    done
    qsub $ProgDir/sub_stat_bounds.sh $bounds_file $burn_in $location_file
    cd ../
done
```
