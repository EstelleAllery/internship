import sys
import re

#Lists all common genes in two text or csv files, given that they are the first element of each line. Tabulation spacing

output=open(sys.argv[3],"w")
#exp_file=open(sys.argv[2],"r")


with open(sys.argv[1]) as coord_file:
	for line in coord_file:
		contents=line.split('\t')
		with open(sys.argv[2]) as exp_file:
			for line2 in exp_file:
				contents2=line2.split('\t')
				if re.search(contents[0],contents2[0]):
					output.write(contents[0]+'\n')
					break

output.close()
