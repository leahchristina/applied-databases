# applied-databases
Repository for my final project of the Applied Databases module.
This project is a menu-driven Python application that connects to both MySQL and Neo4j.

MySQL stores the structured conference data such as attendees, sessions, and rooms.
Neo4j stores the connections between attendees.

The user interacts with the system through a command-line menu.

## Menu Options & Functions
1 – View Speakers & Sessions:
   Displays speaker name, session title, and room.

2 – View Attendees by Company:
   Displays all attendees from a company and details of sessions attended.

3 – Add New Attendee:
   Adds a new attendee after validation checks.

4 – View Connected Attendees:
   Shows all connections for a given attendee using Neo4j.

5 – Add Attendee Connection:
   Creates a new relationship between attendees.

6 – View Rooms:
   Displays all rooms and their capacities.

7 - View Sessions By Date:
    Shows all sessions taking place on a date inputted by the user.

8 - Check Attendee Registration:
    Displays all sessions an Attendee ID is registered to upon input.

## How to Run
How to Run the Program:
1. Ensure MySQL and Neo4j Desktop are running
2. Start the Neo4j database (appdbprojNeo4j)
3. Ensure MySQL database (appdbproj) is available
4. Open a terminal in the project folder
5. Run the program using:

   *python main.py*

6. Follow the on-screen menu prompts

### Requirements:
- Python 3.x
- MySQL Server running locally
- Neo4j Desktop running locally

## Challenges
- Understanding Neo4j vs MySQL differences
- Handling joins across multiple tables in MySQL
- Debugging connection and configuration issues as I am new to Neo4j.

This project demonstrates the ability to integrate multiple database systems into a single Python application while handling user input, validation, and data processing.
