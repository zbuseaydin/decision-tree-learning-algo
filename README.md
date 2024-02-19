# CMPE480 Fall 23-24 HW4 Decision Learning Tree


## Dataset
The dataset I worked on is for loan prediction. There are 8 attributes:
- **Loan_ID:** a unique ID for each person
- **Gender:** “Male” or “Female”
- **Married:** “Yes” or “No”
- **Education:** “Graduate” or “Not Graduate”
- **Self_Employed:** “Yes” or “No”
- **Credit_History:** “0” or “1”
- **Property_Area:** “Rural”, “Urban” or “Semiurban”
- **Loan_Status:** “Y” or “N”

Depending on the background features of the given person, it is decided if they will be granted the loan or not. The attributes 2 to 7 are used as the background features of the person, and with them Loan_Status is decided as “Y” indicating they will get the loan, or “N” otherwise.


## 5-Fold Cross Validation
In total, there were 511 entries in the dataset. They were splitted into 2: 86 for testing, 425 for training and validation. Then, the 425 entries were again splitted into 2: 75% for training and 25% for validation. This was done 5 times and at each iteration i the entries from i*85 to (i+1)*85 were taken as the validation, and the remaining as the training set. At each iteration a new decision tree was created and the error was calculated using the validation set. Finally, the overall error was calculated as the average of these 5 errors.


## Error Plots
### Validation Errors:
Here, each tree that is generated at each iteration during k-fold cross validation is validated and the errors can be seen in the plot.
(./validation_errors.png)

The errors are as follows:
0.2352941
0.2588235
0.2
0.2235294
0.2235294

The overall error is the average = 
0.2282353



### Test Errors:
Each tree is also tested with the test set.
The errors are as follows:
0.22093023255813954
0.18604651162790697
0.18604651162790697
0.19767441860465115
0.19767441860465115











Final Decision Tree
Since the second tree (Tree2) gives the smallest errors, it is the best one.






