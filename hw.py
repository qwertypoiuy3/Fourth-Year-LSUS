#Asks for an integer input representing cents, stops when input < 0.
num = input("Enter the number of cents: ")
a = 0  
while int(num) >= 0:
    a += int(num)/100
    num = input("Next: ")

#Rounds the total value to 2 decimal points.    
a = round(a,2)

#Identfies the index value of the decimal point.
dec = str(a).index('.')
dollars = ""
cents = ""

#Iterates through the characters of the total value, and differentiates
#between dollars and cents.
for i in range (len(str(a))):
    if i < dec:
        dollars += str(a)[i]
    elif i > dec:
        cents += str(a)[i]

print("\nTotal= $",a,"\n")   

#Identifies the amount of money and divides it into the number of bills needed.        
remainder = 0
bill = 0
if int(dollars) / 100 >= 1:
    remainder = int(dollars) / 100
    bill += int(remainder)
    print ("You need:",int(remainder),"bills of 100")
    dollars = a - (int(remainder) * 100)
if int(dollars) / 50 >= 1:
    remainder = int(dollars) / 50
    print ("You need:",int(remainder),"bills of 50")
    bill += int(remainder)
    dollars = int(dollars) - (int(remainder) * 50)
if int(dollars) / 20 >= 1:
    remainder = int(dollars) / 20
    print ("You need:",int(remainder),"bills of 20")
    bill += int(remainder)
    dollars = int(dollars) - (int(remainder) * 20)
if int(dollars) / 10 >= 1:
    remainder = int(dollars) / 10
    print ("You need:",int(remainder),"bills of 10")
    bill += int(remainder)
    dollars = int(dollars) - (int(remainder) * 10)
if int(dollars) / 5 >= 1:
    remainder = int(dollars) / 5
    print ("You need:",int(remainder),"bills of 5")
    bill += int(remainder)
    dollars = int(dollars) - (int(remainder) * 5)
if int(dollars) / 1 >= 1:
    remainder = int(dollars) / 1
    print ("You need:",int(remainder),"bills of 1")
    bill += int(remainder)
    dollars = int(dollars) - (int(remainder) * 1)

#Identifies the amount of cents and divides it into the number of coins needed.
change = 0
coin = 0
if int(cents) / 25 >= 1:
    change = int(cents) / 25
    coin += int(change)
    print("\nYou need:",int(change),"quarters")
    cents = int(cents) - (int(change) * 25)
if int(cents) / 10 >= 1:
    change = int(cents) / 10
    coin += int(change)
    print("You need:",int(change),"dimes")
    cents = int(cents) - (int(change) * 10)
if int(cents) / 5 >= 1:
    change = int(cents) / 5
    coin += int(change)
    print("You need:",int(change),"nickels")
    cents = int(cents) - (int(change) * 5)
if int(cents) / 1 >= 1:
    change = int(cents) / 1
    coin += int(change)
    print("You need:",int(change),"pennies")
    cents = int(cents) - (int(change) * 1)

#Prints the number of bills and coins needed.
print("\n",bill, "bills.")
print("\n",coin, "coins.")
