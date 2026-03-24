with open('provinces.txt') as f:
    provinces = f.read().splitlines()
    
provinces.pop(0)
provinces.pop(-1)

count = 0
for i in range(len(provinces)):
    if provinces[i] == "Alberta":
        count+=1
    elif provinces[i] == "AB":
        provinces[i] = "Alberta"
        count += 1
    

print(provinces)
print(f"Alberta occurs {count} times in the list.")