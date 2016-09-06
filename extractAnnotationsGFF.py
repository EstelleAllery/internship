import re
import sys

#extract annotations of genes from a GFF file
#python extractAnnotationdGFF.py path_to_gff path_to_output

output=open(sys.argv[2],"w")

contig=""
annotation=""
geneModel=""
contigs=[]

with open(sys.argv[1],"r") as annotationFile:
	for line in annotationFile:
		if re.search("^contig",line):
			contents=line.split("\t")
			if re.search("gene",contents[2]):
				contig=contents[0]
				annotations=contents[8].split(";")
				geneModel=annotations[0].split("=")
				annotation=annotations[2].split("=")
				output.write(geneModel[1]+".mRNA-1")
				output.write("\t")
				output.write(contig)
				output.write("\t")
				output.write(annotation[1])
				output.write("\n")
				if not contig in contigs:
					contigs.append(contig)

print len(contigs)
output.close()