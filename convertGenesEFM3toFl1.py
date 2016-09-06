import re
import sys

#Replaces gene labels in a csv file given a correspondence file consisting of two columns separated by tabulation
#python convertGeneslabels.py path_to_correspondence_file path_to_file_to_be_relabelled path_to_output

def readCorrespondenceFile (argv):
	tab=[]
	
	with open(argv[1]) as geneCorrespondences:
		for line in geneCorrespondences:
			contents=line.strip('\n').split('\t')
			if len(contents)<3:
				if re.search('pseudo',contents[0]):
					efm=contents[0].split('.pseudo')
				elif re.search('partial', contents[0]):
					efm=contents[0].split('.partial')
				else:
					efm=contents[0]
				fl1=contents[1]
				if not isinstance(efm, basestring) :
					tab.append([efm[0],fl1])
				else:
					tab.append([efm,fl1])
	return tab

def replaceGeneLabels(argv):
	tab=readCorrespondenceFile(argv)
	output=open(argv[3],"w")
	with open(argv[2]) as geneExpressions:
		for line in geneExpressions:
			contents=line.split('\t')
			for i in tab:
				if re.search(i[0],contents[0]):
					output.write(i[1])
					for j in range (1,len(contents)):
						output.write('\t'+contents[j])
					break

	output.close()

def countObtainedGeneModels(argv):
	tab=[]
	count=0
	with open(argv[1]) as geneCorrespondences:
		for line in geneCorrespondences:
			contents=line.strip('\n').split('\t')
			if len(contents)<3:
				if re.search('pseudo',contents[0]):
					efm=contents[0].split('.pseudo')
				elif re.search('partial', contents[0]):
					efm=contents[0].split('.partial')
				else:
					efm=contents[0]
				fl1=contents[1]
				if not fl1 in tab:
					tab.append(fl1)
				else:
					count+=1

	print ('Number of different genes '+len(tab))
	print ('Number of repeated genes '+count)
replaceGeneLabels(sys.argv)
countObtainedGeneModels(sys.argv)