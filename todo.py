# Function to read the to-do list from a file
def read_list_from_file():
    try:
        with open('todolist.txt', 'r') as file:
            todolist = file.readlines()
        return [task.strip() for task in todolist]  # Strip any extra newlines
    except FileNotFoundError:
        return []  # If the file doesn't exist, return an empty list

# Function to write the to-do list to a file
def write_list_to_file():
    with open('todolist.txt', 'w') as file:
        for task in todolist:
            file.write(f"{task}\n")

# Global variable for to-do list
todolist = read_list_from_file()

def add(text):
    global todolist
    todolist.append(text)
    print(f"Added '{text}' to the list.")
    write_list_to_file()  # Save the updated list to the file

def remove(text):
    global todolist
    if text in todolist:
        todolist.remove(text)
        print(f"Removed '{text}' from the list.")
        write_list_to_file()  # Save the updated list to the file
    else:
        print(f"'{text}' not found in the list.")

def get():
    global todolist
    if todolist:
        print("To-Do List:")
        for task in todolist:
            print(f"- {task}")
    else:
        print("The to-do list is empty.")

def main(command):
    if "add" in command:
        add(command.split("add ")[1].strip())  # To handle extra spaces
        get()
    elif "get" in command:
        get()
    elif "remove" in command:
        remove(command.split("remove ")[1].strip())  # To handle extra spaces
        get()
    else:
        print("Invalid command. Please use 'add', 'get', or 'remove'.")

# Example usage
main("add chores in list1")
main("get")
main("remove chores in list1")
main("get")
