#!/usr/bin/Rscript

# Plot a 3-way Venn diagram from a tab delimited file containing a matrix showing
# presence of DEGs between 3 timepoints post inoculation.

# This is intended to be used on the output of parse_RNA-Seq.py, after the creation of DEG lists by DeSeq

# The script also requires the colorspace package. This can be downloaded by
# opening R and running the following command:

#get config options
library("optparse")
library("colorspace")
library("VennDiagram")
opt_list <- list(
    make_option("--inp", type = "character",
    help = "tab seperated file containing matrix of DEGs"),
    make_option("--out", type = "character",
    help = "output venn diagram in pdf format")
)
opt <- parse_args(OptionParser(option_list = opt_list))
f <- opt$inp
o <- opt$out

DEGs <- data.frame()
DEGs <- read.table(f, header = TRUE)

TP1 <- subset(DEGs, DEGs[, "BC.16"] == 1 &
DEGs[, "BC.1"] == 0 & DEGs[, "NOV.9"] == 0)
TP2 <- subset(DEGs, DEGs[, "BC.16"] == 0 &
DEGs[, "BC.1"] == 1 & DEGs[, "NOV.9"] == 0)
TP3 <- subset(DEGs, DEGs[, "BC.16"] == 0 &
DEGs[, "BC.1"] == 0 & DEGs[, "NOV.9"] == 1)

# Set up labels
label1 <- paste("BC-16", sep = "" )
label2 <- paste("BC-1", sep = "" )
label3 <- paste("NOV-9", sep = "" )

n123 <- nrow(subset(DEGs, DEGs[, "BC.16"] == 1 &
DEGs[, "BC.1"] == 1 & DEGs[, "NOV.9"] == 1))
n12 <- n123 + nrow(subset(DEGs, DEGs[, "BC.16"] == 1 &
DEGs[, "BC.1"] == 1 & DEGs[, "NOV.9"] == 0))
n13 <- n123 + nrow(subset(DEGs, DEGs[, "BC.16"] == 1 &
DEGs[, "BC.1"] == 0 & DEGs[, "NOV.9"] == 1))
n23 <- n123 + nrow(subset(DEGs, DEGs[, "BC.16"] == 0 &
DEGs[, "BC.1"] == 1 & DEGs[, "NOV.9"] == 1))
summary(n12)
summary(n13)
summary(n23)
summary(n123)

area1 <- (nrow(TP1) + (n12 - n123) + (n13 - n123) + n123)
area2 <- (nrow(TP2) + (n12 - n123) + (n23 - n123) + n123)
area3 <- (nrow(TP3) + (n13 - n123) + (n23 - n123) + n123)
nrow(TP1)
nrow(TP2)
nrow(TP3)
n12
n13
n23
n123
area1
area2
area3

pdf(o)
draw.triple.venn(area1, area2, area3,
    n12, n23, n13,
    n123,
    category = c(label1, label2, label3),
#    rep("", 4),
    rotation = 1,
    reverse = FALSE,
    lwd = rep(2, 3),
    lty = rep("solid", 3),
    col = rep("black", 3),
    fill = c("forestgreen", "royalblue2", "khaki1"),
    alpha = rep(0.5, 3),
    label.col = rep("black", 7),
    cex = rep(2, 7),
    fontface = rep("plain", 7),
    fontfamily = rep("sans", 7),
    cat.pos = c(-40, 40, 180),
    cat.dist = c(0.05, 0.05, 0.025),
    cat.col = rep("black", 3),
    cat.cex = rep(2, 3),
    cat.fontface = rep("plain", 3),
    cat.fontfamily = rep("sans", 3),
    cat.just = list(c(0.5, 1), c(0.5, 1), c(0.5, 0)),
    cat.default.pos = "outer",
    cat.prompts = FALSE,
    rotation.degree = 0,
    rotation.centre = c(0.5, 0.5),
    ind = TRUE, sep.dist = 0.05, offset = 0,
    )

warnings()
q()
