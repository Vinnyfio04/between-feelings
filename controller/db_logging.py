import EmotionLog
import sqlite3

# Take user emotion log inputs and send it to the db

def save_log(log):
    # Takes an EmotionLog as a parameter. This method will take the given log and send it to the database using SQL queries and the data attached to the log. It will utilize sqlite3 to execute code to the sql database. Returns True if it succeeds, False if it fails along with what caused it to fail.
    return True

def update_log(log_id, updated_log):
    # Takes two parameters: The id for the log to update, and the EmotionLog that houses the data that will be used to update. Using SQL code, this method will update the rows and columns of the emotion log with id of log_id with the data stored in EmotionLog. Returns True if it succeeds, False if it fails along with what caused it to fail.
    return True

def get_logs(user_id):
    # Takes the user's id as a parameter. This method will use SQL queries to get every emotion log assigned to user_id and put them in a list of EmotionLogs. Returns the list of EmotionLogs.
    logs = []
    return logs

def get_log(log_id):
    # Takes an emotion log's id as a parameter. This method will use a SQL query to get one emotion log using its given id. Returns the datalog.
    log = EmotionLog(1, 1, "label", "description", "trigger", "intesity", "sleep quality", "1000-1-31")
    return log
