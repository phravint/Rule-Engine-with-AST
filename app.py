from flask import Flask, request, render_template
import mysql.connector
from mysql.connector import Error
import json 

app = Flask(__name__)

def create_connection():
    """Create a database connection."""
    try:
        conn = mysql.connector.connect(
            host='localhost',  # Change if needed
            database='rule_engine',  # Your database name
            user='root',  # Your MySQL username
            password='Tphravin06'  # Your MySQL password
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/submit_rule', methods=['POST'])
def submit_rule():
    """Handle the form submission."""
    rule_string = request.form['rule_string']
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rules (rule_string) VALUES (%s)", (rule_string,))
        conn.commit()
        cursor.close()
        conn.close()
        return "Rule submitted successfully!"
    else:
        return "Failed to connect to the database."

if __name__ == '__main__':
    app.run(debug=True)
