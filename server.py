from pathlib import Path
import sys

from flask import Flask, jsonify # Python Flask module for creating a web application
from flask_cors import CORS # Python Flask CORS module for enabling Cross-Origin Resource Sharing


PROJECT_ROOT = Path(__file__).resolve().parent # Path to the project root directory for code reuse
CONTROLLER_DIR = PROJECT_ROOT / "controller"

if str(CONTROLLER_DIR) not in sys.path: # If the controller directory is not in the system path, add it to the system path
    sys.path.insert(0, str(CONTROLLER_DIR))

import controller  # noqa: E402 # Import the controller module in order to gain access to get_logs function



app = Flask(__name__)
CORS(app) # Enable CORS for the app, prevent browser from blocking requests from different origins


@app.get("/logs/<int:user_id>") # Define a route for the get_user_logs function
def get_user_logs(user_id: int):
    logs = controller.get_logs(user_id)
    return jsonify([log.to_dict() for log in logs])


@app.delete("/logs/<int:user_id>/<int:log_id>")
def delete_user_log(user_id: int, log_id: int):
    deleted = controller.delete_log(user_id, log_id)
    if not deleted:
        return jsonify({"deleted": False}), 404
    return jsonify({"deleted": True})

@app.get("/authentication/user_exists/<string:username>")
def user_exists(username: str):
    exists = controller.user_exists(username)
    return jsonify({"exists": exists})

@app.get("/authentication/verify_password/<string:username>/<string:password>")
def verify_password(username: str, password: str):
    user_id = controller.verify_password(username, password)
    if user_id is None:
        return jsonify({"verified": False})
    return jsonify({"verified": True, "user_id": user_id}) # Return user ID of the user that logged in successfully


if __name__ == "__main__":
    app.run(debug=True) # Run the app in debug mode, allow for automatic reloading of the server when code changes are made
