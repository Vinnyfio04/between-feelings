import os
from typing import List

import psycopg
from dotenv import load_dotenv
from emotion_log import EmotionLog

load_dotenv()

def get_connection():
    return psycopg.connect(
        os.environ["DATABASE_URL"]
    )



def get_logs(user_id: int) -> List[EmotionLog]:
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

        log = EmotionLog(
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


def save_log(log: EmotionLog) -> bool:
    # Placeholder: insert one EmotionLog into the database.
    return True

def update_log(log_id: int, updated_log: EmotionLog) -> bool:
    # Placeholder: update one EmotionLog row by log_id.
    return True

def delete_log(user_id: int, log_id: int) -> bool:
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

