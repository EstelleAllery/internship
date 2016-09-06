from Bio import SeqIO
import re
import sys

#extracts gene location fromGenBank file
#python extractGeneLocationGB.py path_to_genbank_file path_to_output_file

loc_genes=open(str(sys.argv[2])+'.txt',"w")

records=SeqIO.to_dict(SeqIO.parse(str(sys.argv[1]),"gb"))


for key in records.keys():
   exons={}
   for feature in records[key].features:
      if feature.type=='gene':
         if 'ID' in feature.qualifiers.keys():
            gene=feature.qualifiers['ID']
            if not gene[0] in exons.keys():
               exons[gene[0]]={}
            if re.search('complement\(',str(feature.location)):
               print 'complement'
               location=str(feature.location).strip('complement(').split(')')
            else:
               location=str(feature.location).strip('[').split(']')
            positions=location[0].split(':')
            if int(positions[0])<int(positions[1]):
               exons[gene[0]]['starts']=int(positions[0])
               exons[gene[0]]['ends']=int(positions[1])
            else:
               print positions
               exons[gene[0]]['starts']=int(positions[1])
               exons[gene[0]]['ends']=int(positions[0])
         #elif 'label' in feature.qualifiers.keys():
            #print feature
				#loc_genes.write('>'+feature.qualifiers['label'][0]+'\n')
         else:
            continue
   for i in exons.keys():
      loc_genes.write(i+'\t'+ str(records[key].description.strip('.'))+'\t')
      starts=exons[i]['starts']
      ends=exons[i]['ends']
      loc_genes.write(str(starts)+'\t'+str(ends)+'\n')

loc_genes.close()