# Statistical analysis and graphing of qRT-PCR data from an infection timecourse

Run on Mac rather than cluster

Each gene analysed is on a separate csv file

## Candidate _Avr_ (g24882.t1)

```R
# Read in csv file
input <- read.csv("/Users/adamst/Documents/qPCR/Statistical_Analysis/cAvr.csv")

# Generate frequency tables
table(input$Timepoint, input$Isolate)

# Perform ANOVA
res.avo2 <- avo(Expression ~ Timepoint * Isolate, data = input)
summary(res.avo2)

# Tukey multiple pairwise-comparisons
```
