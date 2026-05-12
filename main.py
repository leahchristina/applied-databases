# Importing neo4j connection helper
from numpy import record

from neo4j import GraphDatabase

def get_neo4j_driver():
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "glencoagh"  # same one you set in Neo4j Desktop

    return GraphDatabase.driver(uri, auth=(username, password))

# Menu Option 4
def get_connected_attendees(attendee_id):
    query = """ 
    MATCH (a:Attendee {AttendeeID: $attendee_id})
    OPTIONAL MATCH (a)-[:CONNECTED_TO]-(b:Attendee)
    RETURN a.AttendeeID AS attendee,
           collect(b.AttendeeID) AS connections
    """

    driver = get_neo4j_driver()

    with driver.session() as session:
        result = session.run(query, attendee_id=int(attendee_id))
        record = result.single() # result or none

    driver.close()
    return record

## Menu Loop
while True:
    print("\n=== Main Menu ===")
    print("1. Option One")
    print("2. Option Two")
    print("4. View Connected Attendees")
    print("x. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("You chose option 1")

    elif choice == "2":
        print("You chose option 2")

    elif choice == "4":
        attendee_id = input("Enter attendee ID: ")

        if not attendee_id.isdigit():
            print("Invalid attendee ID")
            continue

        record = get_connected_attendees(attendee_id)
print("DEBUG: record is:", record)


        if record is None:
            print("Attendee not found in Neo4j")
            continue

        connections = [c for c in record["connections"] if c is not None]

        print(f"\nAttendee {record['attendee']} is connected to:")

        if len(connections) == 0:
            print("No connections")
        else:
            for connected_id in connections:
                print(f"- Attendee {connected_id}")

    elif choice.lower() == "x":
        print("Exiting program...")
        break

    else:
        print("Invalid choice, please try again")
