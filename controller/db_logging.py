import os
from typing import List

import psycopg
from dotenv import load_dotenv
from emotion_log import EmotionLog

load_dotenv()

def get_connection():
    # Centralize connection creation so environment/config changes happen in one place.
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
            description=row[3],
            date=row[4],
            trigger=row[5],
            intensity=row[6],
            sleep_quality=row[7],
            follow_up_qa=row[8]
        )
    
        logs.append(log)

    # close connection and cursor; return logs
    
    cur.close()
    conn.close()
    return logs


def get_log(user_id: int, log_id: int):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT * FROM emotion_logs
    WHERE user_id = %s AND log_id = %s
    """

    cur.execute(query, (user_id, log_id))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        return None

    return EmotionLog(
        log_id=row[0],
        user_id=row[1],
        label=row[2],
        description=row[3],
        date=row[4],
        trigger=row[5],
        intensity=row[6],
        sleep_quality=row[7],
        follow_up_qa=row[8],
    )


def save_log(log: EmotionLog) -> bool:
    conn = get_connection()
    cur = conn.cursor()

    try:
        query = """
        INSERT INTO emotion_logs (
            log_id,
            user_id,
            label,
            description,
            date,
            trigger,
            intensity,
            sleep_quality,
            follow_up_qa
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cur.execute(
            query,
            (
                log.log_id,
                log.user_id,
                log.label,
                log.description,
                log.date,
                log.trigger,
                log.intensity,
                log.sleep_quality,
                log.follow_up_qa,
            ),
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def update_log(log_id: int, updated_log: EmotionLog) -> bool:
    conn = get_connection()
    cur = conn.cursor()

    try:
        query = """
        UPDATE emotion_logs
        SET
            label = %s,
            description = %s,
            date = %s,
            trigger = %s,
            intensity = %s,
            sleep_quality = %s,
            follow_up_qa = %s
        WHERE log_id = %s AND user_id = %s
        """

        cur.execute(
            query,
            (
                updated_log.label,
                updated_log.description,
                updated_log.date,
                updated_log.trigger,
                updated_log.intensity,
                updated_log.sleep_quality,
                updated_log.follow_up_qa,
                log_id,
                updated_log.user_id,
            ),
        )
        if cur.rowcount == 0:
            # REF(HCDD-130): treat "no rows touched" as a failed update to avoid
            # reporting success when log_id/user_id does not match an owned record.
            conn.rollback()
            return False
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

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

