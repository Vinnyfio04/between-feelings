# Methods to check user input

def user_exists(username, demo):
    # user_exists() is a method that will be called when the username submit button in authentication.html is pressed..
    # It checks to see if it EXISTS in the SQL database.
    # It returns True if the username does exist in the db, False if it doesn't exist.
    # DEMO is a placeholder for the username in the SQL database
    return username == demo

def verify_password(username, demo):
    # user_exists() is a method that takes a string input and will be called when the password submit button in authentication.html is pressed.
    # It assigns a password variable to the output from getPasswordInput().
    # Username is used in SQL code to retrieve the password associated with the username and assigns it to correctPassword variable
    # return if password === correctPassword (true if password matches, False if not)
    # DEMO is a placeholder for the password in the SQL database
    return username == demo

def create_user(username, password):
    # create_user() is a method that takes two parameters: a string username that holds the username input, and a string password that holds the password input
    # It is called in authentication.html when the username input does not exist in the db.
    # It takes the two parameters and sends SQL code that adds the user to the authentication table in the database
    # Returns True if it was successfully created, False if there was an error
    return True