"""Receipt program that reads products and creates a formatted receipt."""

import csv
from datetime import datetime

def main():
    """Main function that reads product and request CSV files and generates a receipt.
    
    Reads products from products.csv and requests from request.csv, then calculates
    and displays a formatted receipt with item details, subtotal, sales tax (6%), and total.
    Handles FileNotFoundError, PermissionError, and KeyError exceptions.
    """
    print("========== SUPER MART ==========")
    print()
    try:
        KEY_INDEX = 0
        NAME_INDEX = 1
        products_dictionary = read_dictionary("products.csv", KEY_INDEX)
        with open("request.csv", "rt") as csvfile:
            requests = csv.reader(csvfile, delimiter=",")
            next(requests)
            print("Item Name               Quantity    Price Per Item")
            print("-" * 55)
            subtotal = 0
            for row in requests:
                product_key = row[0]
                quantity = int(row[1])
                if product_key in products_dictionary:
                    product = products_dictionary[product_key]
                    product_name = product[NAME_INDEX]
                    price = float(product[2])
                    total_price = price * quantity
                    subtotal += total_price
                    print(f"{product_name.title():<14} {quantity:>15}         ${price:.2f}")
                else:
                    print(f"Product with key {product_key} not found.")
            print("-" * 55)
            print(f"Subtotal:                              ${subtotal:.2f}")
            sales_tax = subtotal * 0.06
            print(f"Sales Tax (6%):                        ${sales_tax:.2f}")
            total_due = subtotal + sales_tax
            print(f"Total Due:                             ${total_due:.2f}")
            print()
            print("Thank you for your purchase!")
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except PermissionError as e:
        print(f"Error: Permission denied - {e}")
    except KeyError as e:
        print(f"Error: Invalid data format - key {e} not found")

def read_dictionary(filename, key_colmun_index):
    """Read a CSV file and create a dictionary from it.
    
    Args:
        filename (str): The name of the CSV file to read.
        key_colmun_index (int): The column index to use as the dictionary key.
    
    Returns:
        dict: A dictionary where keys are from the specified column and values are rows.
    
    Handles FileNotFoundError, PermissionError, and KeyError exceptions.
    """
    s_dictionary = {}
    try:
        with open(filename, "rt") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=",")
            next(csvreader)
            for row in csvreader:
                key_value = row[key_colmun_index]
                s_dictionary[key_value] = row
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    except PermissionError:
        print(f"Error: Permission denied accessing {filename}.")
    except KeyError:
        print(f"Error: Invalid data format - required column not found in {filename}.")
    return s_dictionary

if __name__ == "__main__":
    main()