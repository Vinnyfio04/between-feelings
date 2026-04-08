from pathlib import Path
import json
import time
import sys

from flask import Flask, jsonify, request # Python Flask module for creating a web application
from flask_cors import CORS # Python Flask CORS module for enabling Cross-Origin Resource Sharing


PROJECT_ROOT = Path(__file__).resolve().parent # Path to the project root directory for code reuse
CONTROLLER_DIR = PROJECT_ROOT / "controller"

if str(CONTROLLER_DIR) not in sys.path: # If the controller directory is not in the system path, add it to the system path
    sys.path.insert(0, str(CONTROLLER_DIR))

import controller  # noqa: E402 # Import the controller module in order to gain access to get_logs function
from text_generation import (  # noqa: E402
    NoLogsAvailableError,
    InvalidLLMJsonError,
    LLMResponseError,
)



app = Flask(__name__)
CORS(app) # Enable CORS for the app, prevent browser from blocking requests from different origins


@app.get("/logs/<int:user_id>") # Define a route for the get_user_logs function
def get_user_logs(user_id: int):
    logs = controller.get_logs(user_id)
    return jsonify([log.to_dict() for log in logs])

@app.get("/logs/<int:user_id>/<int:log_id>")
def get_user_log(user_id: int, log_id: int):
    log = controller.get_log(user_id, log_id)
    if log is None:
        return jsonify({"error": "not_found", "message": "Log not found"}), 404
    return jsonify(log.to_dict())

@app.put("/logs/<int:user_id>/<int:log_id>")
def update_user_log(user_id: int, log_id: int):
    existing_log = controller.get_log(user_id, log_id)
    if existing_log is None:
        return jsonify({"updated": False, "error": "not_found"}), 404

    payload = request.get_json(silent=True) or {}
    updated_log = controller.EmotionLog(
        log_id=log_id,
        user_id=user_id,
        label=payload.get("label", existing_log.label),
        description=payload.get("description", existing_log.description),
        date=payload.get("date", existing_log.date),
        trigger=payload.get("trigger", existing_log.trigger),
        intensity=payload.get("intensity", existing_log.intensity),
        sleep_quality=payload.get("sleep_quality", existing_log.sleep_quality),
        follow_up_qa=payload.get("follow_up_qa", existing_log.follow_up_qa),
    )
    updated = controller.update_log(log_id, updated_log)
    if not updated:
        return jsonify({"updated": False}), 400
    return jsonify({"updated": True})


@app.get("/patterns/<int:user_id>")
def get_patterns_summary(user_id: int):
    if user_id <= 0:
        return jsonify({
            "error": "invalid_user_id",
            "message": "user_id must be a positive integer",
        }), 400

    try:
        result = controller.generate_patterns_summary(user_id=user_id)
        # region agent log
        try:
            with open("/Users/jacoblee/Desktop/3.2/hcdd412/between-feelings/.cursor/debug-71f2c0.log", "a", encoding="utf-8") as _f:
                _f.write(json.dumps({
                    "sessionId": "71f2c0",
                    "runId": "post-fix",
                    "hypothesisId": "H6",
                    "location": "server.py:get_patterns_summary",
                    "message": "patterns route success",
                    "data": {"user_id": user_id},
                    "timestamp": int(time.time() * 1000),
                }) + "\n")
        except Exception:
            pass
        # endregion
        return jsonify(result)
    except NoLogsAvailableError:
        return jsonify({
            "error": "no_logs_available",
            "message": "No logs available for this user",
        }), 404
    except InvalidLLMJsonError as exc:
        # region agent log
        print(f"[DEBUG InvalidLLMJsonError] {exc}")
        try:
            with open("/Users/jacoblee/Desktop/3.2/hcdd412/between-feelings/.cursor/debug-71f2c0.log", "a", encoding="utf-8") as _f:
                _f.write(json.dumps({
                    "sessionId": "71f2c0",
                    "runId": "post-fix",
                    "hypothesisId": "H6",
                    "location": "server.py:get_patterns_summary",
                    "message": "patterns route invalid_llm_json",
                    "data": {"user_id": user_id, "error": str(exc)},
                    "timestamp": int(time.time() * 1000),
                }) + "\n")
        except Exception:
            pass
        # endregion
        return jsonify({
            "error": "invalid_llm_json",
            "message": f"Model returned malformed or schema-invalid JSON: {str(exc)}",
        }), 502
    except LLMResponseError as exc:
        # region agent log
        print(f"[DEBUG LLMResponseError] {exc}")
        try:
            with open("/Users/jacoblee/Desktop/3.2/hcdd412/between-feelings/.cursor/debug-71f2c0.log", "a", encoding="utf-8") as _f:
                _f.write(json.dumps({
                    "sessionId": "71f2c0",
                    "runId": "post-fix",
                    "hypothesisId": "H6",
                    "location": "server.py:get_patterns_summary",
                    "message": "patterns route llm_failure",
                    "data": {"user_id": user_id, "error": str(exc)},
                    "timestamp": int(time.time() * 1000),
                }) + "\n")
        except Exception:
            pass
        # endregion
        return jsonify({
            "error": "llm_failure",
            "message": f"Pattern summary generation failed: {str(exc)}",
        }), 502
    except Exception as exc:
        # region agent log
        print(f"[DEBUG Exception] {exc}")
        try:
            with open("/Users/jacoblee/Desktop/3.2/hcdd412/between-feelings/.cursor/debug-71f2c0.log", "a", encoding="utf-8") as _f:
                _f.write(json.dumps({
                    "sessionId": "71f2c0",
                    "runId": "post-fix",
                    "hypothesisId": "H6",
                    "location": "server.py:get_patterns_summary",
                    "message": "patterns route internal_error",
                    "data": {"user_id": user_id, "error": str(exc)},
                    "timestamp": int(time.time() * 1000),
                }) + "\n")
        except Exception:
            pass
        # endregion
        return jsonify({
            "error": "internal_error",
            "message": f"Unexpected internal error: {str(exc)}",
        }), 500


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

@app.post("/authentication/create_user/<string:username>/<string:password>")
def create_user(username: str, password: str):
    user_id = controller.create_user(username, password)
    return jsonify({"verified": True, "user_id": user_id})

if __name__ == "__main__":
    app.run(debug=True) # Run the app in debug mode, allow for automatic reloading of the server when code changes are made
