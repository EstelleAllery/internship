import re
import sys

#attribute fragment length and GC content of a restriction fragment from Hi-C to the corresponding bin
#python findCorrespondingBins.py path_to_input path_to_output path_to_bed_file bin_size

out=open(sys.argv[2],'w')

with open(sys.argv[1]) as features:
	for line in features:
		contents=line.split('\t')
		contig=contents[0]
		tmpBin=contents[1]
		start=int(sys.argv[4])*(int(tmpBin)-1)
		bedFile=open(sys.argv[3],'r')
		for i in bedFile.readlines():
			if re.search(contig,i):
				contentBed=i.split('\t')
				if re.search(str(start),contentBed[1]):
					newBin=contentBed[3].strip('\n')
					out.write(contig+'\t'+newBin+'\t'+str(contents[2])+'\t'+str(contents[3]))
					bedFile.close()
					break

out.close()
