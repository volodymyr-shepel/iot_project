import sqlite3
import json
class AccessChecker:
    def __init__(self, db_name='attendance_system.db'):
        self.db_name = db_name

    def check_access(self, message):
        try:
            # Extract information from the message
            message_data = json.loads(message)
            user_id = message_data.get("id")
            measurement = message_data.get("measurement")

            # Connect to the SQLite database
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Check if the user with the given id and measurement has the required role for the room
            cursor.execute('''
                SELECT e.role
                FROM Employers e
                JOIN Room r ON e.role = r.required_role
                WHERE e.card_uid = ? AND r.room_id = ?
            ''', (user_id, measurement))

            result = cursor.fetchone()

            # Close the database connection
            conn.close()

            if result:
                return True
            else:
                return False

        except Exception as e:
            print(f"Error checking access: {e}")
            return False