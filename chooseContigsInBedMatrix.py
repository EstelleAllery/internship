import sys
import re

#select specific contigs in bed file and matrix file.
# python chooseContigsInBedMatrix.py path_to_matrix path_to_bed <contigs separated by spaces>

matrix_file=open(str(sys.argv[2]), "r")
output_bed=open(str(sys.argv[3])+".bed","w")
output_matrix=open(str(sys.argv[3])+".matrix","w")
contigs=sys.argv[4:]
bins={}

bin=0
for line in bed_file.readlines():
	for contig in contigs:
		contents=line.split('\t')
		if (re.search(contig,contents[0])):
			bin+=1
			output_bed.write(contents[0]+'\t'+contents[1]+'\t'+contents[2]+'\t'+str(bin)+'\n')
			if not contents[3] in bins.keys():
				bins[contents[3].strip('\n')]=bin

for line in matrix_file.readlines():
	contents=line.split('\t')
	if contents[0] in bins.keys() and contents[1] in bins.keys():
		output_matrix.write(str(bins[contents[0]])+'\t'+str(bins[contents[1]])+'\t')
		output_matrix.write(contents[2])

bed_file.close()
matrix_file.close()
output_bed.close()
output_matrix.close()

