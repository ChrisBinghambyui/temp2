# 1. Name:
#      Chris Bingham
# 2. Assignment Name:
#      Lab 10: Number of Days
# 3. Assignment Description:
#       Count the number of days between two dates
# 4. What was the hardest part? Be as specific as possible.
#      asserts are something I'm still not super familiar with. I honestly struggle with them. It's weird, because logically i can explain and understand them, but when I'm implementing them I don't understand.
# 5. How long did it take for you to complete the assignment?
#      4.5

def is_leap_year(year):
    '''Return true if year is a leap year'''

    assert year > 1752

    if year % 4 != 0:
        return False
    elif year % 100 != 0:
        return True
    elif year % 400 == 0:
        return True
    else:
        return False
    
def month_days(month, year):
    assert 0 < month < 13
    assert year > 1752

    days = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month != 2 or is_leap_year(year):
        return days[month] 
    else:
        return 28

def year_days (year):
    if is_leap_year(year):
        return 366
    else:
        return 365

def prompt(text, min, max):
    done = False
    while not done:
        try:
            data = int(input(f"{text}:"))

            if min <= data <= max:
                done = True
            else:
                print(f"Error, please enter a number between {min} and {max}")
        except:
            print("Please enter a number.")
    return data

def days(start_year, start_month, start_day, end_year, end_month, end_day):
    assert start_year >= 1753
    assert 1 <= start_month <= 12
    assert 1 <= start_day <= month_days(start_month, start_year)
    assert 1753 <= start_year <= end_year
    assert 1 <= end_month <= 12
    assert 1 <= end_day <= month_days(end_month, end_year)

    if end_year == start_year and end_month == start_month:
        assert end_day >= start_day
        return end_day - start_day

    days = month_days(start_month, start_year) - start_day

    if start_year == end_year:
        assert start_month <= end_month
        for month in range(start_month + 1, end_month):
            days += month_days(month, start_year)
    else:
        for month in range(start_month + 1, 13):
            days += month_days(month, start_year)

        for year in range(start_year + 1, end_year):
            days += year_days(year)

        for month in range(1, end_month):
            days += month_days(month, end_year)

    days += end_day

    assert days >= 0
    return days

run_automation = input("Do you want to run automation? (y/n): ")

if run_automation == 'y':
    assert is_leap_year(1999) == False
    assert is_leap_year(2000) == True
    assert is_leap_year(2003) == False
    assert is_leap_year(2004) == True

    assert year_days(1999) == 365
    assert year_days(2000) == 366
    assert year_days(2003) == 365
    assert year_days(2004) == 366

    assert month_days(1, 1753) == 31
    assert month_days(2, 1999) == 28
    assert month_days(2, 2000) == 29
    assert month_days(2, 2003) == 28
    assert month_days(2, 2004) == 29
    assert month_days(3, 1753) == 31
    assert month_days(4, 1753) == 30
    assert month_days(5, 1753) == 31
    assert month_days(6, 1753) == 30
    assert month_days(7, 1753) == 31
    assert month_days(8, 1753) == 31
    assert month_days(9, 1753) == 30
    assert month_days(10, 1753) == 31
    assert month_days(11, 1753) == 30
    assert month_days(12, 1753) == 31

    assert days(1971, 11, 13, 1971, 11, 13) == 0
    assert days(1999, 10, 15, 1999, 10, 25) == 10
    assert days(1999, 10, 23, 1999, 12, 1) == 39
    assert days(1999, 10, 21, 2004, 3, 4) == 1596
    assert days(2002, 11, 17, 2004, 3, 6) == 475

    assert days(2001, 1, 9, 2001, 1, 9) == 0
    assert days(2001, 1, 9, 2001, 1, 19) == 10
    assert days(2001, 1, 9, 2001, 4, 19) == 100
    assert days(2001, 1, 9, 2003, 10, 6) == 1000
    assert days(2001, 1, 9, 2028, 5, 27) == 10000

    try:
        is_leap_year(1752)
        assert False
    except AssertionError:
        pass

    try:
        is_leap_year("banana")
        assert False
    except TypeError:
        pass

    try:
        days(2001, 0, 1, 2001, 1, 1)
        assert False
    except AssertionError:
        pass

    try:
        days(2001, 13, 1, 2001, 1, 1)
        assert False
    except AssertionError:
        pass

    try:
        days(2001, 1, 0, 2001, 1, 1)
        assert False
    except AssertionError:
        pass

    try:
        days(2003, 2, 29, 2004, 1, 1)
        assert False
    except AssertionError:
        pass

    try:
        days(2001, 1, 9, 2001, 1, 8)
        assert False
    except AssertionError:
        pass

    print("All tests passed")

else:
    start_year = prompt("Start year", 1753, 3000)

    start_month = prompt("start month", 1, 12)

    days_in_start_month = month_days(start_month, start_year)
    start_day = prompt("Start day", 1, days_in_start_month)

    end_year = prompt("End year", start_year, 3000)

    earliest_end_month = 1 if end_year > start_year else start_month
    end_month = prompt("End month", earliest_end_month, 12)

    earliest_start_day = 1 if end_year > start_year or end_month > start_month else start_day
    days_in_end_month = month_days(end_month, end_year)
    end_day = prompt("End day", earliest_start_day, days_in_end_month)

    total_days = days(start_year, start_month, start_day, end_year, end_month, end_day)
    print(f"There are {total_days} days between {start_month}/{start_day}/{start_year} and {end_month}/{end_day}/{end_year}")

    earliest_start_day = 1 if end_year > start_year or end_month > start_month else start_day
    days_in_end_month = month_days(end_month, end_year)
    end_day = prompt("End day", earliest_start_day, days_in_end_month)

    end_days = days(start_year, start_month, start_day, end_year, end_month, end_day)
    assert 0 <= end_days
    print(f"\nThere are {end_days} days.")