import datetime

def read_products(filename):
    products = {}
    
    with open(filename) as file:
        lines = file.read().splitlines()
    
    for i in range(len(lines)):
        if i == 0:
            continue
        else:
            parts = lines[i].split(',')
            product_id = parts[0]
            name = parts[1]
            price = float(parts[2])
            products[product_id] = {
                "name": name,
                "price": price
            }
    
    return products


def read_request(filename, products_dict):
    total = 0
    savings = 0

    with open(filename) as file:
        lines = file.read().splitlines()
    
    for i in range(len(lines)):
        if i == 0:
            continue
        else:
            parts = lines[i].split(',')
            product_id = parts[0]
            quantity = int(parts[1])

            if product_id not in products_dict:
                raise KeyError(f"unknown product ID '{product_id}' in request.csv")

            product_info = products_dict[product_id]
            name = product_info["name"]
            price = product_info["price"]
            subtotal = quantity * price
            total += subtotal

            if "yogurt" in name.lower():
                savings += quantity * 0.10

            print(f"{name}\t{quantity}\t\t{price:.2f}\t{subtotal:.2f}")

            if "yogurt" in name.lower():
                print(f"{name} sale\t\t-${(quantity*0.10):.2f}")

    discounted_total = total - savings
    return discounted_total, savings

ID_INDEX = 0
NAME_INDEX = 1
PRICE_INDEX = 2

QUANTITY_INDEX = 1


def main():
    sales_tax = 0.06
    products_dict = read_products("products.csv")
    # print(products_dict)
    print("W A L - M A R T")
    print("Product name:\tQuantity\tPrice\tSubtotal")
    try:
        subtotal, savings = read_request("request.csv", products_dict)
    except KeyError as error:
        print(f"Error: {error}")
        return
    

    # Import the datetime class from the datetime
    # module so that it can be used in this program.
    from datetime import datetime

    # Call the now() method to get the current
    # date and time as a datetime object from
    # the computer's operating system.
    current_date_and_time = datetime.now()

    # if current_date_and_time
    print(f"\nTotal savings: \t${savings:.2f}")
    print(f"\nSubtotal: \t${subtotal:.2f}")
    added_tax = round((subtotal * sales_tax), 2)
    print(f"Tax (6%): \t${added_tax}")
    total = subtotal + added_tax
    print(f"Total: \t\t${total:.2f}")
    print("Thank you for shopping with us.")
    print("Fill out a survey about your experience for a chance to win a $1000 Wal-mart gift card!")

    # Use an f-string to print the current
    # day of the week and the current time.
    print(f"{current_date_and_time:%A, %B %d}\t{ current_date_and_time:%I:%M %p}")








if __name__ == "__main__":
    main()