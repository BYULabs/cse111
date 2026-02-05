def main():
    province_list = read_provinces("week05/provinces.txt")

    print(province_list)

    province_list.pop(0)
    province_list.pop()

    for i in range(len(province_list)):
        if province_list[i] == "AB":
            province_list[i] = "Alberta"
    
    count = province_list.count("Alberta")
    print(f"Alberta appears {count} times in the list.")

def read_provinces(filename):
    text_list = []
    with open(filename, "rt") as text_file:
        for line in text_file:
            clean_line = line.strip()
            text_list.append(clean_line)
    return text_list

if __name__ == "__main__":
    main()

