#### LASSO Exploration for Variable Selection #######

# Read Data
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

df<-read.csv("../../data/preprocessed/football.csv",header=TRUE)

# Load Libraries
set.seed(123)    # seef for reproducibility
library(car)
library(glmnet)
library(plotmo)
library(faraway)
library(lubridate)
library(dplyr)
library(MASS)

# Check missing values
sum(is.na(df))
Upset <- df$Upset
df = df[ , !(names(df) %in% c('Upset','HomeTeam','AwayTeam'))]

# Scale features
ind <- sapply(df, is.numeric)
df[ind] <- lapply(df[ind], scale)
df = cbind(df, Upset)

# Lasso
y <- df$Upset
X <- model.matrix(Upset~.,df)
lambdas_to_try  <- 10^seq(10, -2, length = 100)
cv.out <- cv.glmnet(X, y, alpha = 1, lambda = lambdas_to_try,standardize = TRUE, nfolds = 10)
#plot(cv.out)

# Find best lambda
bestlam=cv.out$lambda.min
coef(cv.out)
lasso_lm <-glmnet(X, y, alpha = 1, lambda = bestlam )
tmp_coeffs <- coef(lasso_lm)

# Dat frame with coefficients
data_frame_coeffs = data.frame(name = tmp_coeffs@Dimnames[[1]][tmp_coeffs@i + 1], coefficient = tmp_coeffs@x)

