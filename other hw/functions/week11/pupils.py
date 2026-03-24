import csv


# Each row in the pupils.csv file contains three elements.
# These are the indexes of the elements in each row.
GIVEN_NAME_INDEX = 0
SURNAME_INDEX = 1
BIRTHDATE_INDEX = 2

def main():
    try:
        # Read the pupils.csv file into a list named students_list.
        students_list = read_compound_list("pupils.csv")

        # Create a lambda function that returns a student's birthdate.
        get_birthdate = lambda student: student[BIRTHDATE_INDEX]

        # Sort students_list by birthdate from oldest to youngest.
        oldest_to_youngest = sorted(students_list, key=get_birthdate)

        # Print students ordered from oldest to youngest.
        print("Ordered from Oldest to Youngest")
        print_preview_list(oldest_to_youngest)
        print()

        # Create a lambda function that returns a student's given name.
        get_given_name = lambda student: student[GIVEN_NAME_INDEX]

        # Sort students_list by given name.
        by_given_name = sorted(students_list, key=get_given_name)

        # Print students ordered by given name.
        print("Ordered by Given Name")
        print_preview_list(by_given_name)
        print()

        # Create a lambda function that returns a student's birth month and day.
        get_birth_month_day = lambda student: student[BIRTHDATE_INDEX][5:]

        # Sort students_list by birth month and day.
        by_birth_month_day = sorted(students_list, key=get_birth_month_day)

        # Print students ordered by birth month and day.
        print("Ordered by Birth Month and Day")
        print_preview_list(by_birth_month_day)

    except FileNotFoundError as not_found_err:
        print(type(not_found_err).__name__, not_found_err, sep=": ")


def read_compound_list(filename):
    """Read the text from a CSV file into a compound list.
    The compound list will contain small lists. Each small
    list will contain the data from one row of the CSV file.

    Parameter
        filename: the name of the CSV file to read.
    Return: the compound list
    """
    # Create an empty list.
    compound_list = []

    # Open the CSV file for reading.
    with open(filename, "rt") as csv_file:

        # Use the csv module to create a reader
        # object that will read from the opened file.
        reader = csv.reader(csv_file)

        # The first line of the CSV file contains column headings
        # and not a student's I-Number and name, so this statement
        # skips the first line of the CSV file.
        next(reader)

        # Process each row in the CSV file.
        for row in reader:

            # Append the current row at the end of the compound list.
            compound_list.append(row)

    return compound_list


def print_list(example):
    for i in example:
        print(i)


def print_preview_list(example, count=10):
    for item in example[:count]:
        print(item)
    if len(example) > count:
        print("    \u22EE")


if __name__ == "__main__":
    main()