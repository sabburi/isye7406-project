#### Pick a representative variable from groups of correlated variables for Variable Selection #######

# Read data
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
df<-read.csv("football.csv",header=TRUE)

# Load library
library(broom)
library(igraph)

# Drop variable
drops <- c('AwayTeam','HomeTeam')
df = df[ , !(names(df) %in% drops)]

# Correlation matrix
var.corelation <- cor(as.matrix(df), method="pearson")

# Prevent duplicated pairs and find variables with corelation above 0.6
var.corelation <- var.corelation*lower.tri(var.corelation)
check.corelation <- which(var.corelation>0.6, arr.ind=TRUE)
graph.cor <- graph.data.frame(check.corelation, directed = FALSE)
groups.cor <- split(unique(as.vector(check.corelation)),         clusters(graph.cor)$membership)
groups = lapply(groups.cor,FUN=function(list.cor){rownames(var.corelation)[list.cor]})


# Calculate mean correlation between variables in the same groups
a = c()
for (group in groups){
  print(group)
  g = group
  subset_group = (df[,g])
  subset_group = cor(as.matrix(subset_group), method="pearson")
  diag(subset_group) = 0
  avg_corr = colSums(subset_group[,])/(length(g)-1)
  print(sort(avg_corr, decreasing = T)[1])
  a = c(a,sort(avg_corr, decreasing = T)[1])
  print('#####################')
  
}


# Print correlation variable groups
for (group in groups){
  print(group)
}
b = tidy(a)
