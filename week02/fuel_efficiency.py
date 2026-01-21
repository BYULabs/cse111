def main():
    """The main function of the program."""
    starting_odometer = float(input("Enter the value of the starting odometer in miles: "))
    ending_odometer = float(input("Enter the value of the ending odometer in miles: "))
    gallons_used = float(input("Enter the number of gallons used: "))
    # Your program must calculate and print fuel efficiency in both miles per gallon and liters per 100 kilometers. Your program must have three functions named as follows:
    mpg = calculate_mpg(starting_odometer, ending_odometer, gallons_used)
    lp100k = calculate_lp100k(mpg)
    print(f"Fuel efficiency in miles per gallon: {mpg:.2f} mpg")
    print(f"Fuel efficiency in liters per 100 kilometers: {lp100k:.2f} L/100km")
def calculate_mpg(starting_odometer, ending_odometer, gallons_used):
    """Calculate miles per gallon."""
    miles_driven = ending_odometer - starting_odometer
    mpg = miles_driven / gallons_used
    return mpg
def calculate_lp100k(mpg):
    """Calculate liters per 100 kilometers."""
    liters_per_gallon = 3.78541
    kilometers_per_mile = 1.60934
    lp100k = (100 * liters_per_gallon) / (mpg * kilometers_per_mile)
    return lp100k
if __name__ == "__main__":
    main()