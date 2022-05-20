require(dplyr)
require(ggplot2)
require(readxl)
require(openxlsx)
require(tidyverse)

df <- read.csv("C:/Parisa/UVT/Martin Atzmueller/Dataset/NewHero/Py/github1/2/result/plots_FeaturesImportance/FeatureImportance.csv", sep = ";", header = TRUE)

#heatmap(asNumericMatrix(df[1:20,1:33]))


dt2 <- df[1:20,2:34] %>%
  rownames_to_column() %>%
  gather(colname, Importance, -rowname)
#dt2$rowname <- factor(dt2$rowname)
head(dt2)


#Turn your 'treatment' column into a character vector
dt2$rowname <- as.character(dt2$rowname)#Then turn it back into a factor with the levels in the correct order
dt2$rowname <- factor(dt2$rowname, levels=unique(dt2$rowname))

ggplot(dt2, aes(x = rowname, y = colname, fill = Importance)) +
  geom_tile()+
  labs(y="Features", x="Day") 







#######################

