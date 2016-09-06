cluster166=list()
j=1
for (i in 1:8312){
  if (pam$clustering[i]==166){
  cluster166[[j]]=attr(pam$clustering[i],"names")
  j=j+1
  }}

for (i in 1:length(cluster88)){
  cluster88[[i]]=sub(pattern='.mRNA-1',replacement='',x=cluster88[[i]])
}

listEasLtm=list()
j=1
for (i in 1:length(cluster76)){
  for (k in 1:dim(corresp2)[1]){
    if (cluster76[[i]]==corresp2[k,1]){
      listEasLtm[[j]]=corresp2[k,2]
      j=j+1
    }
  }
}

contactANDexpressionsALL[,1]=factor(contactANDexpressionsALL[,1], levels=levels(listEasLtm[[1]]))
contactANDexpressionsALL[,2]=factor(contactANDexpressionsALL[,2], levels=levels(listEasLtm[[1]]))
subsetlistEasLtm=subset(contactANDexpressionsALL,contactANDexpressionsALL[,1]==listEasLtm[[1]])
for (i in 2:length(listEasLtm)){
  subsetlistEasLtm=rbind(subsetlistEasLtm,subset(contactANDexpressionsALL,contactANDexpressionsALL[,1]==listEasLtm[[i]]))
}
subsetlistEasLtmp=subset(contactANDexpressionsALL,contactANDexpressionsALL[,2]==listEasLtm[[1]])
for (i in 2:length(listEasLtm)){
  subsetlistEasLtmp=rbind(subsetlistEasLtmp,subset(contactANDexpressionsALL,contactANDexpressionsALL[,2]==listEasLtm[[i]]))
}
subsetlistEasLtm=rbind(subsetlistEasLtm,subsetlistEasLtmp)

subsetlistEasLtmonly=subset(subsetlistEasLtmp,subsetlistEasLtmp[,1]==listEasLtm[[1]])
for (i in 2:length(listEasLtm)){
  subsetlistEasLtmonly=rbind(subsetlistEasLtmonly,subset(subsetlistEasLtmp,subsetlistEasLtmp[,1]==listEasLtm[[i]]))
}

