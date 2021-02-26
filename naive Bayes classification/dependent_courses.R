library(bnclassify)
library(dplyr)
library(bnlearn)


studata<-read.table("2020_bn_nb_data.txt",head=TRUE) #read data
colnames(studata) #col. names

DF<-studata
studata<-lapply(DF,as.factor)
studata<-data.frame(studata)
colnames(studata)
#plot(nb.student)

nb.student<-nb(class = "QP",dataset = studata[,-5])
plot(nb.grades)


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

pred<-predict(student_nb,test[,-5]) # predict test data
str(pred)

confusionMatrix(table(predicted=pred,true=test$QP))

