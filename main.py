import json
import os
from datetime import datetime

file_name = "bank_data.json"


def get_data():
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return {}


def save(data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=2)

class BankATM:

    def __init__(self):
        self.data = get_data()
        self.user = ""

    def create_account(self):

        print("\nCreate New Account")

        name = input("Enter username : ")

        if name in self.data:
            print("User already exists")
            return

        pin = input("Create 4 digit pin : ")

        if len(pin) != 4:
            print("Pin should be 4 digits")
            return

        self.data[name] = {
            "pin": pin,
            "money": 0,
            "history": []
        }

        save(self.data)

        print("Account created")

    def login(self):

        print("\nLogin Page")

        name = input("Username : ")

        if name not in self.data:
            print("No user found")
            return

        count = 3

        while count > 0:

            pin = input("Pin : ")

            if pin == self.data[name]["pin"]:

                print("Login success")
                self.user = name
                self.dashboard()
                break

            else:
                count -= 1
                print("Wrong pin")
                print("Attempts left :", count)

        if count == 0:
            print("Too many wrong attempts")

    def dashboard(self):

        while True:

            print("\n===== ATM MENU =====")
            print("1.Check Balance")
            print("2.Deposit")
            print("3.Withdraw")
            print("4.Transfer")
            print("5.History")
            print("6.Change Pin")
            print("7.Logout")

            ch = input("Enter choice : ")

            if ch == "1":
                self.balance()

            elif ch == "2":
                self.deposit_money()

            elif ch == "3":
                self.withdraw_money()

            elif ch == "4":
                self.send_money()

            elif ch == "5":
                self.history()

            elif ch == "6":
                self.change_pin()

            elif ch == "7":
                print("Logged out")
                self.user = ""
                break

            else:
                print("Invalid option")

    def balance(self):

        amt = self.data[self.user]["money"]

        print("Available Balance :", amt)

    def deposit_money(self):

        amt = int(input("Enter amount : "))

        if amt <= 0:
            print("Invalid amount")
            return

        self.data[self.user]["money"] += amt

        text = "Deposited " + str(amt) + " on " + str(datetime.now())

        self.data[self.user]["history"].append(text)

        save(self.data)

        print("Money deposited")

    def withdraw_money(self):

        amt = int(input("Enter amount : "))

        bal = self.data[self.user]["money"]

        if amt > bal:
            print("Low balance")

        elif amt <= 0:
            print("Invalid amount")

        else:
            self.data[self.user]["money"] -= amt

            text = "Withdraw " + str(amt) + " on " + str(datetime.now())

            self.data[self.user]["history"].append(text)

            save(self.data)

            print("Please collect cash")

    def send_money(self):

        other = input("Enter receiver name : ")

        if other not in self.data:
            print("Receiver not found")
            return

        amt = int(input("Amount : "))

        if amt <= 0:
            print("Invalid amount")
            return

        if amt > self.data[self.user]["money"]:
            print("Not enough balance")
            return

        self.data[self.user]["money"] -= amt

        self.data[other]["money"] += amt

        t1 = "Sent " + str(amt) + " to " + other + " on " + str(datetime.now())

        t2 = "Received " + str(amt) + " from " + self.user + " on " + str(datetime.now())

        self.data[self.user]["history"].append(t1)

        self.data[other]["history"].append(t2)

        save(self.data)

        print("Transfer done")

    def history(self):

        print("\nTransaction History")

        h = self.data[self.user]["history"]

        if len(h) == 0:
            print("No history")

        else:
            for i in h:
                print(i)

    def change_pin(self):

        old = input("Old pin : ")

        if old == self.data[self.user]["pin"]:

            new = input("New pin : ")

            if len(new) != 4:
                print("Pin must be 4 digits")
                return

            self.data[self.user]["pin"] = new

            save(self.data)

            print("Pin updated")

        else:
            print("Wrong old pin")


obj = BankATM()

while True:

    print("\n====== BANK ATM ======")
    print("1.Register")
    print("2.Login")
    print("3.Exit")

    op = input("Choose : ")

    if op == "1":

        obj.create_account()

    elif op == "2":

        obj.login()

    elif op == "3":

        print("Thank you")
        break

    else:

        print("Wrong choice")