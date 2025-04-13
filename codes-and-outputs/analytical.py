#import python package pandas,numpy
import pandas as pd
import numpy as np

#reading csv
accounts = pd.read_csv("/Users/zp/hw-2-zp199717/data/accounts.csv")
cards =  pd.read_csv("/Users/zp/hw-2-zp199717/data/cards.csv")
clients= pd.read_csv("/Users/zp/hw-2-zp199717/data/clients.csv")
links=pd.read_csv("/Users/zp/hw-2-zp199717/data/links.csv")
payment_orders = pd.read_csv("/Users/zp/hw-2-zp199717/data/payment_orders.csv")
transactions = pd.read_csv("/Users/zp/hw-2-zp199717/data/transactions.csv")
district = pd.read_csv("/Users/zp/hw-2-zp199717/codes-and-outputs/district_r.csv")
loans = pd.read_csv("/Users/zp/hw-2-zp199717/codes-and-outputs/loans_r.csv")

# Rename 'id' columns in each DataFrame
accounts = accounts.rename(columns={"id": "account_id"})
cards = cards.rename(columns={"id": "card_id"})
clients = clients.rename(columns={"id": "client_id"})
links = links.rename(columns={"id": "link_id"})
payment_orders = payment_orders.rename(columns={"id": "order_id"})
transactions = transactions.rename(columns={"id": "transaction_id"})

loans = loans.rename(columns={"date": "loan_granted_date"})
transactions = transactions.rename(columns={
    "date": "transaction_date",
    "type": "debit_or_credit",
    "amount": "transaction_amount"
})
links = links.rename(columns={"type": "owner_user_type"})
payment_orders = payment_orders.rename(columns={"amount": "payment_order_amount"})
cards = cards.rename(columns={"type": "credit_card_name"})

#for a start dat1 is a dataframe that will be used for all the joining process
# join accounts.csv with district.csv(tidy data in step2) and name this
#result as dat1

dat1 = pd.merge(accounts, district, how="left")

#join link.csv and client.csv using left join
client = pd.merge(links, clients, on="client_id", how="left")

#count number of clients using group by function respect to account_id
client_count = client.groupby("account_id").size().reset_index(name="num_customers")

# join dat1 and clients_count(one that has counted number of clients associated with account)
#by account_id using left join
dat1 = pd.merge(dat1, client_count, on="account_id", how="left")

# join cards.csv and links.csv using left join
credit_card = pd.merge(cards, links, on="link_id", how="left")

#count number of credit cards for an account using groupby function(account_id)
credit_count = credit_card.groupby("account_id").size().reset_index(name="credit_cards")

#join dat1 and credit_count(with counts) using left join
dat1 = pd.merge(dat1, credit_count, on="account_id", how="left")

# replace NA to 0 in credit_cards
dat1["credit_cards"] = dat1["credit_cards"].fillna(0)

# add loan column in loan dataframe and rename columns in loans.csv as
#loan_amount = amount, loan_payments = payments, loan_term = month, loan_status = payment_status
loan = loans.assign(loan=True).rename(columns={"amount": "loan_amount", "payments": "loan_payments", "month": "loan_term", "payment_status": "loan_status"})

# join dat1 with loan dataframe using left join
dat1 = pd.merge(dat1, loan, on="account_id", how="left")

#replace NA as False in loan column
dat1["loan"] = dat1["loan"].fillna(True)

## create loan_default column and assign T if loan status is B or D, assign F if A or C, NA if not exists
dat1["loan_default"] = dat1["loan_status"].apply(lambda x: True if x in ["B", "D"] else (False if pd.notna(x) else pd.NA))

# create debit dataframe that only has type debit since debit indicates withdrawal transaction
debit = transactions[transactions["debit_or_credit"] == "debit"]

# compute max and min withdrawal using debit dataframe, which only has debit type in transaction.csv
#respect to account_id
transaction = debit.groupby("account_id").agg(max_withdrawal=("transaction_amount", "max"), min_withdrawal=("transaction_amount", "min")).reset_index()

#join dat1 and transaction dataframe using left join
dat1 = pd.merge(dat1, transaction, on="account_id", how="left")

# join transactions.csv,payment_orders.csv using inner join
payment = pd.merge(transactions, payment_orders, on="account_id", how="inner")
#count credit payments for the account for all cards
credits = payment[payment["method"] == "credit card"].groupby("account_id").size().reset_index(name="cc_payments")

#join dat1 and credits(counted for credit payments) using left join
dat1 = pd.merge(dat1, credits, on="account_id", how="left")

 #compute max and minimum balance from transaction.csv respect
 #to account_id andstore this as balance
balance = transactions.groupby("account_id").agg(max_balance=("balance", "max"), min_balance=("balance", "min")).reset_index()

#join dat1 and balance using left_join and rename dataframe as analytical
analytical = pd.merge(dat1, balance, on="account_id", how="left")

# script to produce csv file inside the folder codes-and-output
analytical.to_csv("/Users/zp/hw-2-zp199717/codes-and-outputs/analytical_py.csv",na_rep = "NA")
