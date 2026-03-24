# euro = float(input("Enter an amount in euros:"))
# assert isinstance(euro, float)

# def conversion(euro):
#     dollar = euro * 1.13
#     return dollar


# dollar = conversion(euro)

# print(f"{dollar:.2f}")

wages = float(input("Enter your hourly rate: "))
hours = float(input("Enter your hours: "))

assert hours > 0
assert wages > 0

def calc_pay(wages, hours):
    overtime_wage = wages*1.5
    if hours > 40:
        overtime_hours = hours - 40
        regular_hours = hours - overtime_hours
        assert regular_hours == 40
        assert overtime_hours > 0
        reg_pay = regular_hours*wages
        ot_pay = overtime_hours * overtime_wage
        total_pay = reg_pay + ot_pay
        return total_pay
    else:
        total_pay = wages * hours
    return total_pay

pay = calc_pay(wages, hours)
assert pay > 0
print(f"${pay:.2f}")




