"""Password strength checker that evaluates and stores passwords."""
import os

# Constants
LOWER = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
         "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
UPPER = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
         "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
SPECIAL = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_",
           "=", "+", "[", "]", "{", "}", "|", ";", ":", "'", "\"", ",",
           ".", "<", ">", "?", "/", "\\", "`", "~"]

TOP_PASSWORDS_FILE = os.path.join(
    os.path.dirname(__file__), "toppasswords.txt")
WORDLIST_FILE = os.path.join(os.path.dirname(__file__), "wordlist.txt")


# Utility Functions
def load_files():
    """Load top passwords and wordlist files from disk.
    
    Returns:
        tuple: A tuple containing (top_passwords_list, wordlist)
    """
    top_passwords = []
    wordlist = []

    if os.path.exists(TOP_PASSWORDS_FILE):
        try:
            with open(TOP_PASSWORDS_FILE, "r", encoding="utf-8") as f:
                top_passwords = f.read().splitlines()
        except Exception as e:
            print(f"Error loading top passwords: {e}")

    if os.path.exists(WORDLIST_FILE):
        try:
            with open(WORDLIST_FILE, "r", encoding="utf-8") as f:
                wordlist = f.read().splitlines()
        except Exception as e:
            print(f"Error loading wordlist: {e}")

    return top_passwords, wordlist


def word_in_file(word, filename, case_sensitive=False):
    """Check if a word exists in a list of words.
    
    Args:
        word: The word to search for
        filename: List of words to search in
        case_sensitive: Whether comparison is case-sensitive
        
    Returns:
        bool: True if word is found, False otherwise
    """
    for name in filename:
        if case_sensitive:
            if word == name:
                return True
        else:
            if word.lower() == name.lower():
                return True
    return False


def word_has_character(word, character_list):
    """Check if a word contains any character from a list.
    
    Args:
        word: The word to check
        character_list: List of characters to search for
        
    Returns:
        bool: True if any character is found, False otherwise
    """
    for char in word:
        if char in character_list:
            return True
    return False


def word_complexity(word):
    """Calculate password complexity score based on character types.
    
    Args:
        word: The password to evaluate
        
    Returns:
        int: Complexity score (0-4) based on character types used
    """
    complexity = 0
    if word_has_character(word, LOWER):
        complexity += 1
    if word_has_character(word, UPPER):
        complexity += 1
    if word_has_character(word, DIGITS):
        complexity += 1
    if word_has_character(word, SPECIAL):
        complexity += 1
    return complexity


# Load global data
TOP_PASSWORDS_LIST, WORDLIST_LIST = load_files()
password_history = []


# Main Logic Functions
def password_strength(password, min_length=10, strong_length=16):
    """Evaluate and print password strength.
    
    Args:
        password: The password to evaluate
        min_length: Minimum acceptable password length
        strong_length: Length threshold for strong passwords
        
    Returns:
        str: A string describing the strength assessment
    """
    length = len(password)
    dictionary = word_in_file(password, TOP_PASSWORDS_LIST) 
    known = word_in_file(password, WORDLIST_LIST)
    complexity = 0
    if known:
        complexity = 0
        message = "Dictionary word (0/5) - Not Secure"
    elif dictionary:
        complexity = 0
        message = "Common password (0/5) - Not Secure"
    elif length > strong_length:
        complexity = 5
        message = "Long password (5/5) - Strong"
    elif length < min_length:
        complexity = word_complexity(password)
        message = f"Too short ({complexity}/5) - Not Secure"
    else:
        complexity = word_complexity(password)
        if length >= min_length:
            complexity += 1
        message = f"Score: {complexity}/5"
    
    print(f"\n{message}")
    return message


def show_history():
    """Display the history of tested passwords and their scores."""
    if not password_history:
        print("\nNo passwords tested yet.\n")
        return
    
    print("\n" + "="*60)
    print(f"{'Password':<20} {'Strength':<30}")
    print("="*60)
    for pwd, strength in password_history:
        print(f"{pwd:<20} {strength:<30}")
    print("="*60 + "\n")


def main():
    """Run the main password strength checking loop."""
    print("\nThis program tests the strength of passwords.")
    print("Commands: Enter password, 'h' for history, 'c' to"
          " clear history, 'q' to quit\n")
    while True:
        user_input = input("Enter a password to test (or command): ")
        
        if user_input.lower() == 'q':
            print("\nGoodbye!\n")
            return
        elif user_input.lower() == 'h':
            show_history()
        elif user_input.lower() == 'c':
            password_history.clear()
            print("\nHistory cleared.\n")
        elif user_input:
            strength = password_strength(user_input)
            password_history.append((user_input, strength))


# Entry Point
if __name__ == "__main__":
    main()