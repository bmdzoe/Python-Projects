#Calculator Program
operator = input("Enter an operation(+ -  *  /): ")
#allows you to use different operations
#input is like scanner in java but you don't have to import it
num1 = float(input("Enter your 1st number:"))
#cast it as a float just in case there are decimals 
num2 = float(input("Enter your 2nd number:"))

if operator == "+":
    result = num1 + num2
    print(round(result,3))
#essentially is the addtion operation coded and we round the result to the 3rd decimal place
elif operator == "-":
    result = num1 - num2
    print(round(result,3))
#essentially is the subtraction operation coded and we round the result to the 3rd decimal place
elif operator == "*":
    result = num1 * num2
    print(round(result,3))
#essentially is the multiplication operation coded and we round to the result to the 3rd decimal place
elif operator == "/":
    result = num1/num2
    print(round(result,3))
#essentially is the division operation coded and we round the result to the 3rd decimal place
else:
    print(f"{operator} is not a valid operator")
#this is just to prompt the user to choose from one of the valid operators