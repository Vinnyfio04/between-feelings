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
    SELECT password FROM users WHERE username = %s
    """
    
    cur.execute(query, (username,))
    correctPassword = cur.fetchone()[0]

    conn.close()
    cur.close()
    return password == correctPassword

def create_user(username, password):
    # create_user() is a method that takes two parameters: a string username that holds the username input, and a string password that holds the password input
    # It is called in authentication.html when the username input does not exist in the db.
    # It takes the two parameters and sends SQL code that adds the user to the authentication table in the database
    # Returns True if it was successfully created, False if there was an error
    return True