# import pandas package as pd
import pandas as pd

#reading csv
loans = pd.read_csv("/Users/zp/hw-2-zp199717/data/loans.csv")
#rename id as loan_id
loans = loans.rename(columns = {'id':'loan_id'})
#changing date from type int to type date
loans['date'] =  pd.to_datetime(loans['date'])

#1. melt dataset to make it tidy
#2.only extract rows with X in column counts(erase rows that has "-")
#3. divide column to month and payment inside test column( test column has values such as X24_A) by "_" and store it to each column(ex 24 in month A in payment status)
#4.remove  any value that has X(like X24) from the column month
#5.erase column counts
loans = loans.melt(id_vars = ['loan_id','account_id','date','amount','payments'],var_name='test',value_name = 'counts')
loans = loans[loans.counts != '-']
loans[['month','payment_status']]= loans['test'].str.split('_',expand = True)
loans = loans.drop(['test','counts'],axis = 1)
loans = loans.sort_values(by = ['loan_id'])

# script to produce csv file inside the folder codes-and-output
loans.to_csv('/Users/zp/hw-2-zp199717/codes-and-outputs/loans_py.csv')
