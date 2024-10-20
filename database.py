import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',  
            database='rule_engine', 
            user='root',  
            password='Tphravin06'  
        )
        if conn.is_connected():
            print("Successfully connected to the database")
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None

def create_table():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rules (
                id INT AUTO_INCREMENT PRIMARY KEY,
                rule_string TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("Table created successfully")
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_table()  # Call this function to create the table
