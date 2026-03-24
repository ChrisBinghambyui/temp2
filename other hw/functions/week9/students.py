def read_dictionary(filename):
    """Read the contents of a CSV file into a
    dictionary and return the dictionary.

    Parameters
        filename: the name of the CSV file to read.
    Return: a dictionary that contains
        the contents of the CSV file.
    """
    # Create an empty dictionary
    students_dict = {}
    
    # Open and read the CSV file
    with open(filename) as students:
        lines = students.read().splitlines()
    
    # Process each line
    for i in range(len(lines)):
        # Skip the header row
        if i == 0:
            continue
        else:
            # Split the line by comma to get columns
            parts = lines[i].split(',')
            number = parts[0]
            name = parts[1]
            # Add to dictionary with I-Number as key, Name as value
            students_dict[number] = name
    
    return students_dict


def get_valid_input(prompt, valid_options):
    """Get input from user and validate it's in valid_options list"""
    valid = False
    choice = None
    
    while not valid:
        try:
            choice = int(input(prompt))
            if choice in valid_options:
                valid = True
            else:
                print(f"Invalid choice. Please enter one of: {valid_options}")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return choice


def remove_dashes(string):
    dash = "-"
    new_string = string.replace(dash, "")
    return new_string



def main():
    dictionary = read_dictionary(r"c:\Users\chris\Downloads\chris hw\python\functions\week9\students.csv")
    selection = get_valid_input("Name or I-number?", [1,2])
    
    if selection == 1:
        entry1 = input("Enter a name: ")
        for i_number, name in dictionary.items():
            if name == entry1:
                print(f"Student I-number: {i_number}")
        else:
            print("Student not found")

    elif selection == 2:
    
        entry1 = input("Enter an I-number: ")
        entry = remove_dashes(entry1)
        if entry in dictionary:
            print(f"Student name: {dictionary[entry]}")
        else:
            print("I-number not found")


if __name__ == "__main__":
    main()