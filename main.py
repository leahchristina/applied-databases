## Menu Loop
while True: # Prompt runs until break statement
    print("\n=== Main Menu ===")
    print("1. Option One")
    print("2. Option Two")
    print("4. View Connected Attendees")
    print("x. Exit")

    choice = input("Enter your choice: ") # User input

    if choice == "1":
        print("You chose option 1")

    elif choice == "2":
        print("You chose option 2")

    elif choice == "4":
        print("You chose option 4 (Neo4j will go here later)") # Placeholder message

    elif choice.lower() == "x":
        print("Exiting program...")
        break
# ensuring it can handle unexpected input
    else:
        print("Invalid choice, please try again")