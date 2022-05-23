
require(dplyr)
require(ggplot2)
require(readxl)
require(openxlsx)

df2 <- read.csv("C:/Parisa/UVT/Martin Atzmueller/Dataset/NewHero/Py/github1/2/result/accuracy_precision_recall_fscore/accuracy.csv", sep = ";", header = TRUE)
df2
df<-data.frame(df2)


df1 <- read.csv("C:/Parisa/UVT/Martin Atzmueller/Dataset/NewHero/Py/github1/2/result/accuracy_precision_recall_fscore/accuracy2.csv", sep = ";", header = TRUE)
df1



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






ggplot(df1, aes(x=Day)) +
  geom_line(aes(y = majorityclass_baseline, color="majorityclass_baseline")) +
  geom_line(aes(y = accuracy, color="accuracy"))+
  geom_point(aes(y = accuracy, color="accuracy", shape="accuracy", size=2)) +
  geom_ribbon(aes( ymin=accuracy-sda, ymax=accuracy+sda, fill="accuracy", shape="accuracy", size=2),
               alpha=0.3)+
  geom_line(aes(y = precision, color="precision")) +
  geom_point(aes(y = precision, color="precision", shape="precision", size=2)) +
   geom_ribbon(aes( ymin=precision-sdp, ymax=precision+sdp, fill="precision", shape= "precision", size=2),
               alpha=0.3)+
  geom_line(aes (y = recall, color="recall")) +
  geom_point(aes (y = recall, color="recall", shape= "recall", size=2)) +
  geom_ribbon(aes( ymin=recall-sdr, ymax=recall+sdr, fill="recall", shape= "recall", size=2),
                alpha=0.3)+
  geom_point(aes (y = fscore, color="fscore", shape= "fscore", size=2)) +
   geom_ribbon(aes( ymin=fscore-sdf, ymax=fscore+sdf, fill="fscore", shape= "fscore", size=2),
                alpha=0.3)+
  
  #scale_color_manual(values = c( "steelblue",  "green", "black","red", "darkred")) +
  labs(y="Mean") +
  theme(legend.title=element_blank())








