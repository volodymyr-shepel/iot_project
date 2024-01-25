import sqlite3

# Connect to SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect('attendance_system.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create Employers table with Card UID as the unique identifier
cursor.execute('''
    CREATE TABLE Employers (
        card_uid TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        role TEXT
    )
''')

# Create Room table
cursor.execute('''
    CREATE TABLE Room (
        room_id INTEGER PRIMARY KEY,
        required_role TEXT
    )
''')

# Create Attendance table with foreign keys for card_uid and room_id
# use it if needed
# cursor.execute('''
#     CREATE TABLE Attendance (
#         attendance_id INTEGER PRIMARY KEY,
#         card_uid TEXT,
#         room_id INTEGER,
#         time DATETIME,
#         FOREIGN KEY (card_uid) REFERENCES Employers(card_uid),
#         FOREIGN KEY (room_id) REFERENCES Room(room_id)
#     )
# ''')


cursor.execute("INSERT INTO Employers VALUES ('84-85-32-5f', 'Daniil', 'Kuznetsov', 'Manager')")
cursor.execute("INSERT INTO Employers VALUES ('a4-f0-94-60', 'Valentina', 'Bolbas', 'Customer')")
cursor.execute("INSERT INTO Employers VALUES ('e4-44-d2-60', 'Volodymyr', 'Shepel', 'Manager')")
cursor.execute("INSERT INTO Employers VALUES ('c4-b3-26-5f', 'Bohdan', 'Kyryliuk', 'Customer')")

# Insert records into Room table
cursor.execute("INSERT INTO Room VALUES (1, 'Manager')")
cursor.execute("INSERT INTO Room VALUES (2, 'Customer')")
cursor.execute("INSERT INTO Room VALUES (3, 'Manager')")
cursor.execute("INSERT INTO Room VALUES (4, 'Customer')")
cursor.execute("INSERT INTO Room VALUES (5, 'Manager')")


# Commit the changes and close the connection
conn.commit()
conn.close()

print("Tables 'Employers' and 'Room' created successfully.")
