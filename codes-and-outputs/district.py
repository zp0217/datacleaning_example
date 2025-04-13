# import pandas package as pd
import pandas as pd
#reading csv
district = pd.read_csv("/Users/zp/hw-2-zp199717/data/districts.csv")
#rename id as district_id
district = district.rename(columns = {'id':'district_id'})
#checking data type,tail and head of the data
print(district.dtypes)
district.head(10)
district.tail(10)

#remove brackets in  municipality_info,unemployment_rate,commited_crimes all at once
district[['municipality_info','unemployment_rate','commited_crimes']] = district[['municipality_info','unemployment_rate','commited_crimes']].apply(lambda col: col.str.replace(r'\[|\]', '', regex=True))

#Split municipality_info into individual columns
district[['municipality_population<500', 'municipality_population_500-1999',
              'municipality_population_2000-9999', 'municipality_population>=10000']] = district['municipality_info'].str.split(',', expand=True)

# Split unemployment_rate into individual columns for 95 and 96
district[['unemployment_rate_for_95', 'unemployment_rate_for_96']] = district['unemployment_rate'].str.split(',', expand=True)

# Split commited_crimes into individual columns for 95 and 96
district[['crimes_committed_in_95', 'crimes_committed_in_96']] = district['commited_crimes'].str.split(',', expand=True)

#drop column municipality_info,unemployment_rate,commited_crimes
district = district.drop(columns=['municipality_info', 'unemployment_rate', 'commited_crimes'])

#check NA
print(district.apply(lambda col: col.astype(str).str.contains('NA', na=False)).sum())

#checking data type since datatype for municipality_info,unemployment_rate,commited_crimes were object, before tidying
print(district.dtypes)

#changing data type of newly created columns from object to numeric
district['crimes_committed_in_96'] = pd.to_numeric(district['crimes_committed_in_96'])
district['unemployment_rate_for_96'] = pd.to_numeric(district['unemployment_rate_for_96'])
district['municipality_population<500'] = pd.to_numeric(district['municipality_population<500'])
district['municipality_population_500-1999'] = pd.to_numeric(district['municipality_population_500-1999'])
district['municipality_population_2000-9999'] = pd.to_numeric(district['municipality_population_2000-9999'])
district['municipality_population>=10000'] = pd.to_numeric(district['municipality_population>=10000'])

#check data types
print(district.dtypes)

#script to produce csv file inside the folder codes-and-output
district.to_csv('/Users/zp/hw-2-zp199717/codes-and-outputs/district_py.csv')
