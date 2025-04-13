library(tidyverse)  # using library for package tidyverse
#reading csv
loans<- read.csv("/Users/zp/hw-2-zp199717/data/loans.csv")

#rename id as loan_id
loans<-loans%>% rename(loan_id = id)

#changing date from type int to type date
loans$date<- as.Date(loans$date)



#1. melt dataset to make it tidy
#2.only extract rows with X in column counts(erase rows that has "-")
#3. divide column to month and payment inside test column( test column has values such as X24_A) by "_" and store it to each column(ex 24 in month A in payment status)
#4.remove  any value that has X(like X24) from the column month
#5.erase column counts
loans<- loans%>% pivot_longer(cols = X24_A:X60_A,names_to = 'test',values_to = "counts")%>%
filter(counts != "-")%>%
separate(test,c('month','payment_status'),sep = "_")%>%
mutate(month = str_remove(month,"X"))%>%
select(-counts)


# script to produce csv file inside the folder codes-and-output
write_csv(loans,"/Users/zp/hw-2-zp199717/codes-and-outputs/loans_r.csv")
