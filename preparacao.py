import numpy as np
import pandas as pd
import datetime

#matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
#Defining the starting and end dates
start_date = datetime.datetime(1993,1,1)
end_date = datetime.datetime(2000,1,1)
# function for plotting histogram.
def histogram(df, col_name, bins):
    plt.hist(df[col_name], alpha=0.5, label=col_name, bins=bins)
    plt.legend(loc='upper right')
    plt.show()

# function to convert a date to age at end_date.
def convert_to_age_days(x):
    td = end_date - x
    return td.days

# function to convert a date to days after start_date.
def convert_date_to_days(x):
    td = x - start_date
    return td.days
   
   #------------------------------------------------------------
#           Clean card table

card_df = pd.read_csv("card.csv", sep=';')
print(card_df.head())
#print(card_df.dtypes)
#Converting the Card issued date to a datetime objt
card_df['issued'] = pd.to_datetime(card_df['issued'].str[:6], format='%y%m%d')
print(card_df.dtypes)

# check the date column for null values
print(card_df['issued'].isnull().sum())
#Convert the card issued date to days in number
card_df['card_issued_date'] = card_df['issued'].map(convert_date_to_days)
del card_df['issued']
# card_issued_date is now an int64.
print(card_df.dtypes)
# rename columns to better names.
card_df = card_df.rename(columns={'type': 'card_type'})
print(card_df.head())
#------------------------------------------------------------
#           Clean client table


client_df = pd.read_csv("client.csv", sep=';')
client_df = client_df.rename(columns={'district_id': 'client_district_id'})
print(client_df.head())
print(client_df.dtypes)
# functions that process the format of the birth_number.

# returns the middle two digits of a six digit integer.
def get_mid2_dig(x):
    return int(x/100) % 100

# returns the month of birth_number.
def get_month(x):
    mth = get_mid2_dig(x)
    if mth > 50:
        return mth - 50
    else:
        return mth

# returns the month of birth_number.
def get_day(x):
    return x % 100

# returns the year of birth_number.
def get_year(x):
    return int(x/10000)

# returns the gender by examining birth_number.
def get_gender(x):
    mth = get_mid2_dig(x)
    if mth > 50:
        return 'F'
    else:
        return 'M'

# converts the birth_number into a date.
def convert_int_to_date(x):
    yr = get_year(x) + 1900
    mth = get_month(x)
    day = get_day(x)
    return datetime.datetime(yr, mth, day)

# converts birth_number into age.
def convert_birthday_to_age(x):
    yr = get_year(x) + 1900
    mth = get_month(x)
    day = get_day(x)
    return convert_to_age_days(datetime.datetime(yr,mth,day))/365
    
client_df['client_age'] = client_df['birth_number'].map(convert_birthday_to_age)
client_df['client_gender'] = client_df['birth_number'].map(get_gender)
del client_df['birth_number']

print(client_df.head())
#------------------------------------------------------------
#           Clean account table

account_df = pd.read_csv('account.csv', sep=';')
account_df = account_df.rename(columns={'district_id': 'account_district_id'})

print(account_df.head())
#Converting date columns in the Account table
account_df['date'] = account_df['date'].map(convert_int_to_date)
account_df['account_date_opened'] = account_df ['date'].map(convert_date_to_days)
del account_df['date']
#Checking the frequency ofAccount table
print(account_df['frequency'].value_counts())

# translate frequency to english.
def convert_freq_to_eng(x):
    if x == 'POPLATEK MESICNE':
        return 'MONTHLY'
    elif x == 'POPLATEK TYDNE':
        return 'WEEKLY'
    elif x == 'POPLATEK PO OBRATU':
        return 'TRANSACTION'
    else:
        return 'UNKNOWN'
    
account_df['frequency'] = account_df['frequency'].map(convert_freq_to_eng)

# Renaming columns for Account
account_df = account_df.rename(columns={'frequency': 'statement_freq'})
print(account_df.head())
#------------------------------------------------------------
#           Clean disp table


disp_df = pd.read_csv('disp.csv', sep=';')
# rename disp_type.
disp_df = disp_df.rename(columns={'type': 'disp_type'})
print(disp_df.head())
print(disp_df['disp_type'].value_counts())

#------------------------------------------------------------
#           Clean district table
district_df = pd.read_csv('district.csv', sep=';')
#print(district_df.head())
# rename A1 ( it is district_id.)
district_df = district_df.rename(columns={'A1':'district_id', 'A2':'district_name', 'A3':'region', 'A4':'num_inhabitants', 'A5':'num_munipalities_gt499',
 'A6':'num_munipalities_500to1999', 'A7':'num_munipalities_2000to9999', 'A8':'num_munipalities_gt10000',
 'A9':'num_cities', 'A10':'ratio_urban', 'A11':'average_salary', 'A12':'unemp_rate95', 'A13': 'unemp_rate96',
 'A14':'num_entrep_per1000', 'A15':'num_crimes95', 'A16':'num_crimes96'})
print(district_df.head())
# something wrong with unemp_rate95 and num_crimes95.
print(district_df.dtypes)
district_df['unemp_rate95'].value_counts()[50:100]
district_df['num_crimes95'].value_counts()[1:50]

def convert_question_marks(x, typ):
    if x == '?':
        return -1
    elif typ == 'float':
        return float(x)
    else:
        return int(x)
    
district_df['unemp_rate95'] = district_df['unemp_rate95'].apply(convert_question_marks, args=('float',))
district_df['num_crimes95'] = district_df['num_crimes95'].apply(convert_question_marks, args=('int',))
print(district_df.dtypes)

#------------------------------------------------------------
#           Clean loan table

loan_df = pd.read_csv('loan.csv', sep=';')
print(loan_df.head())
# convert loan date to integer.
loan_df['date'] = loan_df['date'].map(convert_int_to_date)
loan_df['loan_date'] = loan_df['date'].map(convert_date_to_days)
del loan_df['date']
loan_df = loan_df.rename(columns={'amount': 'loan_amount', 'duration':'loan_duration', 'payments':'monthly_loan_payment', 'status':'loan_status'})
print(loan_df.head())
#------------------------------------------------------------
#           Clean order table

order_df = pd.read_csv('order.csv', sep=';')
print(order_df.head())
print(order_df['k_symbol'].value_counts())
# translate k_symbol to english.
def convert_k_symbol_to_eng(x):
    if x == 'POJISTNE':
        return 'INSURANCE_PAYMENT'
    elif x == 'SIPO':
        return 'HOUSEHOLD_PAYMENT'
    elif x == 'LEASING':
        return 'LEASING_PAYMENT'
    elif x == 'UVER':
        return 'LOAN_PAYMENT'
    else:
        return 'UNKNOWN'
# use map, apply to k_symbol
order_df ['order_k_symbol'] = order_df ['k_symbol'].map(convert_k_symbol_to_eng)
del order_df['k_symbol']
# rename the column names as per remarks
order_df = order_df.rename(columns={'bank_to': 'order_bank_to', 'account_to':'order_account_to', 'amount':'order_amount'})


print(order_df.head())                              

#------------------------------------------------------------
#        Clean transaction table
trans_df = pd.read_csv('trans.csv', sep=';', low_memory=False)
print(trans_df.head()) 
print(trans_df['k_symbol'].value_counts())

def convert_trans_type_to_eng(x):
    if x == 'PRIJEM':
        return 'CREDIT'
    elif x == 'VYDAJ':
        return 'WITHDRAWAL'
    else:
        return 'UNKNOWN'
    
def convert_trans_op_to_eng(x):
    if x == 'VYBER KARTOU':
        return 'CC_WITHDRAWAL'
    elif x == 'VKLAD':
        return 'CREDIT_IN_CASH'
    elif x == 'PREVOD Z UCTU':
        return 'COLLECTION_FROM_OTHER_BANK'
    elif x == 'VYBER':
        return 'WITHDRAWAL_IN_CASH'
    elif x == 'PREVOD NA UCET':
        return 'REMITTANCE_TO_OTHER_BANK'    
    else:
        return 'UNKNOWN'
    
def convert_trans_k_symbol_to_eng(x):
    if x == 'POJISTNE':
        return 'INSURANCE_PAYMENT'
    elif x == 'SLUZBY':
        return 'PAYMENT_FOR_STATEMENT'
    elif x == 'UROK':
        return 'INTEREST_CREDITED'
    elif x == 'SANKC. UROK':
        return 'SANCTION_INTEREST'
    elif x == 'SIPO':
        return 'HOUSEHOLD'
    elif x == 'DUCHOD':
        return 'OLD_AGE_PENSION'  
    elif x == 'UVER':
        return 'LOAN_PAYMENT'      
    else:
        return 'UNKNOWN'
trans_df['trans_type'] = trans_df['type'].map(convert_trans_type_to_eng)
trans_df['trans_operation'] = trans_df['operation'].map(convert_trans_op_to_eng)
trans_df['trans_k_symbol'] = trans_df['k_symbol'].map(convert_trans_k_symbol_to_eng)

del trans_df['type']
del trans_df['operation']
del trans_df['k_symbol']
trans_df['date'] = trans_df['date'].map(convert_int_to_date)
trans_df['trans_date'] = trans_df['date'].map(convert_date_to_days)
del trans_df['date']


trans_df = trans_df.rename(columns={'amount': 'trans_amount', 'balance':'balance_after_trans', 'bank':'trans_bank_partner', 'account':'trans_account_partner'})
#print(trans_df.head(n=10))
print(loan_df.head())


