require(dplyr)
require(ggplot2)
require(readxl)
require(openxlsx)
require(tidyverse)

df <- read.csv("C:/Parisa/UVT/Martin Atzmueller/Dataset/NewHero/Py/github1/2/result/plots_FeaturesImportance/FeatureImportance2.csv", sep = ";", header = TRUE)

heatmap(asNumericMatrix(df[1:20,1:33]))


dt2 <- df[1:20,1:33] %>%
  rownames_to_column() %>%
  gather(colname, Importance, -rowname)
head(dt2)

ggplot(dt2, aes(x = rowname, y = colname, fill = Importance)) +
  geom_tile()+
  labs(y="Features", x="Day") 