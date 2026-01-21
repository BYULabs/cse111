"""Calculate tire volume based on tire dimensions with interactive menu."""
import math
from datetime import datetime
import os


def calculate_tire_volume():
    """Get tire dimensions from user and calculate volume."""
    try:
        width = float(input("Enter the width of the tire in mm (ex 205): "))
        aspect_ratio = float(input("Enter the aspect ratio of the tire (ex 60): "))
        diameter = float(input("Enter the diameter of the wheel in inches (ex 15): "))
        
        if width <= 0 or aspect_ratio <= 0 or diameter <= 0:
            print("Error: All values must be positive numbers.")
            return
        
        volume = (math.pi * width**2 * aspect_ratio *
                  (width * aspect_ratio + 2540 * diameter)) / 10000000000
        
        print(f"\nThe approximate volume is {volume:.2f} liters")
        
        current_date_and_time = datetime.now()
        current_date = f"{current_date_and_time:%Y-%m-%d}"
        
        with open("volumes.txt", "at", encoding="utf-8") as volumes_file:
            print(f"{current_date}, {width:.0f}, {aspect_ratio:.0f}, {diameter:.0f}, {volume:.2f}", file=volumes_file)
        
        print("✓ Data saved to volumes.txt\n")
        
    except ValueError:
        print("Error: Please enter valid numbers.\n")


def view_history():
    """Display all previous calculations from volumes.txt."""
    try:
        if not os.path.exists("volumes.txt"):
            print("No history file found. Run a calculation first.\n")
            return
        
        with open("volumes.txt", "rt", encoding="utf-8") as volumes_file:
            lines = volumes_file.readlines()
        
        if not lines:
            print("No calculations recorded yet.\n")
            return
        
        print("\n" + "="*70)
        print(f"{'Date':<12} {'Width (mm)':<12} {'Aspect':<10} {'Diameter (in)':<15} {'Volume (L)':<10}")
        print("="*70)
        for line in lines:
            parts = line.strip().split(", ")
            if len(parts) == 5:
                date, width, aspect, diameter, volume = parts
                print(f"{date:<12} {width:<12} {aspect:<10} {diameter:<15} {volume:<10}")
        print("="*70 + "\n")
        
    except FileNotFoundError:
        print("No history file found.\n")


def clear_history():
    """Clear the volumes.txt file."""
    try:
        if os.path.exists("volumes.txt"):
            confirm = input("Are you sure you want to clear all history? (yes/no): ").lower()
            if confirm == "yes":
                open("volumes.txt", "w", encoding="utf-8").close()
                print("✓ History cleared.\n")
            else:
                print("Cancelled.\n")
        else:
            print("No history file to clear.\n")
    except Exception as e:
        print(f"Error: {e}\n")


def display_menu():
    """Display the main menu."""
    print("\n" + "="*40)
    print("     TIRE VOLUME CALCULATOR")
    print("="*40)
    print("1. Calculate tire volume")
    print("2. View history")
    print("3. Clear history")
    print("4. Exit")
    print("="*40)


def main():
    """Main program loop with interactive menu."""
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            calculate_tire_volume()
        elif choice == "2":
            view_history()
        elif choice == "3":
            clear_history()
        elif choice == "4":
            print("Thank you for using Tire Volume Calculator. Goodbye!\n")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    main()
