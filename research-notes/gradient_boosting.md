# Gradient Boosting for Regression

## Pre-reqs 
### Decision trees 
Structure is in the form of 
* statement 
* outcome 

When the statement results in an outcome of numeric values then it is a regression tree. When the statement results in an outcome of classification it is a classification tree.

## Gradient boosting algorithm
* first take all the average of all the y values (this is the prediction for all x initially)
* build a tree based on each of the errors
* find the residuals
* build the tree based on params to predict the residuals
* you can then use the decision tree based on the params to figure out the residual, this can then be added to the mean y value to get the prediction 

Not good enough to stop here because there is low bias but very high variance
*  adjusted by the learning rate 
* this way we just nudge the prediction to the fitted direction 
* based on empirical studies taking lots of small steps in the right direction is better

This is then done recursively with the new generation's predictions 
* multiple trees are created and the values are then added as a weighted sum to find the final output


## Extreme Gradient Boosting (XGBoost)
* efficient implementation of the gradient boosting algorithm 
* dominates structured or tabular datasets on classification and regression problems


## References 
[XGBoost Guide for Regression](https://machinelearningmastery.com/xgboost-for-regression/)
[StatQuest - Gradient Boost Part 1 (of 4): Regression Main Ideas](https://www.youtube.com/watch?v=3CC4N4z3GJc)
