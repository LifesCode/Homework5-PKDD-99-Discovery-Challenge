import pandas as pd
import datetime

# Defining the starting & end dates
start_date = datetime.datetime(1993, 1, 1)
end_date = datetime.datetime(2000, 1, 1)
data_directory = "PKDD'99-Dataset"


# ------------------------------------- SUPPORT FUNCTIONS: GENERAL -----------------------------------------------------
# function to convert a date to days after start_date.
def convert_date_to_days(x):
    td = x - start_date
    return td.days


# converts the birth_number into a date.
def convert_int_to_date(x):
    yr = get_year(x) + 1900
    mth = get_month(x)
    day = get_day(x)
    return datetime.datetime(yr, mth, day)


# returns the middle two digits of a six digit integer.
def get_mid2_dig(x):
    return int(x / 100) % 100


# returns the month of birth_number.
def get_day(x):
    return x % 100


# returns the month of birth_number.
def get_month(x):
    mth = get_mid2_dig(x)
    if mth > 50:
        return mth - 50
    else:
        return mth


# returns the year of birth_number.
def get_year(x):
    return x // 10000


# ------------------------------------- SUPPORT FUNCTIONS: CLIENT TABLE ------------------------------------------------
# returns the gender by examining birth_number.
def get_gender(x):
    mth = get_mid2_dig(x)
    return 'F' if mth > 50 else 'M'

def adjust_date(x):
    yr = get_year(x) + 1900
    mth = get_month(x)
    day = get_day(x)
    return datetime.datetime(yr, mth, day)


# gets the age age, with 2 decimal places precision, based on birth day and end_date
def convert_birthday_to_age(b_day):
    born = datetime.datetime.strptime(b_day, "%Y-%m-%d").date()
    age = end_date.year - born.year - ((end_date.month, end_date.day) < (born.month, born.day))
    return age


# ------------------------------------- SUPPORT FUNCTIONS: ACCOUNT TABLE -----------------------------------------------
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


# ------------------------------------- SUPPORT FUNCTIONS: DISTRICT TABLE ----------------------------------------------
def convert_question_marks(x, typ):
    if x == '?':
        return -1
    elif typ == 'float':
        return float(x)
    else:
        return int(x)


# ------------------------------------- SUPPORT FUNCTIONS: LOAN TABLE ----------------------------------------------
def convert_status_code_to_meaning(status_code):
    code_meaning = {"A": "finished-no-problem", "B": "finished-not-payed", "C": "running-ok", "D": "running-debt"}
    return code_meaning[status_code]


# ------------------------------------- SUPPORT FUNCTIONS: ORDER TABLE -------------------------------------------------
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


def convert_trans_type_to_eng(x):
    if x == 'PRIJEM':
        return 'CREDIT'
    elif x == 'VYDAJ':
        return 'WITHDRAWAL'
    else:
        return 'UNKNOWN'


# ------------------------------------- SUPPORT FUNCTIONS: TRANSACTION TABLE -------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------- CLEANING: ACCOUNT TABLE --------------------------------------------------------
def clean_account_table(save_changes=False):
    account_df = pd.read_csv(f"{data_directory}/account.csv", sep=';')  # read and store content of the "account" table
    # print(account_df.head())  # -> visualize table's fields
    # print(account_df.dtypes)  # -> visualize table's data-types

    account_df = account_df.rename(columns={'district_id': 'account_district_id'})
    # print(account_df.head())  # -> visualize last update

    # Converting date columns in the "account" table to a more appropriate format to work with later
    account_df['date'] = account_df['date'].map(convert_int_to_date)
    # Creating a new field in the table based on the "date" field
    account_df['account_open_date'] = account_df['date']  # create another field
    del account_df['date']  # deleting the no longer needed field "date"

    # Checking the frequency of "account" table
    print(account_df['frequency'].value_counts())
    account_df['frequency'] = account_df['frequency'].map(convert_freq_to_eng)

    # Renaming fields
    account_df = account_df.rename(columns={'frequency': 'statement_freq'})
    # print(account_df.head())  # -> visualize last update

    if save_changes:  # if specified, saves the changes made
        account_df.to_csv(f"{data_directory}/account.csv", sep=";")

    return account_df


# ------------------------------------- CLEANING: CARD TABLE -----------------------------------------------------------
def clean_card_table(save_changes=False):
    card_df = pd.read_csv(f"{data_directory}/card.csv", sep=';')  # read and store the content of the "card" table
    # print(card_df.head())  # -> visualize table's fields
    # print(card_df.dtypes)  # -> visualize table's data-types

    # Converting the Card issued date to a datetime object
    card_df['issued'] = pd.to_datetime(card_df['issued'].str[:6], format='%y%m%d')
    # print(card_df.dtypes)  # -> visualize last update
    card_df['card_issued_date'] = card_df['issued']  # change card_issued_date type to int64
    del card_df['issued']
    # print(card_df.dtypes)  # -> visualize last updates

    # rename field "type" to (a more descriptive name) "card_type"
    card_df = card_df.rename(columns={'type': 'card_type'})
    # print(card_df.head())  # -> visualize last update

    if save_changes:  # if specified, saves the changes made
        card_df.to_csv(f"{data_directory}/card.csv", sep=";")

    return card_df


# ------------------------------------- CLEANING: CLIENT TABLE ---------------------------------------------------------
def clean_client_table(save_changes=False):
    client_df = pd.read_csv(f"{data_directory}/client.csv", sep=';')  # read and store the content of the "client" table
    # print(client_df.head())  # -> visualize table's fields
    # print(client_df.dtypes)  # -> visualize table's data-types

    # rename field "district_id" to "client_district_id"
    client_df = client_df.rename(columns={'district_id': 'client_district_id'})

    # clean the "client_age" field. First thing was to create a field called "client_age" and it's content was created
    # by extracting it from the "birth_number" field.
    client_df['client_birth_date'] = client_df['birth_number'].map(adjust_date)

    # clean the "client_age" field. First thing was to create a field called "client_age" and it's content was created
    # by extracting it from the "birth_number" field.
    client_df['client_gender'] = client_df['birth_number'].map(get_gender)  # clean the "client_gender" field

    # deleting the field "birth_number" from the table "client" because it is no longer useful. All the information was
    # extracted from it and placed in more clear fields.
    del client_df['birth_number']

    if save_changes:  # if specified, saves the changes made
        client_df.to_csv(f"{data_directory}/client.csv", sep=";")

    return client_df


# ------------------------------------- CLEANING: DISP TABLE -----------------------------------------------------------
def clean_disp_table(save_changes=False):
    disp_df = pd.read_csv(f"{data_directory}/disp.csv", sep=';')  # read and store the content of the "disp" table
    # print(disp_df.head())  # -> visualize table's fields
    # print(disp_df.dtypes)  # -> visualize table's data-types

    # rename field "disp_type"
    disp_df = disp_df.rename(columns={'type': 'disp_type'})
    # print(disp_df.head())  # -> visualize last update
    # print(disp_df['disp_type'].value_counts())

    if save_changes:  # if specified, saves the changes made
        disp_df.to_csv(f"{data_directory}/disp.csv", sep=";")

    return disp_df


# ------------------------------------- CLEANING: DISTRICT TABLE -------------------------------------------------------
def clean_district_table(save_changes=False):
    district_df = pd.read_csv(f"{data_directory}/district.csv", sep=';')  # read & store the content of "district" table
    # print(district_df.head())  # -> visualize table's fields
    # print(district_df.dtypes)  # -> visualize table's data-types

    # change every field to a more descriptive name
    district_df = district_df.rename(columns=
                                     {'A1': 'district_id',
                                      'A2': 'district_name',
                                      'A3': 'region',
                                      'A4': 'num_inhabitants',
                                      'A5': 'num_munipalities_gt499',
                                      'A6': 'num_munipalities_500to1999',
                                      'A7': 'num_munipalities_2000to9999',
                                      'A8': 'num_munipalities_gt10000',
                                      'A9': 'num_cities',
                                      'A10': 'ratio_urban',
                                      'A11': 'average_salary',
                                      'A12': 'unemp_rate95',
                                      'A13': 'unemp_rate96',
                                      'A14': 'num_entrep_per1000',
                                      'A15': 'num_crimes95',
                                      'A16': 'num_crimes96'
                                      }
                                     )
    # print(district_df.head())  # -> visualize last update

    # something wrong with unemp_rate95 and num_crimes95.
    # print(district_df['unemp_rate95'].value_counts()[50:100])  # -> partially visualize field to understand better
    # print(district_df['num_crimes95'].value_counts()[1:50])  # -> partially visualize field to understand better
    # clean data from field 'unemp_rate95'
    district_df['unemp_rate95'] = district_df['unemp_rate95'].apply(convert_question_marks, args=('float',))
    # clean data from field 'unemp_crimes95'
    district_df['num_crimes95'] = district_df['num_crimes95'].apply(convert_question_marks, args=('int',))
    # print(district_df.dtypes)  # -> visualize last update

    if save_changes:  # if specified, saves the changes made
        district_df.to_csv(f"{data_directory}/district.csv", sep=";")

    return district_df


# ------------------------------------- CLEANING: LOAN TABLE -----------------------------------------------------------
def clean_loan_table(save_changes=False):
    loan_df = pd.read_csv(f"{data_directory}/loan.csv", sep=';')  # read and store the content of the "loan" table
    # print(loan_df.head())  # -> visualize table's fields
    # print(loan_df.dtypes)  # -> visualize table's data-types

    # rename field "date" to (a more descriptive name) "loan_date_granted". Also converting its content
    loan_df['loan_date_granted'] = loan_df['date'].map(convert_int_to_date)
    del loan_df['date']  # deleting the (now) useless field "date"

    # convert loan status code to understandable string.
    loan_df['status'] = loan_df['status'].map(convert_status_code_to_meaning)
    # rename field "date" to (a more descriptive name) "loan_date". Also converting its content
    loan_df['loan_status'] = loan_df['status']
    del loan_df['status']  # deleting the (now) useless field "status"

    # change some field to a more descriptive name
    loan_df = loan_df.rename(columns={
        'amount': 'loan_amount',
        'duration': 'loan_duration',
        'payments': 'monthly_loan_payment',
    })
    # print(loan_df.head())  # -> visualize last update

    if save_changes:  # if specified, saves the changes made
        loan_df.to_csv(f"{data_directory}/loan.csv", sep=";")

    return loan_df


# ------------------------------------- CLEANING: ORDER TABLE ----------------------------------------------------------
def clean_order_table(save_changes=False):
    order_df = pd.read_csv(f"{data_directory}/order.csv", sep=';')  # read and store the content of the "order" table
    # print(order_df.head())  # -> visualize table's fields
    # print(order_df.dtypes)  # -> visualize table's data-types

    # print(order_df['k_symbol'].value_counts())  # get better understanding about the field "k_symbol"
    # convert data from field "k_symbol" & give it to new field "order_k_symbol"
    order_df['payment_characterization'] = order_df['k_symbol'].map(convert_k_symbol_to_eng)
    del order_df['k_symbol']  # deleting the (now) useless field "k_symbol"

    # rename the column names as per remarks
    order_df = order_df.rename(
        columns={'bank_to': 'recipient_bank',
                 'account_to': 'recipient_account',
                 'amount': 'debited_amount'
                 })
    # print(order_df.head())  # -> visualize last update

    if save_changes:  # if specified, saves the changes made
        order_df.to_csv(f"{data_directory}/order.csv", sep=";")


# ------------------------------------- CLEANING: TRANSACTION TABLE ----------------------------------------------------
def clean_transaction_table(save_changes=False):
    trans_df = pd.read_csv(f"{data_directory}/trans.csv", sep=';', low_memory=False)  # content of "transaction" table
    # print(trans_df.head())  # -> visualize table's fields
    # print(trans_df.dtypes)  # -> visualize table's data-types

    # print(trans_df['k_symbol'].value_counts())  # get better understanding about the field "k_symbol"
    trans_df['trans_k_symbol'] = trans_df['k_symbol'].map(convert_trans_k_symbol_to_eng)

    # convert data from field "type" & give it to new field "trans_type"
    trans_df['trans_type'] = trans_df['type'].map(convert_trans_type_to_eng)

    # convert data from field "operation" & give it to new field "trans_operation"
    trans_df['trans_operation'] = trans_df['operation'].map(convert_trans_op_to_eng)

    # convert data from field "date" to a more appropriate datatype to work with later
    trans_df['date'] = trans_df['date'].map(convert_int_to_date)
    # convert data from field "date" & give it to new field "trans_date"
    trans_df['trans_date'] = trans_df['date'].map(convert_date_to_days)

    # change some field to a more descriptive name
    trans_df = trans_df.rename(columns={
        'amount': 'trans_amount',
        'balance': 'balance_after_trans',
        'bank': 'trans_bank_partner',
        'account': 'trans_account_partner'})

    # deleting (now) useless fields from the table
    del trans_df['date']
    del trans_df['type']
    del trans_df['operation']
    del trans_df['k_symbol']

    if save_changes:  # if specified, saves the changes made
        trans_df.to_csv(f"{data_directory}/trans.csv", sep=";")

    return trans_df


# ------------------------------------- ALLOW TABLES TO BE IMPORTED SAFELY ---------------------------------------------
# returns the clean version of a specific file.
def get_clean_table(name):
    get_functions = {"account.csv": clean_account_table,
                     "card.csv": clean_card_table,
                     "client.csv": clean_client_table,
                     "disp.csv": clean_disp_table,
                     "district.csv": clean_district_table,
                     "loan.csv": clean_loan_table,
                     "order.csv": clean_order_table,
                     "trans.csv": clean_transaction_table
                     }
    try:
        table = get_functions[name]()
    except:
        table = pd.read_csv(f"{data_directory}/{name}")
    return table
