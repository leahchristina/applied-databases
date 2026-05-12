# Importing neo4j connection helper & MySQL Connector
from numpy import record
from neo4j import GraphDatabase
import mysql.connector

# Neo4j helper function
def get_neo4j_driver():
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "glencoagh"  # same one you set in Neo4j Desktop

    return GraphDatabase.driver(uri, auth=(username, password))

# MySQL Helper Function
def get_mysql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="appdbproj",
        port=3306
    )

# Menu Option 1 
def view_speakers_and_sessions():
    search = input("Enter speaker name (or part of name): ")

    query = """
    SELECT
        s.speakerName,
        s.sessionTitle,
        r.roomName
    FROM session s
    JOIN room r ON s.roomID = r.roomID
    WHERE s.speakerName LIKE %s
    """

    connection = get_mysql_connection()
    cursor = connection.cursor()

    cursor.execute(query, (f"%{search}%",))
    results = cursor.fetchall()

    if len(results) == 0:
        print("No speakers match that search.")
    else:
        for speaker, session, room in results:
            print(f"\nSpeaker: {speaker}")
            print(f"Session: {session}")
            print(f"Room: {room}")

    cursor.close()
    connection.close()

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

# Menu Option 5
def add_attendee_connection(id1, id2):
    check_query = """
    MATCH (a:Attendee {AttendeeID: $id1})-[:CONNECTED_TO]-
          (b:Attendee {AttendeeID: $id2})
    RETURN a
    """

    create_query = """
    MATCH (a:Attendee {AttendeeID: $id1}),
          (b:Attendee {AttendeeID: $id2})
    CREATE (a)-[:CONNECTED_TO]->(b)
    """

    driver = get_neo4j_driver()

    with driver.session() as session:
        # Check if connection already exists
        existing = session.run(check_query, id1=int(id1), id2=int(id2)).single()

        if existing:
            driver.close()
            return "exists"

        # Create new connection
        session.run(create_query, id1=int(id1), id2=int(id2))

    driver.close()
    return "created"


## Menu Loop
while True:
    print("\n=== Main Menu ===")
    print("1. View Speakers & Sessions")
    print("2. Option Two")
    print("4. View Connected Attendees")
    print("5. Add Attendee Connection")
    print("x. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        view_speakers_and_sessions()
        input("\nPress Enter to return to the menu...")

    elif choice == "2":
        print("You chose option 2")

    elif choice == "4":
        attendee_id = input("Enter attendee ID: ")

        if not attendee_id.isdigit():
            print("Invalid attendee ID")
            continue

        record = get_connected_attendees(attendee_id)

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

        input("\nPress Enter to return to the menu...")

    elif choice == "5":
        id1 = input("Enter first attendee ID: ")
        id2 = input("Enter second attendee ID: ")

        if not id1.isdigit() or not id2.isdigit():
            print("Attendee IDs must be numeric")
            continue

        if id1 == id2:
            print("An attendee cannot be connected to themselves")
            continue

        result = add_attendee_connection(id1, id2)

        if result == "exists":
            print("These attendees are already connected")
        else:
            print("Connection successfully added")

        input("\nPress Enter to return to the menu...")

    elif choice.lower() == "x":
        print("Exiting program...")
        break

    else:
        print("Invalid choice, please try again")
