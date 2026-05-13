# 1 - IMPORTS
# Importing neo4j connection helper & MySQL Connector
from numpy import record
from neo4j import GraphDatabase
import mysql.connector

# 2 - DATABASE CONNECTIONS
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

# 3 - MENU OPTION 1
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

# 4 - MENU OPTION 2
def view_attendees_by_company():
    company_id = input("Enter company ID: ")

    if not company_id.isdigit():
        print("Invalid company ID")
        return

    company_id = int(company_id)

    connection = get_mysql_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT companyName FROM company WHERE companyID = %s",
        (company_id,)
    )
    company = cursor.fetchone()

    if not company:
        print("Company does not exist")
        cursor.close()
        connection.close()
        return

    print(f"\nCompany: {company[0]}")

    query = """
    SELECT
        a.attendeeName,
        a.attendeeDOB,
        s.sessionTitle,
        s.speakerName,
        s.sessionDate,
        r.roomName
    FROM attendee a
    JOIN registration reg ON a.attendeeID = reg.attendeeID
    JOIN session s ON reg.sessionID = s.sessionID
    JOIN room r ON s.roomID = r.roomID
    WHERE a.attendeeCompanyID = %s
    """

    cursor.execute(query, (company_id,))
    results = cursor.fetchall()

    if not results:
        print("No attendees for this company")
    else:
        for row in results:
            print(f"\nName: {row[0]}")
            print(f"DOB: {row[1]}")
            print(f"Session: {row[2]}")
            print(f"Speaker: {row[3]}")
            print(f"Date: {row[4]}")
            print(f"Room: {row[5]}")

    cursor.close()
    connection.close()

# 5 - MENU OPTION 3
def add_new_attendee():
    attendee_id = input("Enter attendee ID: ")
    name = input("Enter attendee name: ")
    dob = input("Enter DOB (YYYY-MM-DD): ")
    gender = input("Enter gender (Male/Female): ")
    company_id = input("Enter company ID: ")

    # Validate ID
    if not attendee_id.isdigit():
        print("Invalid attendee ID")
        return

    # Validate company ID
    if not company_id.isdigit():
        print("Invalid company ID")
        return

    # Validate gender
    if gender not in ["Male", "Female"]:
        print("Invalid gender")
        return

    attendee_id = int(attendee_id)
    company_id = int(company_id)

    connection = get_mysql_connection()
    cursor = connection.cursor()

    # Check if attendee already exists
    cursor.execute(
        "SELECT * FROM attendee WHERE attendeeID = %s",
        (attendee_id,)
    )
    if cursor.fetchone():
        print("Attendee ID already exists")
        cursor.close()
        connection.close()
        return

    # Check if company exists
    cursor.execute(
        "SELECT * FROM company WHERE companyID = %s",
        (company_id,)
    )
    if not cursor.fetchone():
        print("Invalid Company ID")
        cursor.close()
        connection.close()
        return

    # Insert new attendee
    query = """
    INSERT INTO attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (attendee_id, name, dob, gender, company_id))
    connection.commit()

    print("Attendee successfully added")

    cursor.close()
    connection.close()

# SECTION 6 - MENU OPTION 4 & 5
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

# 7 - MENU OPTION 6
def view_rooms():
    connection = get_mysql_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        roomID,
        roomName,
        capacity
    FROM room
    """

    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        print("No rooms found")
    else:
        print("\n=== Rooms ===")
        for room_id, room_name, capacity in results:
            print(f"\nRoom ID: {room_id}")
            print(f"Room Name: {room_name}")
            print(f"Capacity: {capacity}")

    cursor.close()
    connection.close()

## 8 - FINAL MENU LOOP
while True:
    print("\n=== Main Menu ===")
    print("1. View Speakers & Sessions")
    print("2. View Attendees by Company")
    print("3. Add New Attendee")
    print("4. View Connected Attendees")
    print("5. Add Attendee Connection")
    print("6. View Rooms")
    print("x. Exit")

    choice = input("Enter your choice: ")

    # OPTION 1
    if choice == "1":
        view_speakers_and_sessions()
        input("\nPress Enter to return to the menu...")

    # OPTION 2
    elif choice == "2":
        view_attendees_by_company()
        input("\nPress Enter to return to the menu...")

    # OPTION 3
    elif choice == "3":
        add_new_attendee()
        input ("\nPress Enter to rerturn to the menu...")

    # OPTION 4
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

    # OPTION 5
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

    # OPTION 6
    elif choice == "6":
        view_rooms()
        input("\nPress Enter to return to the menu...")

    # EXIT
    elif choice.lower() == "x":
        print("Exiting program...")
        break

    # INVALID INPUT
    else:
        print("Invalid choice, please try again")

