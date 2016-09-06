import sys
import re

"""Run with Pypy for resonnable computation time"""
#python prepCorrelations.py path_to_gene_contact_matrix path_to_expression_file path_to_outputs
#outputs: matrix: containing contacts and difference in expression for each pair of genes
		# unusedGenesFromExpression: genes in expression file but absent from contact matrix
		# genesWithoutExpression: genes present in contact matrix but not in expression file
		
def extractGeneContacts(argv):
	
	Contacts=open(sys.argv[1],"r")
	genes={}
	for line in Contacts.readlines():
		contents= line.split('\t')
		if not contents[0] in genes.keys():
			genes[contents[0]]={'exp':[], 'paired_genes':[],'contacts':[]}
			genes[contents[0]]['paired_genes'].append(contents[1])
			genes[contents[0]]['contacts'].append(contents[2])
		else:
			genes[contents[0]]['paired_genes'].append(contents[1])
			genes[contents[0]]['contacts'].append(contents[2].strip('\n'))
		if not contents[1] in genes.keys():
			genes[contents[1]]={'exp':[], 'paired_genes':[],'contacts':[]}
	Contacts.close()
	print ('contacts done')
	return genes

def linkExptoContacts(argv,genes):
	unused_exp=[]
	output2=open(sys.argv[3]+'unusedGenesFromExpression.txt',"w")
	with open(sys.argv[2]) as Expressions:
		for line in Expressions:
			contents=line.split('\t')
			if contents[0] in genes.keys():
				genes[contents[0]]['exp'].append(float(contents[1]))
			else:
				if not contents[0] in unused_exp:
					unused_exp.append(contents[0])
	for i in unused_exp:
		output2.write(i+'\n')


	output2.close()
	print 'expressions done'
	return genes

def writeGeneMatrixAndMissingGenes(argv):
	genes1=extractGeneContacts(argv)
	genes=linkExptoContacts(argv,genes1)
	output=open(sys.argv[3]+'matrix.csv',"w")
	output3=open(sys.argv[3]+'genesWithoutExpression.txt',"w")
	noexp=[]
	for gene in genes.keys():
		for i in range(len(genes[gene]['paired_genes'])):
			gene2=genes[gene]['paired_genes'][i]
			if len(genes[gene]['exp'])==0 and not gene in noexp:
				noexp.append(gene)
			if len(genes[gene2]['exp'])==0 and not gene2 in noexp:
				noexp.append(gene2)
			for j in genes[gene]['exp']:
				for k in genes[gene2]['exp']:
					output.write(gene+'\t'+gene2+'\t'+genes[gene]['contacts'][i]+'\t'+str(abs(j-k))+'\n')

	for i in noexp:
		output3.write(i+'\n')

	output.close()
	output3.close()

writeGeneMatrixAndMissingGenes(sys.argv)
