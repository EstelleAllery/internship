from Bio import SeqIO
import re
import sys

#extracts gene sequences from a GenBank file with extension of given size on both extremities of the gene
#python extractGenesFromGenBank.py path_to_GenBank_file path_to_fasta_output(withoutfiletype) size_of_extension_in_bases

fasta_FL1_genes=open(str(sys.argv[2])+str(sys.argv[3])+'.fasta',"w")
#fasta_FL1_genes=open("/home/eallery/Desktop/FL1_extendedGenes.fasta","w")

records=SeqIO.to_dict(SeqIO.parse(str(sys.argv[1]),"gb"))
#records=SeqIO.to_dict(SeqIO.parse("/home/eallery/Desktop/FL1.2.gb","gb"))

extension=int(sys.argv[3])

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
				#fasta_FL1_genes.write('>'+feature.qualifiers['label'][0]+'\n')
         else:
            continue
   for i in exons.keys():
      fasta_FL1_genes.write('>'+i+' '+ str(records[key].description.strip('.'))+' ')
      starts=exons[i]['starts']-extension
      ends=exons[i]['ends']+extension
      fasta_FL1_genes.write(str(starts)+' '+str(ends)+'\n')
      seq=""
      seq+=records[key].seq[starts:ends]
      if len(seq)<15:
         print i
         print exons[i]
      fasta_FL1_genes.write(str(seq)+'\n')

fasta_FL1_genes.close()
