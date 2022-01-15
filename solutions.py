import db_cleaning as dbc
# import ml_functions as mlf


#  -------------------------- CHALLENGE 1-1: Cleaning and treatment of the data ----------------------------------------
help_content_ch1_ex1 = "------------------------ Challenge 1 Exercise 1 ------------------------" \
                       ""\


def clean_database():
    dbc.clean_account_table(save_changes=True)
    dbc.clean_card_table(save_changes=True)
    dbc.clean_client_table(save_changes=True)
    dbc.clean_disp_table(save_changes=True)
    dbc.clean_district_table(save_changes=True)
    dbc.clean_loan_table(save_changes=True)
    dbc.clean_order_table(save_changes=True)
    dbc.clean_transaction_table(save_changes=True)


#  -------------------------- CHALLENGE 1-2: Define a problem to help the bank improve his services --------------------
help_content_ch1_ex2 = "------------------------ Challenge 1 Exercise 2 ------------------------" \
                       ""\

def define_problem_to_help_bank_improve():
    pass


#  -------------------------- CHALLENGE 1-3: Show how ML could be used to solve the Defined Problem --------------------
help_content_ch1_ex3 = "------------------------ Challenge 1 Exercise 3 ------------------------" \
                       ""\


def problem_solution():
    pass


#  -------------------------- CHALLENGE 2-1: Predict The Average Credit/Bank Account -----------------------------------
help_content_ch2_ex1 = "------------------------ Challenge 2 Exercise 1 ------------------------" \
                       ""\


def predict_average_credit():
    pass


#  -------------------------- CHALLENGE 2-2-1: You Could Also ----------------------------------------------------------
help_content_ch2_ex2_l1 = "------------------------ Challenge 2 Exercise 2 Line 1 ------------------" \
                          ""\


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
                          ""\


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
                          ""\


# Returns a list of all the clients who are minors (have an age < 18 years old)
def minor_clients():
    client_df = dbc.get_clean_table("client.csv")
    minor_clients_id = [client_id for client_id, client_age in zip(client_df['client_id'], client_df['client_age'])
                        if client_age < 18]
    minor_clients_number = len(minor_clients_id)
    print(f"-> Minor clients ID: {minor_clients_id}\n->Number of Minor Clients: {minor_clients_number}")


#  -------------------------- CHALLENGE 2-2-4: You Could Also ----------------------------------------------------------
help_content_ch2_ex2_l4 = "------------------------ Challenge 2 Exercise 2 Line 4 ------------------" \
                          ""\


# Returns a tuple with 2 values which ate the Total Number of: 1->  Male clients; 2-> Female clients.
def number_of_clients_for_sex():
    client_df = dbc.get_clean_table("client.csv")
    clients_gender_count = client_df['client_gender'].value_counts()
    print(f"Male Clients: {clients_gender_count[0]}\nFemale Clients: {clients_gender_count[1]}")


#  -------------------------- CHALLENGE 2-2-5: You Could Also ----------------------------------------------------------
help_content_ch2_ex2_l5 = "------------------------ Challenge 2 Exercise 2 Line 5 ------------------" \
                          ""\


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
