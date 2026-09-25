# Key check for Try with me 1
sales = []
print("after line 1:", sales, len(sales))
sales.append({"item": "chai", "price": 60})
print("after line 2:", sales, len(sales))
sales.append({"item": "samosa", "price": 40})
print("after line 3:", sales, len(sales))
sales.append({"item": "chai", "price": 60})
print("after line 4:", sales, len(sales))
print(len(sales))
print("prices added up (wrong option C):", sales[0]["price"] + sales[1]["price"] + sales[2]["price"])
