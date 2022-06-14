from time import sleep
import MySQLdb


# Making connection to database MySQL server
# maybe you need to change the host, user and password to get connection
def connect():
    """This function is responsible for connecting to server."""
    try:
        conn = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='123456'
        )
        return conn
    except MySQLdb.Error as e:
        print(f'Error to connect to MySQL Server: {e}')


def disconnect(conn):
    """This function just disconnect of the database server."""
    if conn:
        conn.close()


def main():
    return menu()


# Welcome to...
print(f"{'=' * 50}\n{' ' * 11} WELCOME TO PYTHON BANK!\n{'=' * 50}")

# creating database, all tables, collumns if not exist and adding fake data...
conn = connect()
cursor = conn.cursor()
cursor.execute(
    "CREATE DATABASE IF NOT EXISTS bank;USE bank;"
    "CREATE TABLE IF NOT EXISTS clients (id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, clientname VARCHAR(100) NOT NULL, passwordkey VARCHAR(6) NOT NULL,"
    "email VARCHAR(45) NOT NULL, identification VARCHAR(11) NOT NULL, birth VARCHAR(10) NOT NULL);"
    "INSERT INTO clients (clientname, passwordkey, email, identification, birth) VALUES ('Jhon', '123456', 'jhon@hotmail.com', '12345678999', '01/01/1995');"
    "INSERT INTO clients (clientname, passwordkey, email, identification, birth) VALUES ('Alex', '457895', 'alex@hotmail.com', '45678912398', '03/02/1990');"
    "INSERT INTO clients (clientname, passwordkey, email, identification, birth) VALUES ('Kity', '123546', 'kity@gmail.com', '87598521366', '10/28/1997');"
    "INSERT INTO clients (clientname, passwordkey, email, identification, birth) VALUES ('Tommy', '147258', 'tommy@gmail.com', '14785236989', '11/15/1985');"
    "CREATE TABLE IF NOT EXISTS accounts (id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, cash DECIMAL(20,2) NOT NULL, credit DECIMAL(20,2) NOT NULL,  clients_id INT NOT NULL);"
    f"INSERT INTO accounts (cash, credit, clients_id) VALUES ({100.0}, {100.0}, {1});" 
    f"INSERT INTO accounts (cash, credit, clients_id) VALUES ({100.0}, {100.0}, {2});" 
    f"INSERT INTO accounts (cash, credit, clients_id) VALUES ({100.0}, {100.0}, {3});" 
    f"INSERT INTO accounts (cash, credit, clients_id) VALUES ({100.0}, {100.0}, {4});"
    "ALTER TABLE accounts ADD FOREIGN KEY (clients_id) REFERENCES clients (id);"
)


def menu():
    '''This function shows all options available and do what was chosen'''
    print('1 - Check cash available\n'
          '2 - Create an account\n'
          '3 - Make withdraw\n'
          '4 - Make deposit\n'
          '5 - Transfer money.\n'
          '6 - Show all accounts\n'
          '7 - Search an account for ID\n'
          '0 - Exit')

    objective = int(input('Choose one from options above: '))

    if objective == 1:
        check_cash_available()

    elif objective == 2:
        create_account()

    elif objective == 3:
        make_withdraw()

    elif objective == 4:
        make_deposit()

    elif objective == 5:
        transfer_money()

    elif objective == 6:
        show_accounts()

    elif objective == 7:
        search_account()

    elif objective == 0:
        sleep(1)
        print('\nSee you soon!\n')
        sleep(1)
    else:
        sleep(1)
        print('\nType a valid option!\n')
        sleep(1)
        menu()


def check_cash_available():
    '''This function shows amount of cash and credit available in your account.'''
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('USE bank;')

    code = int(input('Inform your account ID: '))
    password = input('Type your password: ')
    cursor.execute(f'SELECT clientname, passwordkey FROM clients WHERE id = {code};')
    clientname_passwordkey = cursor.fetchall()
    if password == clientname_passwordkey[0][1]:
        sleep(1)
        print(f'Welcome, {(clientname_passwordkey[0][0].split(" ")[0])}!')
        cursor.execute(f'SELECT cash, credit FROM accounts WHERE clients_id = {code};')
        balance = cursor.fetchall()
        sleep(2)
        print(f'Current balance in account: $ {balance[0][0]}\n'
              f'Credit available: $ {balance[0][1]}\n')
        sleep(2)
        menu()
    else:
        print('Invalid password!')
        sleep(2)
        menu()


def create_account():
    '''This function is responsible for creating an account'''
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('USE bank;')

    name = input("What's your name? ")
    password = input('Type a password (6 digits): ')
    email = input('Type your email: ')
    identification = input('Informe your SIN number (identification): ')
    birth = input('Date of birth (mm/dd/aaaa):  ')
    cursor.execute("SET foreign_key_checks = 0;")  # It will force data import

    credit = 100.00
    cash = 0.00
    cursor.execute(f'INSERT INTO clients (clientname, passwordkey, email, identification, birth) VALUES ("{name.title()}", "{password}", "{email}", "{identification}", "{birth}");')

    cursor.execute(f'SELECT id FROM clients WHERE identification = {identification};')
    get_id = cursor.fetchall()
    cursor.execute(f'INSERT INTO accounts (cash, credit, clients_id) VALUES ("{cash}", "{credit}", {get_id[0][0]});')
    conn.commit()

    if cursor.rowcount > 1:
        print(f'{name.title()}, your account was created sucessfully!\n'
              f'Current balance account: $ {cash}\n'
              f'Credit: $ {credit}')
    sleep(1)
    print('\nAccount was created sucessfully!')
    sleep(1)
    menu()


def make_withdraw():
    '''This function makes withdraws if you want to take some money'''
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('USE bank;')

    code = int(input('Type your account ID: '))

    cursor.execute(f'SELECT cash, credit FROM accounts WHERE clients_id = {code};')
    cash_credit = cursor.fetchall()

    if len(cash_credit) > 0:

        password = input('Type your password: ')
        cursor.execute(f'SELECT clientname, passwordkey FROM clients WHERE id = {code};')
        clientname_password = cursor.fetchall()

        # checking password
        if clientname_password[0][1] == password:

            print(f'Welcome, {clientname_password[0][0].split(" ")[0]}!')
            sleep(1)

            print(f'Current balance account: $ {float(cash_credit[0][0])}\n'
                  f'Current credit: $ {float(cash_credit[0][1])}\n')
            value = input('Type the value of withdraw: $ ')

            # verifying if the balance account is bigger than or equal the value of withdraw
            if float(cash_credit[0][0]) >= float(value):

                cursor.execute(f'UPDATE accounts SET cash = "{float(cash_credit[0][0]) - float(value)}" WHERE clients_id = {code};')
                conn.commit()

                cursor.execute(f'SELECT cash, credit FROM accounts WHERE clients_id = {code};')
                cash_after = cursor.fetchall()

                print(f'{clientname_password[0][0].split(" ")[0]}, You made a withdraw of $ {value} from your account!\n'
                      f'Current account balance: $ {cash_after[0][0]}')
                sleep(2)
                menu()

            # if the value of withdraw is bigger than balance account, using the credit:
            elif float(value) > float(cash_credit[0][0]):

                print('Value of withdraw is bigger than current balance account.\n'
                      '1 - Yes\n'
                      '2 - No')

                objective = int(input('Want to use credit? '))

                # if want use credit
                if objective == 1:

                    # total value able for withdraw (cash + credit)
                    total_value = float(cash_credit[0][0]) + float(cash_credit[0][1])

                    print(f'Current account balance: $ {cash_credit[0][0]}\n'
                          f'Current credit: $ {cash_credit[0][1]}\n'
                          f'Total value able for withdraws: $ {total_value}\n')

                    # checking if the value of withdraws is less than or equals to total value available (cash + credit)
                    if float(value) <= total_value:

                        # value to use from credit after balance = 0
                        remaining_value = float(value) - float(cash_credit[0][0])
                        cursor.execute(
                            f'UPDATE accounts SET cash = 0, credit = "{abs(float(cash_credit[0][1])) - abs(remaining_value)}" WHERE clients_id = {code};')
                        conn.commit()

                        cursor.execute(f'SELECT cash, credit FROM accounts WHERE clients_id = {code};')
                        new_cash_credit = cursor.fetchall()

                        print(f'You made a withdraw of R$ {float(value)}\n'
                              f'Current balance account: $ {new_cash_credit[0][0]}\n'
                              f'Current credit: $ {new_cash_credit[0][1]}\n')
                        sleep(2)
                        menu()

                    # if the withdraw value is bigger than the total value available (cash + credit)
                    else:
                        print("Error: Withdraw's value must be less than or equals to total value available (cash + credit)")
                        sleep(2)
                        menu()

                # if won't use credit
                elif objective == 2:
                    print("Ok, You don't want to use your credit.")
                    sleep(2)
                    menu()

                else:
                    print('Invalid option!')
                    sleep(2)
                    menu()

            else:
                cursor.execute(f'SELECT credit FROM accounts WHERE clients_id = {code};')
                credit = cursor.fetchall()

                print(f'Total balance account is unable to make withdraws.\n'
                      f'Current balance account: $ {cash_credit[0][0]}\n'
                      f'Current credit: $ {credit[0][0]}\n')
                menu()

        else:
            print('Incorrect password!')
            sleep(2)
            menu()
    else:
        print("There isn't account to link with this ID.")
        sleep(2)
        menu()


def make_deposit():
    '''This function makes deposit in some account that you want'''
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('USE bank;')

    code = int(input('Type account ID for deposit: '))
    cursor.execute(f'SELECT cash FROM accounts WHERE clients_id = {code};')
    cash = cursor.fetchall()

    cursor.execute(f'SELECT clientname FROM clients WHERE id = {code};')
    name = cursor.fetchall()

    if len(name) > 0:
        value = input('Type the value of the withdraw\n'
                      '$: ')
        if value == 0.00:
            print('Value of withdraw must be bigger than $ 0,00')
            menu()
        else:
            cursor.execute(
                f'UPDATE accounts SET cash = "{float(cash[0][0]) + float(value)}" WHERE clients_id = {code};')
            conn.commit()
            print(f'{name[0][0]}, you received a deposit of $ {value}')
            menu()
    else:
        print(f'Error: account ID does not exists. ({code})')
        sleep(2)
        menu()


def transfer_money():
    '''This function sends money from your account to another one'''
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('USE bank;')

    code_from = int(input('Enter source account ID: ')) # ID code from the account that the money is gonna out

    cursor.execute(f'SELECT passwordkey FROM clients WHERE id = {code_from};')
    password = cursor.fetchall()

    check_password = input('Type your password: ')

    # verifying password
    if check_password == password[0][0]:

        destination_code = int(input('Enter destination account ID: ')) # account's id will receives the money
        cursor.execute(f'SELECT clientname FROM clients WHERE id = {code_from};')
        source_client = cursor.fetchall()

        cursor.execute(f'SELECT cash FROM accounts WHERE clients_id = {code_from};')
        cash_from = cursor.fetchall() # account's cash that the money will departure

        print(f'{source_client[0][0]}, your account balance is $ {cash_from[0][0]}')
        value = input('Enter the amount to transfer\n'
                      '$: ')

        # checking ir the amount to transfer is less than or equals to the balance
        if float(value) <= float(cash_from[0][0]):

            cursor.execute(f'SELECT id FROM clients WHERE id = {destination_code};')
            id_destination = cursor.fetchall()

            if len(id_destination) > 0:

                print('Destination account found!')

                cursor.execute(f'SELECT clientname FROM clients WHERE id = {destination_code};')
                destination_client = cursor.fetchall()

                cursor.execute(f'SELECT cash FROM accounts WHERE clients_id = {destination_code};')
                destination_balance = cursor.fetchall()

                print(cursor.execute(f'SELECT id, clientname FROM clients WHERE id = {destination_code};'))

                cursor.execute(f'UPDATE accounts SET cash = "{float(cash_from[0][0]) - float(value)}" WHERE clients_id = {code_from};')
                print(f'Sending $ {value} from {source_client[0][0]} to {destination_client[0][0]}')

                sleep(2)
                cursor.execute(f'UPDATE accounts SET cash = "{float(destination_balance[0][0]) + float(value)}" WHERE clients_id = {destination_code};')
                conn.commit()
                print('Transaction completed successfully!')
                sleep(1)
                print(f'{destination_client[0][0]}, you received $ {value}!')
                menu()
            else:
                print(f"Error to find destination account: ID {id_destination[0][0]} doesn't exists.")
                menu()

        # in case of value is bigger than the balance from source account, use the credit
        else:
            print('Amount requested to transfer is bigger than the current account balance.\n')

            option = int(input('Want to use the credit? (1-Yes or 2-No): '))

            # in case want to use credit
            if option == 1:

                cursor.execute(f'SELECT credit FROM accounts WHERE clients_id = {code_from};')
                credit = cursor.fetchall()

                cursor.execute(f'SELECT cash FROM accounts WHERE clients_id = {code_from};')
                cash = cursor.fetchall()

                # total value available (cash + credit)
                total_value = float(cash[0][0]) + float(credit[0][0])

                print(f'Current account balance: $ {cash[0][0]}\n'
                      f'Credit: $ {credit[0][0]}\n'
                      f'Total value able to transfer: $ {total_value}\n')

                # checking if the amount requested is less than or equals to the total value able (cash + credit)
                if float(value) <= total_value:

                    cursor.execute(f'SELECT clientname FROM clients WHERE id = {destination_code};')
                    destination_client = cursor.fetchall()

                    # credit able to use after cash = 0
                    value_remaining = float(value) - float(cash[0][0])
                    cursor.execute(f'UPDATE accounts SET cash = 0, credit = "{abs(float(credit[0][0])) - abs(value_remaining)}" WHERE clients_id = {code_from};')

                    print(f'Sending R$ {float(value)} from {source_client[0][0]} to {destination_client[0][0]}')

                    cursor.execute(f'UPDATE accounts SET cash = {float(cash[0][0]) + float(value)} WHERE clients_id = {destination_code};')
                    sleep(2)

                    print('Transaction completed successfully!')
                    conn.commit()

                    sleep(2)
                    menu()

                # if the value requested is bigger than or equals to total value able (cash + credit)
                else:
                    print('Error: Transaction value must be less than or equals to total value available (cash + credit)')
                    sleep(2)
                    menu()

            # if don't want to use the credit
            elif option == 2:
                print("Ok, you don't want to use the credit.")
                sleep(2)
                menu()

            else:
                print('Invalid option!')
                sleep(2)
                menu()
    else:
        print('Incorrect password!')
        sleep(2)
        menu()


def show_accounts():
    '''This function shows all accounts in the database'''
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('USE bank;')

    cursor.execute(f'SELECT id, clientname FROM clients;')
    clients = cursor.fetchall()  # The fetchall() put all data in a list

    if len(clients) > 0:
        print('Searching for accounts...')
        sleep(2)

        for client in clients:
            print(f'ID: {client[0]}\n'
                  f'Name: {client[1]}\n')
            print('-' * 20)
            sleep(1)
    else:
        print('The list of accounts is empty!')
    menu()


def search_account():
    '''This function search an account for ID'''
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('USE bank;')

    code = int(input('Type the account ID for search: '))
    cursor.execute(f'SELECT id, clientname FROM clients WHERE id = {code};')
    account = cursor.fetchall()

    if len(account) > 0:
        print('We found an account!')
        sleep(1)
        print('-' * 20)
        print(f'ID: {account[0][0]}\n'
              f'Name: {account[0][1]}')
        print('-' * 20)
        sleep(2)
        menu()
    else:
        print(f'Error: account ID does not exists. ({code})\n')
        sleep(2)
        menu()


if __name__ == '__main__':
    menu()

