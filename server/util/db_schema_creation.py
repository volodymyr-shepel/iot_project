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
cursor.execute('''
    CREATE TABLE Attendance (
        attendance_id INTEGER PRIMARY KEY,
        card_uid TEXT,
        room_id INTEGER,
        time DATETIME,
        FOREIGN KEY (card_uid) REFERENCES Employers(card_uid),
        FOREIGN KEY (room_id) REFERENCES Room(room_id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Tables 'Employers' and 'Room' created successfully.")
