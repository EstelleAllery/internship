library("kohonen")
slopeData=read.table('foldChangesGeneModelsFl1.csv',sep="\t",header = TRUE)
slopeData2=data.matrix(slopeData)
somFl1<- som(data = slopeData2, grid = somgrid(15, 15, "hexagonal"))
save(somFl1,file='somFl1_225.rda')

somFl1_100 = som(data = slopeData2, rlen = 100, alpha = c(0.05, 0.01), grid = somgrid(10, 10, "hexagonal"))
save(somFl1_100,file='somFl1_100.rda')
