import re
import sys

#creates a gene contact matrix, if a gene is present accross several Hi-C bins the superior contact value is chosen
#python findGeneContacts.py path_to_bed_file path_to_matrix_file path_to_gene_location_file path_to_output_gen_matrix path_to_ listing_of_overlapping_genes

def getContigPositionFromBin():
	dictBins={}
	with open(str(sys.argv[1])) as bins:
	#with open('/home/eallery/GRAAL100/Result_HICPRO_GRAAL100/hic_results/matrix/reads/raw/20000/reads_20000_abs.bed') as bins:
		for line in bins:
			contents_bed=line.split('\t')
			dictBins[str(contents_bed[3].strip('\n'))]=[contents_bed[0],int(contents_bed[1]),int(contents_bed[2])]
	return dictBins


def getGenePositions():
	dictio={}
	with open(str(sys.argv[3])) as genes:
		for line in genes:
			contents=line.split('\t')
			dictio[contents[0]]={'contig':contents[1],'start':int(contents[2]),'end':int(contents[3].strip('\n'))}
	return dictio


def allocateGenestoBins(dictGenes,dictBins):
	tab=[]
	dictGenesBins={}
	for gene in dictGenes.keys():
		for i in dictBins.keys():
			if not str(i) in dictGenesBins.keys():
				dictGenesBins[str(i)]=[]
			if dictBins[str(i)][0]==dictGenes[gene]['contig']:
				if dictGenes[gene]['start']>dictBins[i][1] and dictGenes[gene]['start']<dictBins[i][2] and dictGenes[gene]['end']>dictBins[i][1] and dictGenes[gene]['end']<dictBins[i][2]:
					dictGenesBins[str(i)].append(gene)
				elif (dictGenes[gene]['start']>dictBins[i][1] and dictGenes[gene]['start']<dictBins[i][2]) and not (dictGenes[gene]['end']>dictBins[i][1] and dictGenes[gene]['end']<dictBins[i][2]):
					dictGenesBins[str(i)].append(gene)
					if not gene in tab:
						tab.append(gene)
				elif (not (dictGenes[gene]['start']>dictBins[i][1] and dictGenes[gene]['start']<dictBins[i][2])) and  (dictGenes[gene]['end']>dictBins[i][1] and dictGenes[gene]['end']<dictBins[i][2]):
					dictGenesBins[str(i)].append(gene)
					if not gene in tab:
						tab.append(gene)
				elif dictBins[i][1]>dictGenes[gene]['start'] and dictBins[i][2]<dictGenes[gene]['end']:
					print gene
					print dictGenes[gene]
	return tab,dictGenesBins


def buildGeneContactMatrix(argv, dictGenesBins):
	genePairs={}
	tab2=[]
	with open(str(argv[2])) as matrix:
	#with open('/home/eallery/GRAAL100/Result_HICPRO_GRAAL100/hic_results/matrix/reads/iced/20000/reads_20000_iced.matrix') as matrix:
		for line in matrix:
			contents=line.split('\t')
			for geneA in dictGenesBins[contents[0]]:
				if not geneA in genePairs.keys():
					genePairs[geneA]={}
				for geneB in dictGenesBins[contents[1]]:
					if geneA==geneB:
						continue
					else:
						if not geneA in tab2:
							tab2.append(geneA)
						if not geneB in tab2:
							tab2.append(geneB)
						if geneB not in genePairs[geneA].keys():
							genePairs[geneA][geneB]=float(contents[2])
						else:
							if float(contents[2])>genePairs[geneA][geneB]:
								genePairs[geneA][geneB]=float(contents[2])
	return tab2,genePairs


def writeGeneContactMatrix(genePairs,argv):
	output=open(str(argv[4]),"w")
	for geneA in genePairs.keys():
		for geneB in genePairs[geneA].keys():
			output.write(geneA + '\t' + geneB + '\t' + str(genePairs[geneA][geneB])+'\n')
	output.close()

#output=open('/home/eallery/Desktop/fl1Genes/HICMap/HicPro/geneModelsContacts.matrix','w')

output2=open(str(sys.argv[5]),"w")

dictGenes=getGenePositions()
dictBins=getContigPositionFromBin()
tab,dictGenesBins=allocateGenestoBins(dictGenes,dictBins)
print len(tab)
for i in tab:
	output2.write(i+'\n')
output2.close()
tab2,genePairs=buildGeneContactMatrix(sys.argv,dictGenesBins)		
print len(tab2)
writeGeneContactMatrix(genePairs,sys.argv)

