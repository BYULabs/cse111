import random

def main():
    numbers = [16.2, 75.1, 52.3]
    words = ["apple", "banana", "cherry"]
    print(numbers)
    append_random_number(numbers)
    print(numbers)
    append_random_number(numbers, 3)
    print(numbers)
    print(" --- ")
    print(words)
    append_random_word(words)
    print(words)
    append_random_word(words, 2)
    print(words)

def append_random_number(numlist, quantity=1):
    for _ in range(quantity):
        rand_num = round(random.uniform(0, 100), 1)
        numlist.append(rand_num)

def append_random_word(wordlist, quantity=1):
    for _ in range(quantity):
        rand_word = (random.choice(["orange", "grape", "melon", "kiwi", "mango"]))
        wordlist.append(rand_word)

if __name__ == "__main__":
    main()

     