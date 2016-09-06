import re
import numpy
import sys

#extract length and GC content of restriction fragments from Hi-C
#python findHiCFragmentsFeatures.py path_to_genome_fasta_file path_to_output enzyme_forward_strand_motif

out=open(sys.argv[2],'w')
seq={}

with open(sys.argv[1]) as file:
	for line in file:
		if re.search('>',line):
			header=line.strip('>').strip('\n')
		if not re.search('>',line):
			if header in seq.keys():
				seq[header]+=line
			else:
				seq[header]=line

for i in seq.keys():
	positions=[]
	length=[]
	tabGCC=[]
	for m in re.finditer('(?={0})'.format(re.escape(sys.argv[3])),seq[i],re.I):
		positions.append(m.start())
	for k in range(0,len(positions)):
		if k==0:
			length.append(positions[k])
			gcc1=len(re.findall("G",seq[i][0:200],re.I))+len(re.findall("C",seq[i][0:200],re.I))
			gcc2=len(re.findall("G",seq[i][positions[k]-200:positions[k]],re.I))+len(re.findall("C",seq[i][positions[k]-200:positions[k]],re.I))
			tabGCC.append((gcc1+gcc2)/400.0)
		elif k==len(positions)-1:
			length.append(len(seq[i])-positions[k])
			gcc1=len(re.findall("G",seq[i][positions[k]:positions[k]+200],re.I))+len(re.findall("C",seq[i][positions[k]:positions[k]+200],re.I))
			gcc2=len(re.findall("G",seq[i][len(seq[i])-200:],re.I))+len(re.findall("C",seq[i][len(seq[i])-200:],re.I))

			tabGCC.append((gcc1+gcc2)/400.0)
		else:
			length.append(positions[k+1]-positions[k])
			gcc1=len(re.findall("G",seq[i][positions[k]:positions[k]+200],re.I))+len(re.findall("C",seq[i][positions[k]:positions[k]+200],re.I))
			gcc2=len(re.findall("G",seq[i][positions[k+1]-200:positions[k+1]],re.I))+len(re.findall("C",seq[i][positions[k+1]-200:positions[k+1]],re.I))
			tabGCC.append((gcc1+gcc2)/400.0)
	bins=1
	if len(seq[i])>150000:
		for t in range(1,len(seq[i])/150000,1):
			start=(t-1)*150000
			end=t*150000
			indicesOk=[]
			for x in range(0,len(positions)):
				if positions[x]>=start and positions[x]<end:
					indicesOk.append(x)
			out.write(i +'\t'+str(bins)+'\t')
			sum1=0
			sum2=0
			gcc=0
			for x in indicesOk:
				if length[x]>1000:
					sum1+=1
				else:
					sum2+=length[x]
				gcc+=tabGCC[x]
			out.write(str(sum1*1000 + sum2) + '\t')
			out.write(str(gcc/len(indicesOk)))
			out.write('\n')
			bins+=1
	else:
		start=0
		end=150000
		indicesOk=[]
		for x in range(0,len(positions)):
			if positions[x]>=start and positions[x]<end:
				indicesOk.append(x)
		if len(indicesOk)!=0:
			out.write(i +'\t'+str(bins)+'\t')
			sum1=0
			sum2=0
			gcc=0
			for x in indicesOk:
				if length[x]>1000:
					sum1+=1
				else:
					sum2+=length[x]
				gcc+=tabGCC[x]
			out.write(str(sum1*1000 + sum2) + '\t')
			out.write(str(gcc/len(indicesOk)))
			out.write('\n')
out.close()
