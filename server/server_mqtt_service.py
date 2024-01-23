import sqlite3
import json

class AccessChecker:
    def __init__(self, db_name='attendance_system.db'):
        self.db_name = db_name

    def check_access(self, message):
        try:
            # Extract information from the message
            message_data = json.loads(message)
            user_id = message_data.get("measurement")  # Assuming measurement is now the card_id (user_id)
            room_id = message_data.get("id")  # Assuming id is now the room_id

            # Connect to the SQLite database
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Check if the user with the given card_id has the required role for the room with room_id
            cursor.execute('''
                SELECT e.role
                FROM Employers e
                JOIN Room r ON e.role = r.required_role
                WHERE e.card_uid = ? AND r.room_id = ?
            ''', (user_id, room_id))

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

