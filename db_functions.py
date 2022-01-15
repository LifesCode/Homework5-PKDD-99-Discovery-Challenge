import csv

"""-dizer quais os clientes possui cartões de crédito
-quem pediu empréstimos ao banco
-clientes menores de idade
- numero de clientes por sexo
- os tipos de cartão o banco oferece."""


# reads a csv file based his name and returns (fields, content, content_size)
def read_csv_file(file_name) -> ([], []):
    with open(f"PKDD'99-Dataset/{file_name}", 'r') as csv_file:
        csv_reader = csv.reader(csv_file)  # creating a csv reader object
        fields = next(csv_reader)  # extracting field names through first row
        rows = [row for row in csv_reader]  # extracting each data row one by one
        #  get total number of rows
        #  print("Total no. of rows: %d" % (csv_reader.line_num))
    return fields, rows, csv_reader.line_num-1


