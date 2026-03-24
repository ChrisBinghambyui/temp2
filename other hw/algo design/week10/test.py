number = int(input("Enter a positive, whole number: "))

total = number
while number > 0:
    total += number - 1
    number -= 1

print(total)