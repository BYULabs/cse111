import csv

def main():
    KEY_INDEX = 0
    NAME_INDEX = 1
    students = read_dictionary("week05/students.csv", KEY_INDEX)
    inumber = input("Enter an i-number: ")
    inumber = inumber.replace("-", "")
    if not inumber.isdigit():
        print("Invalid i-number format.")
    elif len(inumber) != 9:
        print("An i-number must have 9 digits.")
    else:
        if inumber in students:

            student = students[inumber]
            name = student[NAME_INDEX]
            print(f"The name of the student with i-number {inumber} is {name}.")
        else:
            print(f"There is no student with i-number {inumber}.")

def read_dictionary(filename, key_colmun_index):
    s_dictionary = {}
    with open(filename, "rt") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        next(csvreader)
        for row in csvreader:
            key_value = row[key_colmun_index]
            s_dictionary[key_value] = row
    return s_dictionary

if __name__ == "__main__":
    main()