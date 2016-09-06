d2=dist(t(expNorm),method="euclidean")
h=hclust(d2,method="single")
plot(h)

#Resampling
for (i in 1:18){
  tnormalized=as.data.frame(t(expNorm[sample(1:nrow(expNorm),size=500,replace=TRUE),]))
  d2=dist(tnormalized,method="euclidean")
  h=hclust(d2,method="single")
  plot(h)  
}

pam_test=pam(test,20,metric="euclidean")

