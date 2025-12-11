"""
SQL-Connector and all things DB go in here
"""

import mysql.connector
from config import db_config

class DbConnectionError(Exception):
    pass

#Connect to the database
def _connect_to_db():
    cnx = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        auth_plugin='mysql_native_password'
    )
    return cnx

#Fetch all mood logs
def get_all_mood_logs():
    db_connection = None
    try:
        db_connection = _connect_to_db()
        cur = db_connection.cursor(dictionary=True)
        print(f"✅ Connected to DB: {db_config['database']}")

        query = "SELECT * FROM mood_logs ORDER BY date_logged DESC"
        cur.execute(query)
        result = cur.fetchall()

        cur.close()
        return result

    except Exception as e:
        print(e)
        raise DbConnectionError("Failed to fetch mood logs from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("🔌 DB connection closed")

#Insert a new mood log
def insert_mood_log(mood_data):
    db_connection = None
    try:
        db_connection = _connect_to_db()
        cur = db_connection.cursor()
        print(f"✅ Connected to DB: {db_config['database']}")

        query = """
            INSERT INTO mood_logs (mood, focus_level, note)
            VALUES (%s, %s, %s)
        """
        values = (
            mood_data["mood"],
            mood_data["focus_level"],
            mood_data.get("note")
        )
        cur.execute(query, values)
        db_connection.commit()

        print("📝 Mood log inserted successfully!")

        cur.close()

    except Exception as e:
        print(e)
        raise DbConnectionError("Failed to insert mood log")

    finally:
        if db_connection:
            db_connection.close()
            print("🔌 DB connection closed")


#Fetch one random suggestion
def get_random_suggestion():
    db_connection = None
    try:
        db_connection = _connect_to_db()
        cur = db_connection.cursor(dictionary=True)
        print(f"✅ Connected to DB: {db_config['database']}")

        query = "SELECT * FROM suggestions ORDER BY RAND() LIMIT 1"
        cur.execute(query)
        suggestion = cur.fetchone()

        cur.close()
        return suggestion

    except Exception as e:
        print(e)
        raise DbConnectionError("Failed to fetch suggestion")

    finally:
        if db_connection:
            db_connection.close()
            print("🔌 DB connection closed")

#Testing the DB functions
if __name__ == "__main__":
    print("🧪 TESTING DB CONNECTION")
    logs = get_all_mood_logs()
    for log in logs:
        print(log)
