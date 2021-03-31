import sqlite3
import random
import itertools
import sys

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''create table if not exists card
            (id INTEGER,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0)''')

conn.commit()


class CardAnatomy:
    option_list = [1, 2, 0]
    card_no_list = []
    card_no = 0
    PIN = 0

    def __init__(self):
        self.IIN = 400000
        self.card_no = 0
        self.PIN = 0

    def unique_cust(self):

        random.seed

        cust_acct_no = str(random.randrange(99999999, 999999999, 9))
        random.seed
        yield ''.join(cust_acct_no)

    def choose_option(self):

        self.IIN = 400000
        check_accountno = []
        final_acct_no = []
        sum_acctno = 0
        checksum = 0

        for account_no in CardAnatomy.unique_cust(self):

            self.card_no = list(str(self.IIN) + str(account_no))

            for i in range(0, len(self.card_no)):
                if (i % 2) == 0:
                    check_accountno.append(int(self.card_no[i]) * 2)
                    i += 1
                else:
                    check_accountno.append(int(self.card_no[i]))
                    i += 1

            for i in range(0, len(check_accountno)):
                if (check_accountno[i] > 9):
                    final_acct_no.append(check_accountno[i] - 9)
                    i += 1
                else:
                    final_acct_no.append(check_accountno[i])
                    i += 1

            for i in range(0, len(final_acct_no)):
                sum_acctno += final_acct_no[i]
                i += 1

                # if sum_acctno % 10 > 0:
                # checksum = 10 - (sum_acctno % 10)
            checksum = (sum_acctno * 9) % 10
            # else:
            # checksum = 0

            card_no = ''.join(list(str(self.IIN) + str(account_no) + str(checksum)))

            # pin_first = random.choice('0123456789')
            # pin_second = random.choice('0123456789')
            # pin_third = random.choice('0123456789')
            # pin_four = random.choice('0123456789')
            random.seed
            self.PIN = '{:04d}'.format(random.randint(1111, 9999))
            # PIN = pin_first + pin_second + pin_third + pin_four

            print('''
1. Create an account
2. Log into account
0. Exit
            ''')
            while True:
                option = int(input())

                if option == 2:
                    print("Enter your card number:")
                    c_no = input()
                    print("Enter your PIN:")
                    pin = input()
                    cur.execute('select number from card where pin =' + pin)
                    card_number = cur.fetchone()

                    cur.execute('select pin from card where number =' + c_no)
                    card_pin = cur.fetchone()

                    if card_number != None and card_pin != None:

                        print("""You have successfully logged in!

1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
                        while True:
                            option1 = int(sys.stdin.readline())
                            if option1 == 1:
                                cur.execute('select balance from card where number =' + c_no)
                                balance = ''.join(map(str, cur.fetchone()))
                                print("Balance: " + str(balance))
                            elif option1 == 2:
                                print('Enter income:')
                                balance = int(input())
                                sql = """update card set balance = balance + ? where number = ?"""
                                val = (balance, c_no)
                                cur.execute(sql, val)
                                print('Income was added!')
                                conn.commit()

                            elif option1 == 3:
                                check_accountno = []
                                final_acct_no = []
                                sum_acctno = 0
                                checksum = 0

                                print("Transfer")
                                print("Enter card number:")
                                trans_no = input()

                                trans_list = [d for d in str(trans_no)]

                                transfer_acct_no = trans_list[6:len(trans_list) - 1]

                                trans_acct_no = ''.join(i for i in transfer_acct_no)

                                card_no = list(str(self.IIN) + str(trans_acct_no))

                                for i in range(0, len(card_no)):
                                    if (i % 2) == 0:
                                        check_accountno.append(int(card_no[i]) * 2)
                                        i += 1
                                    else:
                                        check_accountno.append(int(card_no[i]))
                                        i += 1

                                for i in range(0, len(check_accountno)):
                                    if (check_accountno[i] > 9):
                                        final_acct_no.append(check_accountno[i] - 9)
                                        i += 1
                                    else:
                                        final_acct_no.append(check_accountno[i])
                                        i += 1

                                for i in range(0, len(final_acct_no)):
                                    sum_acctno += final_acct_no[i]
                                    i += 1

                                checksum = (sum_acctno * 9) % 10

                                card_no = ''.join(list(str(self.IIN) + str(trans_acct_no) + str(checksum)))

                                # check whether no. presesnt in db or not
                                cur.execute('select * from card where number=' + card_no)
                                card_num = cur.fetchone()
                                if card_no != trans_no:
                                    print("Probably you made a mistake in the card number. Please try again!")
                                if card_no == c_no:
                                    print("You can't transfer money to the same account!")

                                elif card_num != None:
                                    print("Enter how much money you want to transfer:")
                                    trans_money = int(input())
                                    cur.execute('select balance from card where number =' + c_no)
                                    balance = ''.join(map(str, cur.fetchone()))
                                    # balance = cur.fetchone()
                                    if int(balance) < trans_money:
                                        print("Not enough money!")
                                    else:
                                        sql = """update card set balance = balance - ? where number = ?"""
                                        val = (trans_money, c_no)
                                        cur.execute(sql, val)
                                        sql = """update card set balance = balance + ? where number = ?"""
                                        val = (trans_money, card_no)
                                        cur.execute(sql, val)

                                        print('Success!')
                                        conn.commit()

                                elif card_num == None:
                                    print("Such a card does not exist.")




                            elif option1 == 4:
                                cur.execute("delete from card where number =" + c_no)
                                print("The account has been closed!")
                                conn.commit()
                                CardAnatomy.choose_option(self)



                            elif option1 == 5:
                                print("You have successfully logged out!")
                                CardAnatomy.choose_option(self)
                                cur.close()
                                conn.close()
                            elif option1 == 0:
                                exit()
                                print("Bye!")
                    else:
                        print("Wrong card number or PIN!")
                        CardAnatomy.choose_option(self)

                elif option == 0:
                    exit()
                    print("Bye!")

                elif option == 1:

                    cur.execute('select number from card')
                    card_num = cur.fetchall()

                    # res_num = [''.join(i) for i in card_num]
                    # print(res_num)
                    if card_no in card_num:
                        CardAnatomy.choose_option(self)
                    else:
                        cur.execute('insert into card (number,pin) values({} ,{})'.format(card_no, self.PIN))

                        print('''
Your card has been created                      
Your card number:
{}
Your card PIN:
{}'''.format(int(card_no), int(self.PIN)))

                        conn.commit()
                        CardAnatomy.choose_option(self)
                    # else:
                    # print('Account no is already in a system')
                    # CardAnatomy.unique_cust(self)


a = CardAnatomy()
a.choose_option()