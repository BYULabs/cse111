"""Calculate discount and tax on a customer order."""
from datetime import datetime

DISCOUNT_DAYS = [2, 3]  # Wednesday and Thursday
DISCOUNT_RATE = 0.10  # 10% discount
TAX_RATE = 0.06  # 6% tax


def main():
    """Process customer order with discount and tax calculation."""
    today = datetime.now()
    dow = today.weekday()  # Monday is 0 and Sunday is 6
    subtotal = 0.0
    quantity = -1

    while quantity != 0:
        quantity = int(input("Enter the quantity of items (0 to end): "))
        if quantity == 0:
            break
        price = float(input("Enter the price of the item: "))
        subtotal += quantity * price

    print(f"Total order: ${subtotal:.2f}")
    discount = 0
    if dow in DISCOUNT_DAYS:
        if subtotal >= 50:
            discount = round(subtotal * DISCOUNT_RATE, 2)
            print(f"Discount: ${discount:.2f}")
        else:
            short = 50 - subtotal
            print(f"Add ${short:.2f} more to your order to qualify for a discount.")

    subtotal -= discount
    tax = round(subtotal * TAX_RATE, 2)
    total = subtotal + tax

    print(f"Tax: ${tax:.2f}")
    print(f"Total Due: ${total:.2f}")


if __name__ == "__main__":
    main()
