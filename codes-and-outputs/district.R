#using tidyverse package
library(tidyverse)

# reading csv
district<- read.csv("/Users/zp/hw-2-zp199717/data/districts.csv")

#rename id as district_id
district<-district%>% rename(district_id = id)

#check data type
str(district)

#checking NA value
sum(is.na(district))

#two NAs are found and find which column they are in
colnames(district)[ apply(district, 2, anyNA) ]
#NA is in column unemployment_rate_for_95" "crimes_committed_in_95"
#replace NA after tidy data

#tidy data

# remove [] in municipality_info
district<- district %>% mutate(municipality_info = str_remove_all(municipality_info, "\\[|\\]")) %>%
# separate  municipality_info into four columns
  separate(municipality_info, into = c("municipality_population<500", "municipality_population_500-1999",                                      "municipality_population_2000-9999","municipality_population_>=10000"),sep = ",", convert = TRUE)%>%
#remove [] in unemployment_rate
mutate(unemployment_rate = str_remove_all(unemployment_rate, "\\[|\\]")) %>%
# separate unemployment_rate into two columns
separate(unemployment_rate, into = c("unemployment_rate_for_95",  "unemployment_rate_for_96"),sep = ",", convert = TRUE) %>%

#remove [] in commited crimes
mutate(commited_crimes = str_remove_all(commited_crimes, "\\[|\\]")) %>%
#separate commited_crimes into two columns
separate(commited_crimes, into = c("crimes_committed_in_95","crimes_committed_in_96"),sep = ",", convert = TRUE)

#check data type of tidy data
str(district)


#script to produce csv file inside the folder codes-and-output
write_csv(district,"/Users/zp/hw-2-zp199717/codes-and-outputs/district_r.csv")
