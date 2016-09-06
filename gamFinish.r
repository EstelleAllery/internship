normalized=Exp
k1=1
k2=1
k3=1
k4=1
k5=1
k6=1
k7=1
k8=1
for (i in 1:8191){
  if (Exp[i,1]!=0.000){
    normalized[i,1]=gamcrt[[1]][k1,1]
    k1=k1+1
  }
  if (Exp[i,2]!=0.000){
    normalized[i,2]=gamcrt[[2]][k2,1]
    k2=k2+1
  }
  if (Exp[i,3]!=0.000){
    normalized[i,3]=gamcrt[[3]][k3,1]
    k3=k3+1
  }
  if (Exp[i,4]!=0.000){
    normalized[i,4]=gamcrt[[4]][k4,1]
    k4=k4+1
  }
  if (Exp[i,5]!=0.000){
    normalized[i,5]=gamcrt[[5]][k5,1]
    k5=k5+1
  }
  if (Exp[i,6]!=0.000){
    normalized[i,6]=gamcrt[[6]][k6,1]
    k6=k6+1
  }
  if (Exp[i,7]!=0.000){
    normalized[i,7]=gamcrt[[7]][k7,1]
    k7=k7+1
  }
  if (Exp[i,8]!=0.000){
    normalized[i,8]=gamcrt[[8]][k8,1]
    k8=k8+1
  }
}
normalized=rbind(normalized,nullGeneExp)
write.table(normalized,col.names=FALSE,sep="\t",file='gamNorm_expdata_fl1WThepA_CulturePlanta.csv')

