library(bnlearn)
library(dplyr)

df<-read.table("2020_bn_nb_data.txt",head=TRUE)
N<-nrow(df)

DF<-df
df<-lapply(DF,as.factor)
df<-data.frame(df)


bayes_bn31<-hc(df,score = "k2")
bayes_bn31.net<-bn.fit(bayes_bn31,df)
plot(bayes_bn31)
bayes_bn31.net
bayes_bn31

bayes_bn32<-hc(df,score = "bic")
bayes_bn32.net<-bn.fit(bayes_bn32,df)
plot(bayes_bn32)
bayes_bn32.net
bayes_bn32



#q3
course.grades<-read.table("2020_bn_nb_data.txt",head=TRUE)
N<-nrow(course.grades)
subset(course.grades,EC100=="DD" & IT101=="CC" & MA101=="CD")

