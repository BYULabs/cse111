def main():
  # Create and print a list named fruit.
  fruit_list = ["pear", "banana", "apple", "mango"]
  print(f"original: {fruit_list}")
  
  # Reverse the list
  fruit_list.reverse()
  print(f"reversed: {fruit_list}")
  
  # Append "orange" to the list
  fruit_list.append("orange")
  print(f"after append: {fruit_list}")
  
  # Find the index of "apple" and insert "cherry" before it
  apple_index = fruit_list.index("apple")
  fruit_list.insert(apple_index, "cherry")
  print(f"after insert: {fruit_list}")
  
  # Remove "banana" from the list
  fruit_list.remove("banana")
  print(f"after remove: {fruit_list}")
  
  # Pop the last element from the list
  popped_element = fruit_list.pop()
  print(f"popped element: {popped_element}")
  print(f"after pop: {fruit_list}")
  
  # Sort the list
  fruit_list.sort()
  print(f"sorted: {fruit_list}")

if __name__ == "__main__":
    main()