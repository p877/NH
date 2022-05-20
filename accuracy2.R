
require(dplyr)
require(ggplot2)
require(readxl)
require(openxlsx)

df2 <- read.csv("C:/Parisa/UVT/Martin Atzmueller/Dataset/NewHero/Py/github1/2/result/accuracy_precision_recall_fscore/accuracy.csv", sep = ";", header = TRUE)
df2
df<-data.frame(df2)

sd<-sd(df[201:210,4])
sd



df1 <- read.csv("C:/Parisa/UVT/Martin Atzmueller/Dataset/NewHero/Py/github1/2/result/accuracy_precision_recall_fscore/accuracy2.csv", sep = ";", header = TRUE)
df1


#summary(df1)
# 
# sd(df1[21,4:7])

#rowMeans(df1[4:7])   
# Day <- df1[1:20,3]
# majorityclass_baseline <- df1[1:20,8]
# accuracy <- df1[1:20,4]
# precision <- df1[1:20,5]
# recall <- df1[1:20,6]
# fscore <- df1[1:20,7]
# SD <- df1[1:20,9]
# M <- df1[1:20,10]
# Category<-df1[1:20,c(4:7)]
# Category

ggplot(df1, aes(x=Day)) +
  geom_line(aes(y = majorityclass_baseline, color="majorityclass_baseline")) +
  geom_line(aes(y = accuracy, color="accuracy")) +
  geom_ribbon(aes( ymin=accuracy-sda, ymax=accuracy+sda, fill="accuracy"),
              alpha=0.3)+
  geom_line(aes(y = precision, color="precision")) +
  geom_ribbon(aes( ymin=precision-sdp, ymax=precision+sdp, fill="precision" ),
                alpha=0.3)+
  geom_line(aes (y = recall, color="recall")) +
  geom_ribbon(aes( ymin=recall-sdr, ymax=recall+sdr, fill="recall" ),
                alpha=0.3)+
  geom_line(aes (y = fscore, color="fscore")) +
  geom_ribbon(aes( ymin=fscore-sdf, ymax=fscore+sdf, fill="fscore"),
                alpha=0.3)+
  
  #scale_color_manual(values = c( "steelblue",  "green", "black","red", "darkred")) +
  labs(y="Mean") +
  theme(legend.title=element_blank())







geom_errorbar(aes( ymin=recall-SD, ymax=recall+SD), width=.2, color="darkgray",
              position=position_dodge(0.05))+



df<-data.frame(Mean=c(0.24,0.25,0.37,0.643,0.54),
               sd=c(0.00362,0.281,0.3068,0.2432,0.322),
               Quality=as.factor(c("good","bad","good",
                                   "very good","very good")),
               Category=c("A","B","C","D","E"),
               Insert= c(0.0, 0.1, 0.3, 0.5, 1.0))



ggplot(df, aes(x=Category, y=Mean, fill=Quality)) +
  geom_bar(position=position_dodge(), stat="identity",
           colour='black') +
  geom_errorbar(aes(ymin=Mean-sd, ymax=Mean+sd), width=.2)









