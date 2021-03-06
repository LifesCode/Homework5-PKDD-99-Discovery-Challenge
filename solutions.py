import math
import db_cleaning as dbc
# import ml_functions as mlf


#  -------------------------- CHALLENGE 1-1: Cleaning and treatment of the data ----------------------------------------
help_content_ch1_ex1 = "------------------------ Challenge 1 Exercise 1 ------------------------\n" \
                       "-> Task: Clean the Database\n"\

def clean_database():
    try:
        dbc.clean_account_table(save_changes=True)
        dbc.clean_card_table(save_changes=True)
        dbc.clean_client_table(save_changes=True)
        dbc.clean_disp_table(save_changes=True)
        dbc.clean_district_table(save_changes=True)
        dbc.clean_loan_table(save_changes=True)
        dbc.clean_order_table(save_changes=True)
        dbc.clean_transaction_table(save_changes=True)
    except KeyError:
        print("Database was already clean")


#  -------------------------- CHALLENGE 1-2: Define a problem to help the bank improve his services --------------------
help_content_ch1_ex2 = "------------------------ Challenge 1 Exercise 2 ------------------------" \
                       "Task: define a problem to improve the bank's services"\

def define_problem_to_help_bank_improve():
    solution_definition = "\n-> Basic Idea: Definition of a good client based on loan records\n"\
                          "\n-> Details: A good metric for finding out if a client is good or bad is by\n" \
                          "analysing his loan record. More specifically: analysing his loan status and amount.\n" \
                          "If a client has a record of paying his loans, and the amount of the loan is considerable\n" \
                          "than the client is a good client. If he has a record of not paying his loans and the\n" \
                          "amount is not considerable, than he is a bad client\n"
    print(solution_definition)


#  -------------------------- CHALLENGE 1-3: Show how ML could be used to solve the Defined Problem --------------------
help_content_ch1_ex3 = "------------------------ Challenge 1 Exercise 3 ------------------------" \
                       "Task: Show how Machine Learning can be used to solve this problem"\

def problem_solution():
    solution_definition = "\n-> Basic Idea: Using a mathematical definition of a good client as desired output\n"\
                          "and predict it based on specific information about the client\n" \
                          "\n-> Details: \n" \
                          "\tFIRST: We create a field for every client. This field will contain\n" \
                          "a value proportional to how good of a client he is for the bank. This value will be\n" \
                          "calculated like it was defined in the problem: Based on the size of his loans and how\n"\
                          "well he pays them. Mathematically: G = A*L\n" \
                          "\t -> G: It defines how good a client is. The higher the value, the better a client is;\n" \
                          "\t -> A: Average Amount of the loan he asked to the bank. Directly proportional to |G|;\n" \
                          "\t -> L: Average Loan status of the client. Goes in a range from [-1; 1].\n" \
                          "\t -> Meaning of the Formula: The BEST client is defined as the one that loans the \n" \
                          "\t    greatest amount of money, and has a record of paying all his loans.\n"\
                          "\t    The exact opposite is the definition of the WORST client.\n" \
                          "\t    This way, a good client is when G > 0. A bad client is when G <= 0\n" \
                          "\tSECOND: Choose what information about a client to use in order to predict G.\n" \
                          "-> Where he lives (found in 'district'); -> Age (found in 'client');\n" \
                          "->type of Credit card (found in 'card')\n" \
                          "\tTHIRD: Choose a MACHINE LEARNING Model/Algorithm to use (based on the type of\n" \
                          "INPUT defined in the SECOND section and the type of OUTPUT defined in the FIRST section\n" \
                          "A good choice would be to use a CLASSIFICATION algorithm like K-NN\n" \
                          "\tFORTH: Train the model."\
                          "\n-> How would it help: At this point, if the model gets an acceptable accuracy, we have\n" \
                          "a model that can predict the value which defines how good a client is. With this value,\n" \
                          "it is easier to find out what client to offer different kinds of services that could not\n" \
                          "be offered to a bad client. G also defines who is more likely to be trusted with a loan.\n" \
                          "\n"
    print(solution_definition)


#  -------------------------- CHALLENGE 2-1: Predict The Average Credit/Bank Account -----------------------------------
help_content_ch2_ex1 = "------------------------ Challenge 2 Exercise 1 ------------------------" \
                       "Task: Predict the average amount of money for an account"\

def predict_average_credit():

    def reseting_nan_value(value) -> float:
        if math.isnan(value):
            return 0.0
        return value

    trans_df = dbc.get_clean_table("trans.csv")
    dict_predictions = {}

    for total_trns, blc_after_trns, trans_date, account_id in zip(trans_df["trans_account_partner"], \
        trans_df["balance_after_trans"], trans_df["trans_date"], trans_df["account_id"]):
        year = trans_date.split("-")[0]
        if year not in dict_predictions:
            dict_predictions[year] = [1, 0, []]

        dict_predictions[year][0] += 1
        dict_predictions[year][1] += (reseting_nan_value(total_trns) + reseting_nan_value(blc_after_trns))
        if account_id not in dict_predictions[year][2]:
            dict_predictions[year][2].append(account_id)
    
    print(" \nPredictions of the total ammount per partner in a year: \n")
    [print(f"  - {elem[0]} -> Prediction: {(elem[1][1])/sum(elem[1][2]) / 365}") \
        for elem in dict_predictions.items()]
    print("\n")
    # print(dict_predictions)

#  -------------------------- CHALLENGE 2-2-1: You Could Also ----------------------------------------------------------
help_content_ch2_ex2_l1 = "------------------------ Challenge 2 Exercise 2 Line 1 ------------------" \
                          "Task: Show which clients have credit cards"\

# Returns a list of all the clients with a credit card
def which_client_has_credit_card():
    card_df = dbc.get_clean_table("card.csv")
    disp_df = dbc.get_clean_table("disp.csv")
    clients_w_credit_card = []
    for disp_id, client_id in zip(disp_df["disp_id"], disp_df["client_id"]):
        if disp_id in card_df["disp_id"]:
            clients_w_credit_card.append(client_id)
    print(f"Clients with Credit Card:\nClients IDs:{clients_w_credit_card}\n"
          f"Number of clients with Credit Card: {len(clients_w_credit_card)}")


#  -------------------------- CHALLENGE 2-2-2: You Could Also ----------------------------------------------------------
help_content_ch2_ex2_l2 = "------------------------ Challenge 2 Exercise 2 Line 2 ------------------" \
                          "Task: Show which clients asked the bank for loans"\

# Returns a list of all the clients who asked for a loan
def who_asked_for_loans():
    # Step one is to get all the IDs of the accounts in the  table "loan"
    loan_df = dbc.get_clean_table("loan.csv")
    accounts_id = set([account_id for account_id in loan_df["account_id"]])

    # Step two is to get, for every account with a loan, the corresponding clients
    disp_df = dbc.get_clean_table("disp.csv")
    clients_w_loans = []
    for account, client in zip(disp_df["account_id"], disp_df["client_id"]):
        if account in accounts_id and client not in clients_w_loans:
            clients_w_loans.append(client)

    print(f"Clients with Loans:\nClients IDs:{clients_w_loans}\nNumber of clients with loans: {len(clients_w_loans)}")


#  -------------------------- CHALLENGE 2-2-3: You Could Also ----------------------------------------------------------
help_content_ch2_ex2_l3 = "------------------------ Challenge 2 Exercise 2 Line 3 ------------------" \
                          "Task: Show which clients are minors"\

# Returns a list of all the clients who are minors (have an age < 18 years old)
def minor_clients():
    client_df = dbc.get_clean_table("client.csv")
    clients_age = client_df['client_birth_date'].map(dbc.convert_birthday_to_age)
    minor_clients_id = [cli_id for cli_id, cli_age in zip(client_df['client_id'], clients_age) if cli_age<18]
    minor_clients_number = len(minor_clients_id)
    print(f"-> Minor clients ID: {minor_clients_id}\n->Number of Minor Clients: {minor_clients_number}")


#  -------------------------- CHALLENGE 2-2-4: You Could Also ----------------------------------------------------------
help_content_ch2_ex2_l4 = "------------------------ Challenge 2 Exercise 2 Line 4 ------------------" \
                          "Task: Show, for each sex, the number of clients"\

# Returns a tuple with 2 values which ate the Total Number of: 1->  Male clients; 2-> Female clients.
def number_of_clients_for_sex():
    client_df = dbc.get_clean_table("client.csv")
    clients_gender_count = client_df['client_gender'].value_counts()
    print(f"Male Clients: {clients_gender_count[0]}\nFemale Clients: {clients_gender_count[1]}")


#  -------------------------- CHALLENGE 2-2-5: You Could Also ----------------------------------------------------------
help_content_ch2_ex2_l5 = "------------------------ Challenge 2 Exercise 2 Line 5 ------------------" \
                          "Task: Show the types of credit cards the bank offers"\

# Returns a list of all the types of cards offered by the bank
def types_of_cards():
    card_df = dbc.get_clean_table("card.csv")
    card_types = set(card_df['card_type'])
    print(f"Types of Cards: {card_types}")


# --------------------------- EXERCISE CREATION ------------------------------------------------------------------------
# Generic Class representing an Exercise.
# The attribute "solve" receives a callable (function) which implements the solution of the respective exercise
# The attribute "help_content" receives a list of strings. Each string is a line of the explanation of the exercise
# The function  "help" prints all the help_content
class Exercise:
    def __init__(self, solving_function, help_content):
        self.solve = solving_function
        self.help_content = help_content

    def help(self):
        print(self.help_content)


def ch1_ex1():
    return Exercise(clean_database, help_content_ch1_ex1)

def ch1_ex2():
    return Exercise(define_problem_to_help_bank_improve, help_content_ch1_ex2)

def ch1_ex3():
    return Exercise(problem_solution, help_content_ch1_ex3)

def ch2_ex1():
    return Exercise(predict_average_credit, help_content_ch2_ex1)

def ch2_ex2_l1():
    return Exercise(which_client_has_credit_card, help_content_ch2_ex2_l1)

def ch2_ex2_l2():
    return Exercise(who_asked_for_loans, help_content_ch2_ex2_l2)

def ch2_ex2_l3():
    return Exercise(minor_clients, help_content_ch2_ex2_l3)

def ch2_ex2_l4():
    return Exercise(number_of_clients_for_sex, help_content_ch2_ex2_l4)

def ch2_ex2_l5():
    return Exercise(types_of_cards, help_content_ch2_ex2_l5)

def invalid_exercise():
    invalid_text = "--------------- Error: Invalid Exercise Name -------------------"

    def print_invalid():
        print(invalid_text)
    return Exercise(print_invalid, invalid_text)
