# Day 6 - Personal Expense Tracker

def calculate_total(expenses):
    total = 0

    for expense in expenses:
        total += expense
        
    return total

def check_budget(total,budget):

    if total < budget :
        return "you are within your budget"

    elif total == budget :
        return "you have used your entire budget"

    else :
        return "you jave exceeded your budget"

print("="*38)
print("       PERSONAL EXPENSE TRACKER")
print("="*38)

budget = float(input("\nEnter your monthly budget :"))

expense_names = []
expense_amounts = []

number = int(input("How many expense do you want to enter?"))

for i in range(number):
    print("\nExpense",i+1)

    name = input("Enter expense name :")
    amount = float(input("Enter amount :"))

    expense_names.append(name) #store datas in list
    expense_amounts.append(amount)

total = calculate_total(expense_amounts)

remaining = budget - total

percentage = (total/budget)*100

status = check_budget(total,budget)

print("\n======================================")
print("          EXPENSE SUMMARY")
print("="*38)

for i in range(number):
    print(expense_names[i], ":", expense_amounts[i])

print("-"*38)
print("Monthly Budget    :", round(budget, 2))
print("Total Expenses    :", round(total, 2))
print("Remaining Balance :", round(remaining, 2))
print("Budget Used       :", round(percentage, 2), "%")
print("-"*38)

print("Status:", status)

print("="*38)




