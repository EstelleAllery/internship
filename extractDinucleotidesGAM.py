import re
import math
import sys

#extracts percentages of each dinucleotide of each gene given as input in a fasta file. Necessary for RNASeqBias normalization of RNASeq read counts
#Output written in a csv file
# python extractDinuleotidesGAM.py path_to_fasta_file path_to_output

def dinucleotidesCounting(i, fasta_seq):
	return len(re.findall('(?={0})'.format(re.escape(i)),fasta_seq,re.I))

def GCContentCounting(seq):
	return len(re.findall("G",seq,re.I))+len(re.findall("C",seq,re.I))

def dinucleotidesIterator(gene, dictDinucleotides, dinucleotides, fasta_seq):
   dictDinucleotides[gene]={}
   for i in dinucleotides:
      dictDinucleotides[gene][i]=dinucleotidesCounting(i, fasta_seq)

sequence=False
header=""
GCContent={}
length={}
dinucleotidesContent={}
dinucleotides=["AA","TT","CC","GG","AT","AC","AG","TA","TC","TG","CA","CT","CG","GA","GT","GC"]
fasta_seq=""
outputFile2=open(sys.argv[2],"w")
outputFile2.write("gene"+'\t'+"length"+'\t'+"G+C_Content"+'\t'+"AA"+'\t'+"TT"+'\t'+"CC"+'\t'+"GG"+'\t'+"AT"+'\t'+"AC"+'\t'+"AG"+'\t'+"TA"+'\t'+"TC"+'\t'+"TG"+'\t'+"CA"+'\t'+"CT"+'\t'+"CG"+'\t'+"GA"+'\t'+"GT"+'\t'+"GC"+'\n')

with open(sys.argv[1],"r") as fasta:
	for line in fasta:
		if re.search("^>",line):
			if re.search("mRNA-1",line) or re.search("ltm",line):
				sequence=True
				if len(fasta_seq)>1:
					dinucleotidesIterator(header[0].strip(">").strip("\n"), dinucleotidesContent, dinucleotides, fasta_seq)
				fasta_seq=""
				header=line.strip(">").strip("\n").split(" ")
			else:
				sequence=False
		elif sequence==True and not re.search("^>",line):
			if header[0] in GCContent.keys():
				GCContent[header[0]]+=GCContentCounting(line)
				length[header[0]]+=len(line.strip("\n"))
				fasta_seq+=line.strip("\n")
			else:
				GCContent[header[0]]=GCContentCounting(line)
				length[header[0]]=len(line.strip("\n"))
				fasta_seq=line.strip("\n")
	dinucleotidesIterator(header[0].strip(">").strip("\n"), dinucleotidesContent, dinucleotides, fasta_seq)
count=0
count2=0
count3=0
for key in GCContent.keys():
	if re.search('partial',key):
		count+=1
		print key
		gene=key.split('.partial')
		if not (gene[0]+'.mRNA-1') in GCContent.keys():
			outputFile2.write(gene[0]+".mRNA-1\t")
			outputFile2.write(str(length[key])+"\t")
			outputFile2.write(str(float(GCContent[key])/length[key])+"\t")
			for i in dinucleotides:
				outputFile2.write(str(float(dinucleotidesContent[key][i])/(length[key]-1))+"\t")
			outputFile2.write("\n")
		else:
			continue
	elif re.search('pseudo',key):
		count2+=1
		print key
		gene=key.split('.pseudo')
		if not (gene[0]+'.mRNA-1') in GCContent.keys():
			outputFile2.write(gene[0]+".mRNA-1\t")
			outputFile2.write(str(length[key])+"\t")
			outputFile2.write(str(float(GCContent[key])/length[key])+"\t")
			for i in dinucleotides:
				outputFile2.write(str(float(dinucleotidesContent[key][i])/(length[key]-1))+"\t")
			outputFile2.write("\n")
		else:
			continue
	else:
		count3+=1
		outputFile2.write(key+"\t")
		outputFile2.write(str(length[key])+"\t")
		outputFile2.write(str(float(GCContent[key])/length[key])+"\t")
		for i in dinucleotides:
			outputFile2.write(str(float(dinucleotidesContent[key][i])/(length[key]-1))+"\t")
		outputFile2.write("\n")

print count
print count2
print count3
outputFile2.close()


