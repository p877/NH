
require(dplyr)
require(ggplot2)
require(readxl)
require(openxlsx)




df1 <- read.csv("/Users/pshayan/Downloads/Py/github1/2/result/accuracy_precision_recall_fscore/accuracy2.csv", sep = ";", header = TRUE)
df1


majorityclass_baseline <- df1[1:20,8]
accuracy <- df1[1:20,4]
precision <- df1[1:20,5]
recall <- df1[1:20,6]
fscore <- df1[1:10,7]



ggplot(df1, aes(x=Day)) +
  geom_line(aes(y = majorityclass_baseline, color="majorityclass_baseline")) +
  geom_line(aes(y = accuracy, color="accuracy")) +
  geom_line(aes(y = precision, color="precision")) +
  geom_line(aes (y = recall, color="recall")) +
  geom_line(aes (y = fscore, color="fscore")) +
  scale_color_manual(values = c( "steelblue",  "green", "black","red", "darkred")) +
  labs(y="Value") +
  theme(legend.title=element_blank())












