#Shopping Cart Program
foods = []
prices = []
total = 0

while True:
    food = input("Enter the food item: (q to quit) ")
    if food.lower() == 'q':
        break
    price = float(input("Enter the price of a {food} : $"))
    foods.append(food)
    prices.append(price)    

print("-----YOUR CART-----")
for food in foods:
    print(food, end= " ")

for price in prices:
    total += price
print()
print(f"Your total is: ${total}")