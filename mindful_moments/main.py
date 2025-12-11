from flask import Flask, jsonify, request

app = Flask(__name__)

#Log mood

@app.route('/log-mood', methods=['POST'])
def log_mood():
    data = request.get_json()
    mood = data.get("mood")
    focus_level = data.get("focus_level")
    note = data.get("note")

    if not mood or not focus_level:
        return jsonify({"error": "Mood and focus_level are required"}), 400

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO mood_logs (mood, focus_level, note) VALUES (%s, %s, %s)"
            cursor.execute(query, (mood, focus_level, note))
            conn.commit()
            return jsonify({"message": "Mood log saved!"}), 201
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500


#Get all mood entries
@app.route('/mood-history', methods=['GET'])
def mood_history():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM mood_logs ORDER BY date_logged DESC"
            cursor.execute(query)
            results = cursor.fetchall()
            return jsonify(results), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500


#Get a random suggestion

@app.route('/mindful-moment', methods=['GET'])
def mindful_moment():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM suggestions ORDER BY RAND() LIMIT 1"
            cursor.execute(query)
            suggestion = cursor.fetchone()
            return jsonify(suggestion), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Could not connect to database"}), 500


#Simulate user
def run():
    print("👋 Welcome to the Mindful Moments API!")
    print("📬 You can log your mood, receive mindful suggestions, and check your mood history.")
    print("✨ Use client.py or Postman to interact with the API.")

#Run the app
if __name__ == '__main__':
    run()
    app.run(debug=True)
