gene <- as.character(geneContents[match(rownames(ReadCounts_20Jan16_RPKM_WThepA_CulturePlanta), geneContents[, 1]),1])
geneExp <- apply(ReadCounts_20Jan16_RPKM_WThepA_CulturePlanta, 2, function(X) {
  ave(X, gene, FUN = median)
})
geneExp <- data.frame(gene, geneExp)
geneExp <- unique(geneExp)

ganno <- apply(geneContents[, 2:19], 2, function(X) {
  ave(X, geneContents[, 1], FUN = median)
})
ganno <- data.frame(geneContents[, 1], ganno)
ganno <- unique(ganno)
rownames(ganno) <- ganno[, 1]
ganno <- ganno[, -1]
nullGeneExp<-geneExp[apply(geneExp[, -1], 1, sum) <= 0, ]
nullGeneExp<-nullGeneExp[,-1]
geneExp <- geneExp[apply(geneExp[, -1], 1, sum) > 0, ]

biasanno<-ganno
Exp<-geneExp
rownames(Exp) <- geneExp[, 1]
Exp=Exp[,-1]
grpnn=200

bias <- biasanno[rownames(Exp), ]
bias[, 1] <- log(bias[, 1])
colnames(bias)[1] <- "Log_L"
trend_bias <- gamcrt <- list()
for (i in 1:8) {
  zeroid <- which(Exp[, i] == 0)
  trend_bias[[i]] <- group_plot(cbind(log(Exp[-zeroid, i]), bias[-zeroid, ]), grpn = grpnn)
  gamcrt[[i]] <- gampc(log(Exp[-zeroid, i]), bias[-zeroid, 1], bias[-zeroid, 2:18])
  trend_bias[[i + 8]] <- group_plot(cbind(gamcrt[[i]], bias[-zeroid, ]), grpn = grpnn)
}

