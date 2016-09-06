import re
import sys

#extract gene position on a genome from a blast output
#Blast output format: 6 qseqid sseqid pident qlen length qstart qend sstart send mismatch gapope evalue bitscore
#Only straight alignments ie complete and uninterrupted are reported
#python parseBlastforGenesNewPosition.py path_to_blast_output path_to_genes_new_location_output

def inversion_detection(contig,start,end,qlength,length,complete,complete_rev,gene):
	if length==qlength and start>end:
		complete_rev=True
	elif length==qlength and start<end:
		complete=True
	return complete,complete_rev

gene=""
contig=""
pident=0
length=0
count=0
complete_rev=False
complete=False
tab_pb_genes=[]
pb_gene=""
output=open(sys.argv[2],'w')

with open(str(sys.argv[1])) as blast_file:
	for line in blast_file:
		contents=line.strip('\n').split('\t')
		if contents[0]!=gene and len(gene)>0:
			if complete==True or complete_rev==True:
				output.write(gene+'\t'+new_contig+'\t'+str(start)+'\t'+str(end)+'\n')
			pident=0
			length=0
			qlength=0
			complete=False
			complete_rev=False
		gene=contents[0]
		contig=contents[1]
		if float(contents[2])>=pident and int(contents[4])>=length:
			pident=float(contents[2])
			length=int(contents[4])
			qlength=int(contents[3])
			new_contig=contig
			start=int(contents[7])
			end=int(contents[8])
		if contig!=new_contig and float(contents[2])>85.0 and (float(contents[4])>0.7*float(contents[3]) or float(contents[4])>=0.9*length):
			if gene!=pb_gene:
				pb_gene=gene
				count+=1
				tab_pb_genes.append(pb_gene)
		if contig==new_contig and (complete!=True and complete_rev!=True):
			big_rev,small,complete,complete_rev=inversion_detection(contig,int(contents[7]),int(contents[8]),qlength,length,complete,complete_rev,gene)
output.close()
print count
