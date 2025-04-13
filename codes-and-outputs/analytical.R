
#using tidyverse package

library(conflicted)
library(tidyverse)
conflict_prefer("filter", "dplyr")
conflict_prefer("lag", "dplyr")
#i had error
#Use the conflicted package (<http://conflicted.r-lib.org/>) to force all conflicts to become errors

# so i referenced this link to solve this
#https://stackoverflow.com/questions/73336628/package-conflicts-in-rlibrary(tidyverse)

library(dplyr)
# reading csv
accounts<- read.csv("/Users/zp/hw-2-zp199717/data/accounts.csv")
cards<-read.csv("/Users/zp/hw-2-zp199717/data/cards.csv")
clients<- read.csv("/Users/zp/hw-2-zp199717/data/clients.csv")
links<- read.csv("/Users/zp/hw-2-zp199717/data/links.csv")
payment_orders<-read.csv("/Users/zp/hw-2-zp199717/data/payment_orders.csv")
transactions<-read.csv("/Users/zp/hw-2-zp199717/data/transactions.csv")
district<-read.csv("/Users/zp/hw-2-zp199717/codes-and-outputs/district_r.csv")
loans<-read.csv("/Users/zp/hw-2-zp199717/codes-and-outputs/loans_r.csv")

# rename ids (ex. id in accounts data as account_id)
accounts<-accounts%>% rename(account_id = id)
clients<-clients%>% rename(client_id = id)
links<-links%>% rename(link_id = id)
transactions<-transactions%>% rename(transaction_id = id)
payment_orders<-payment_orders%>% rename(order_id = id)
cards<-cards%>% rename(card_id = id)

#change date in each csv file  same names but indicates differently
accounts<- accounts%>%rename(open_date = date)

#rename columns in each csv file since there are same names but indicates different
loans<- loans%>% rename(loan_granted_date = date)
transactions<- transactions%>% rename(transaction_date = date)
links<- links%>%rename(owner_user_type = type)
transactions<- transactions%>%rename(debit_or_credit = type)
transactions<- transactions%>%rename(transaction_amount = amount)
payment_orders<- payment_orders%>%rename(payment_order_amount = amount)
cards<- cards%>%rename(credit_card_name = type)

# for a start dat1 is a dataframe that will be used for all the joining process
# join accounts.csv with district.csv(tidy data in step2) and name this result as dat1
dat1<-accounts%>% left_join(district)

#join link.csv and client.csv using left join
client<- links%>% left_join(clients,by = "client_id")
#count number of clients using group by function respect to account_id

client_count<- client%>% group_by(account_id)%>%
  summarise(num_customers = n())

# join dat1 and clients_count(one that has counted number of clients associated with account)
#by account_id using left join

dat1<- dat1%>% left_join(client_count,by = "account_id")

# join cards.csv and links.csv using left join first
#next count number of credit cards for an account using group by function(account_id)
#and use summarize to get the number based on account_id

credit_card<- cards%>% left_join(links,by = c("link_id"))
credit_count<- credit_card%>% group_by(account_id) %>%
  summarize(credit_cards = n())

#join dat1 and credit_count(with counts) using left join
dat1<- dat1%>% left_join(credit_count,by = "account_id")

# replace NA to 0 in credit_cards
dat1<- dat1%>% mutate(credit_cards = replace_na(credit_cards,0))

# add loan column in loan dataframe and rename columns in loans.csv as
#loan_amount = amount, loan_payments = payments, loan_term = month, loan_status = payment_status
loan<- loans %>% mutate(loan = T)%>%
  rename(loan_amount = amount, loan_payments = payments, loan_term = month, loan_status = payment_status)

# join dat1 with loan dataframe using left join.replace NA as False in loan column
dat1<- dat1%>% left_join(loan,by = "account_id")%>%
  mutate(loan = replace_na(loan,F))

# create loan_default column and assign T if loan status is B or D, assign F if A or C, NA if not exists
dat1<- dat1%>%mutate(loan_default = ifelse(loan_status %in% c("B","D"),T,ifelse(!is.na(loan_status),F,NA)))

# create debit dataframe that only has type debit since debit indicates withdrawal transaction
debit<- transactions %>% filter(debit_or_credit == "debit")

# compute max and min withdrawal using debit dataframe, which only has debit type in transaction.csv
#respect to account_id
transaction<- debit%>% group_by(account_id)%>%
  summarize(max_withdrawal = max(transaction_amount,na.rm = T),min_withdrawal = min(transaction_amount,na.rm = T))

#join dat1 and transaction dataframe using left join
dat1<- dat1%>% left_join(transaction,by = "account_id")

# join transactions.csv,payment_orders.csv using inner join
payment<- transactions%>%inner_join(payment_orders,by = "account_id",relationship = "many-to-many")
#count credit payments for the account for all cards
credits<- payment%>% filter(method == "credit card")%>%
  group_by(account_id)%>%
  summarise(cc_payments = n())

#join dat1 and credits(counted for credit payments) using left join
dat1<- dat1%>%left_join(credits,by = "account_id")

 #compute max and minimum balance from transaction.csv respect to account_id and store this as balance
balance<- transactions%>% group_by(account_id)%>%
  summarise(max_balance = max(balance,na.rm = T),min_balance = min(balance,na.rm = T))

#join dat1 and balance using left_join and rename dataframe as analytical
analytical<- dat1%>% left_join(balance,by = "account_id")

write_csv(analytical,"/Users/zp/hw-2-zp199717/codes-and-outputs/analytical_r.csv")
