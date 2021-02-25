

studata<-read.table("2020_bn_nb_data.txt",head=TRUE) #read data
colnames(studata) #col. names

#label
table(studata$QP)# print QP table 

#split Train and Test
set.seed(20) # random no
id<-sample(2,nrow(studata),prob = c(0.7,0.3),replace = TRUE) # 70% train and test 
train<-studata[id==1,]#train data
test<-studata[id==2,]#test data

nrow(train)
nrow(test)

#naive bayes

library(e1071)
library(caret)
library(rminer)

student_nb<-naiveBayes(QP ~ ., data=train)# Applying naviebayes
student_nb

pred<-studata.predict(student_nb,test) # predict test data
mmetric(test$QP,pred,c("ACC","PRECISION","TPR","F1")) # accuracy

