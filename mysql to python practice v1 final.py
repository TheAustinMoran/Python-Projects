Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
#import libraries

import mysql.connector
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

#establish connection to mysql database
db=mysql.connector.connect(host='localhost',
                           database='Lending',
                           user='root',
                           password='************')

#create cursor to work on mysql db
cursor=db.cursor()

#retrieve all data from loans table
cursor.execute('SELECT * FROM loans')
#read loans data into pandas df
df_loans=pd.DataFrame(cursor.fetchall())

#read first five rows of new loans df
df_loans.head()
          0   1                   2           3   ...  11  12  13  14
0  180400932  03     Clark, Courtney  2021-04-01  ...  KY  13  01  01
1  180501386  03  Lawrence, Jennifer  2021-05-06  ...  KY  13  11  03
2  180601723  03       Oliver, James  2021-06-02  ...  KY  13  10  03
3  500300341  08         Allan, Zach  2021-03-01  ...  KY  09  02  02
4  500300380  14       Morrison, Van  2021-05-26  ...  KY  03  08  04

[5 rows x 15 columns]

#rename columns
loans_headers = ['loan_id', 'branch_id', 'borrower', 'app_date', 'close_date', 'product', 'purpose', 'rate', 'amount', 'address', 'city', 'state', 'lo_id', 'lp_id', 'uw_id']
df_loans.columns=loans_headers
#check changes took
df_loans.head()
     loan_id branch_id            borrower    app_date  ... state lo_id lp_id uw_id
0  180400932        03     Clark, Courtney  2021-04-01  ...    KY    13    01    01
1  180501386        03  Lawrence, Jennifer  2021-05-06  ...    KY    13    11    03
2  180601723        03       Oliver, James  2021-06-02  ...    KY    13    10    03
3  500300341        08         Allan, Zach  2021-03-01  ...    KY    09    02    02
4  500300380        14       Morrison, Van  2021-05-26  ...    KY    03    08    04

[5 rows x 15 columns]

#check datatypes
df_loans.dtypes
loan_id       object
branch_id     object
borrower      object
app_date      object
close_date    object
product       object
purpose       object
rate          object
amount        object
address       object
city          object
state         object
lo_id         object
lp_id         object
uw_id         object
dtype: object

#convert datatypes
df_loans['rate']=df_loans['rate'].astype('float')
df_loans['amount']=df_loans['amount'].astype('float')
df_loans['app_date']=df_loans['app_date'].astype('datetime64[ns]')
df_loans['close_date']=df_loans['close_date'].astype('datetime64[ns]')
#check changes took
df_loans.dtypes
loan_id               object
branch_id             object
borrower              object
app_date      datetime64[ns]
close_date    datetime64[ns]
product               object
purpose               object
rate                 float64
amount               float64
address               object
city                  object
state                 object
lo_id                 object
lp_id                 object
uw_id                 object
dtype: object

#retrieve branches table from mysql db
cursor.execute('SELECT * FROM branches')
#create df with branches data
df_branches=pd.DataFrame(cursor.fetchall())
#check branches df
df_branches.head()
    0                        1                                            2
0  01         Southern Parkway   123 Southern Parkway Louisville, KY, 40214
1  02             South Corbin           123 S Corbin Way Corbin, KY, 40160
2  03  Old Brownsboro Crossing  3701 Von Allmen Court Louisville, KY, 40245
3  04                    Dixie     6400 Dixie Highway Louisville, KY, 40258
4  05                 Somerset         6500 Trucker Way Somerset, KY, 40055

#close cursor & db connection
cursor.close()
True
db.close()

#rename branch columns
branches_headers=['branch_id', 'branch', 'address']
df_branches.columns=branches_headers

#drop address column
df_branches.drop('address', axis=1, inplace=True)

#set index to branch id column
df_branches.set_index('branch_id', inplace=True)

#check changes
df_branches.head()
                            branch
branch_id                         
01                Southern Parkway
02                    South Corbin
03         Old Brownsboro Crossing
04                           Dixie
05                        Somerset


#merging loans & branches df on branch_id
merged_df=pd.merge(df_loans, df_branches, on='branch_id', how='left')

#dropping branch_id column
merged_df.drop('branch_id', axis=1, inplace=True)

df_loans=merged_df
df_loans.head()
     loan_id            borrower  ... uw_id                   branch
0  180400932     Clark, Courtney  ...    01  Old Brownsboro Crossing
1  180501386  Lawrence, Jennifer  ...    03  Old Brownsboro Crossing
2  180601723       Oliver, James  ...    03  Old Brownsboro Crossing
3  500300341         Allan, Zach  ...    02                   Smyrna
4  500300380       Morrison, Van  ...    04       Ft. Wright Walmart

[5 rows x 15 columns]

#reordering columns
print(list(df_loans.columns))
['loan_id', 'borrower', 'app_date', 'close_date', 'product', 'purpose', 'rate', 'amount', 'address', 'city', 'state', 'lo_id', 'lp_id', 'uw_id', 'branch']
df_loans=df_loans[['loan_id', 'branch', 'borrower', 'app_date', 'close_date', 'product', 'purpose', 'rate', 'amount', 'address', 'city', 'state', 'lo_id', 'lp_id', 'uw_id']]

df_loans.head()
     loan_id                   branch            borrower  ... lo_id lp_id uw_id
0  180400932  Old Brownsboro Crossing     Clark, Courtney  ...    13    01    01
1  180501386  Old Brownsboro Crossing  Lawrence, Jennifer  ...    13    11    03
2  180601723  Old Brownsboro Crossing       Oliver, James  ...    13    10    03
3  500300341                   Smyrna         Allan, Zach  ...    09    02    02
4  500300380       Ft. Wright Walmart       Morrison, Van  ...    03    08    04

[5 rows x 15 columns]

#create series data for count of branches
branch_counts=df_loans['branch'].value_counts()
branch_counts
branch
Smyrna                     14
Mt. Washington             13
Old Brownsboro Crossing    11
Veteran's Parkway          10
Erlanger                    7
Hikes Point                 7
South Corbin                6
London South                6
Downtown                    4
Williamsburg Walmart        3
London Downtown             3
New Albany                  3
Jeffersontown               3
Southern Parkway            2
Middletown Walmart          2
Ft. Wright Walmart          2
Somerset                    2
Crestwood                   1
Dixie                       1
Name: count, dtype: int64
>>> 
>>> #plot bar graph of branch counts
>>> 
>>> #lay gridlines under bars
>>> plt.rcParams['axes.axisbelow']=True
>>> 
>>> branch_counts.plot(kind='bar')
<Axes: xlabel='branch'>
>>> #label axes & create title
>>> plt.xlabel('Branches')
Text(0.5, 0, 'Branches')
>>> plt.ylabel('Number of Loans')
Text(0, 0.5, 'Number of Loans')
>>> plt.title('Number of Loans by Branch')
Text(0.5, 1.0, 'Number of Loans by Branch')
>>> #remove legend & add gridlines
>>> plt.legend('', frameon=False)
<matplotlib.legend.Legend object at 0x00000245E027FE00>
>>> plt.grid(True)
>>> 
>>> plt.tight_layout()
>>> plt.show()
