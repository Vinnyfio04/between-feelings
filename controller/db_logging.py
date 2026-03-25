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



# Take user emotion log inputs and send it to the db

def get_logs(user_id):
    conn = get_connection() 
    cur = conn.cursor()

    # SQL code
    query = """
    SELECT * FROM emotion_logs
    WHERE user_id = %s
    """

    cur.execute(query, (user_id,))
    
    rows = cur.fetchall()
    

    logs = []

    for row in rows:
        # row[0] = log_id
        # row[1] = user_id
        # row[2] = label
        # row[3] = description
        # row[4] = date
        # row[5] = trigger
        # row[6] = intensity
        # row[7] = sleep_quality
        # row[8] = follow_up_qa

        log = emotion_log.EmotionLog(
            log_id=row[0],
            user_id=row[1],
            label=row[2],
            situation_description=row[3],
            log_date=row[4],
            perceived_trigger=row[5],
            intensity=row[6],
            sleep_quality=row[7],
            follow_up_qa=row[8]
        )
    
        logs.append(log)

    # close connection and cursor; return logs
    
    cur.close()
    conn.close()
    return logs


def save_log(log):
    # Takes an EmotionLog as a parameter. This method will take the given log and send it to the database using SQL queries and the data attached to the log. It will utilize sqlite3 to execute code to the sql database. Returns True if it succeeds, False if it fails along with what caused it to fail.
    return True

def update_log(log_id, updated_log):
    # Takes two parameters: The id for the log to update, and the EmotionLog that houses the data that will be used to update. Using SQL code, this method will update the rows and columns of the emotion log with id of log_id with the data stored in EmotionLog. Returns True if it succeeds, False if it fails along with what caused it to fail.
    return True

def delete_log(user_id, log_id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        query = """
        DELETE FROM emotion_logs
        WHERE user_id = %s AND log_id = %s
        """

        cur.execute(query, (user_id, log_id))
        if cur.rowcount == 0:
            conn.rollback()
            return False
        conn.commit()
        return True
    finally:
        cur.close()
        conn.close()

