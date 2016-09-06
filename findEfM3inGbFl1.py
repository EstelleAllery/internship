from Bio import SeqIO
import re
import sys

#find EfM3 correspondences in Fl1 GenBank file
#python findEfM3inGBFl1.py path_to_GenBank_file path_to_output_csv

def extractCorrespondenceFromGenBank(argv):
	dictio={}
	records=SeqIO.to_dict(SeqIO.parse(str(sys.argv[1]),"gb"))
	for key in records.keys():
		for feature in records[key].features:
			gene=''
			efm=''
			if feature.type=='gene':
				if 'ID' in feature.qualifiers.keys():
					gene=feature.qualifiers['ID']
					if 'm3source' in feature.qualifiers.keys():
						efm=feature.qualifiers['m3source']
					if not gene[0] in dictio.keys():
						dictio[gene[0]]=efm
					else:
						print gene[0]
	return dictio

def writeCorrespondenceFile(argv):
	dictio=extractCorrespondenceFromGenBank(argv)
	out=open(sys.argv[2],'w')
	for fl1 in dictio.keys():
		efm=str(dictio[fl1]).split(',')
		if len(efm)==1 and re.search('EfM3',efm[0]) and re.search('mRNA-1',efm[0]):
			out.write(dictio[fl1][0].strip('.mRNA-1')+'\t'+fl1+'\n')
		else:
			for i in efm:
				if re.search(' ',i) and re.search("mRNA-1",i):
					gene=i.split(' ')
					out.write(gene[0].strip("[']")+gene[1].strip("[']").strip(".mRNA-1")+'\t'+fl1+'\n')
				elif re.search('mRNA-1',i):
					out.write(i.strip("[']").strip('.mRNA-1')+'\t'+fl1+'\n')

	out.close()

writeCorrespondenceFile(sys.argv)