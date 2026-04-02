import os # system module
import psycopg # database connector
import emotion_log #dataclass
from dotenv import load_dotenv

# get DATABASE_URL variable from the .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to the database using psycopg for future conn variables (reusing code)
def get_connection():
    return psycopg.connect(
        os.environ["DATABASE_URL"]
    )


# Methods to check user input

def user_exists(username):
    # Create a connection to the database
    conn = get_connection()
    cur = conn.cursor()

    # Create a query variable to check if the username exists in the database
    query = """
    SELECT EXISTS (SELECT 1 FROM users WHERE username = %s)
    """

    cur.execute(query, (username,))
    exists = cur.fetchone()[0]
    
    conn.close()
    cur.close()
    return exists

def verify_password(username, password):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT user_id, password FROM users WHERE username = %s
    """
   
    cur.execute(query, (username,))
    row = cur.fetchone()

    conn.close()
    cur.close()

    if row is None:
        return None

    user_id, correct_password = row
    if password == correct_password:
        return user_id
    return None

def create_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO users (username, password) VALUES ( %s, %s)
    """
    cur.execute(query, (username, password,))

    conn.commit()

    # Get the user id of the newly created user
    queryID = """
    SELECT user_id, password FROM users WHERE username = %s
    """
    cur.execute(queryID, (username,))
    row = cur.fetchone()
    user_id = row[0]

    cur.close()
    conn.close()

    return user_id