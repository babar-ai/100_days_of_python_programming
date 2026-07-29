# loc[] and iloc[] are indexing functions in Pandas used to select rows and columns from a DataFrame or Series

#loc[]:
'''
loc[] - Label-Based Indexing
Purpose: Select data using labels (row and column names).
Syntax:
DataFrame.loc[row_labels, column_labels]
* Access rows and columns by explicit labels (e.g., row index or column names).
* To apply conditions for filtering.
'''

#example 
import pandas as pd

mydata = {'Name': ['alice','bob'],
          'age':[21,32],
          'score':[50,55]
            }
df = pd.DataFrame(mydata)
print(df.head())

#to access specific column or row data through label 
a_age = df.loc[0,'age']
print(f'Alice is {a_age} year old')

print("\n")
result = df.loc[df['age']>20] 
print(f"ages greater than 20 are \n {result}")
print('\n') 

# iloc[]
'''
iloc[] - Integer-Based Indexing
Purpose: Select data using integer positions (row and column positions).
Syntax:
DataFrame.iloc[row_indices, column_indices]
*Useful when you don’t know labels but know positions.
* For quick access to rows and columns without caring about labels.

'''
customers = df.iloc[0:2,0]
print(f'Names of the customers are \n {customers}')
print('\n')

#lets i want to access datacell at location 55
score = df.iloc[1,2]
print(score)