from pathlib import Path
import json
import time
import sys
import threading

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
    InvalidFollowupQuestionsError,
)



app = Flask(__name__)
CORS(app) # Enable CORS for the app, prevent browser from blocking requests from different origins

# Helper function to generate patterns in the background; caches the result.
patterns_cache = {}
def refresh_pattern(user_id: int):
    patterns_cache[user_id] = {"status": "loading", "data": None, "error": None}
    try:
        data = controller.generate_patterns_summary(user_id=user_id)
        patterns_cache[user_id] = {"status": "success", "data": data, "error": None}
    except Exception as e:
        patterns_cache[user_id] = {"status": "error", "data": None, "error": str(e)}


def _validate_new_log_payload(payload: dict, user_id: int, require_follow_up_qa: bool):
    required_keys = {
        "log_id",
        "label",
        "description",
        "date",
        "trigger",
        "intensity",
        "sleep_quality",
    }
    if require_follow_up_qa:
        required_keys.add("follow_up_qa")

    missing_keys = sorted([key for key in required_keys if key not in payload])
    if missing_keys:
        return None, {
            "error": "bad_request",
            "message": f"Missing required field(s): {', '.join(missing_keys)}.",
        }

    if not isinstance(payload["log_id"], int):
        return None, {"error": "bad_request", "message": "log_id must be an integer."}
    if not isinstance(payload["label"], str) or not payload["label"].strip():
        return None, {"error": "bad_request", "message": "label must be a non-empty string."}
    if not isinstance(payload["description"], str) or not payload["description"].strip():
        return None, {"error": "bad_request", "message": "description must be a non-empty string."}
    if not isinstance(payload["date"], str) or not payload["date"].strip():
        return None, {"error": "bad_request", "message": "date must be a non-empty string."}
    if not isinstance(payload["trigger"], str) or not payload["trigger"].strip():
        return None, {"error": "bad_request", "message": "trigger must be a non-empty string."}
    if not isinstance(payload["intensity"], int):
        return None, {"error": "bad_request", "message": "intensity must be an integer."}
    if not isinstance(payload["sleep_quality"], str) or not payload["sleep_quality"].strip():
        return None, {"error": "bad_request", "message": "sleep_quality must be a non-empty string."}

    follow_up_qa = ""
    if require_follow_up_qa:
        if not isinstance(payload["follow_up_qa"], str):
            return None, {"error": "bad_request", "message": "follow_up_qa must be a string."}
        follow_up_qa = payload["follow_up_qa"].strip()
    # TEMP WORKAROUND: log_id is frontend-provided because current save path requires it.
    log = controller.EmotionLog(
        log_id=payload["log_id"],
        user_id=user_id,
        label=payload["label"].strip(),
        description=payload["description"].strip(),
        date=payload["date"].strip(),
        trigger=payload["trigger"].strip(),
        intensity=payload["intensity"],
        sleep_quality=payload["sleep_quality"].strip(),
        follow_up_qa=follow_up_qa,
    )
    return log, None


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
        result = patterns_cache.get(user_id)


        if result is None:
            threading.Thread(target=refresh_pattern, args=(user_id,), daemon=True).start()
            return jsonify({"status": "loading"}), 202
       
        if result["status"] == "loading":
            return jsonify({"status": "loading"}), 202


        if result["status"] == "success":
            return jsonify(result["data"]), 200


        if result["status"] == "error":
            return jsonify({"status": "error", "message": result.get("error", "Pattern generation failed.")}), 502
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
    threading.Thread(target=refresh_pattern, args=(user_id,), daemon=True).start() # Refresh the pattern cache when a log is deleted
    return jsonify({"deleted": True})


@app.post("/logs/<int:user_id>/followup-questions")
def generate_new_log_followup_questions(user_id: int):
    if user_id <= 0:
        return jsonify({
            "error": "invalid_user_id",
            "message": "user_id must be a positive integer",
        }), 400

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({
            "error": "bad_request",
            "message": "Expected JSON object for new log payload.",
        }), 400

    log, validation_error = _validate_new_log_payload(payload, user_id, require_follow_up_qa=False)
    if validation_error is not None:
        return jsonify(validation_error), 400

    try:
        questions = controller.generate_followup_questions(log)
        return jsonify({"questions": questions}), 200
    except (InvalidFollowupQuestionsError, ValueError) as exc:
        return jsonify({
            "error": "followup_generation_failed",
            "message": f"Follow-up question generation failed: {str(exc)}",
        }), 502
    except Exception as exc:
        return jsonify({
            "error": "internal_error",
            "message": f"Unexpected internal error: {str(exc)}",
        }), 500


@app.post("/logs/<int:user_id>")
def create_user_log(user_id: int):
    if user_id <= 0:
        return jsonify({
            "error": "invalid_user_id",
            "message": "user_id must be a positive integer",
        }), 400

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({
            "error": "bad_request",
            "message": "Expected JSON object for completed new log payload.",
        }), 400

    log, validation_error = _validate_new_log_payload(payload, user_id, require_follow_up_qa=True)
    if validation_error is not None:
        return jsonify(validation_error), 400

    # Minimal validation for now: stronger completion checks depend on a finalized
    # frontend follow_up_qa string format contract.
    if not log.follow_up_qa.strip():
        return jsonify({
            "error": "bad_request",
            "message": "follow_up_qa must be a non-empty string.",
        }), 400

    try:
        saved = controller.save_log(log)
        if not saved:
            return jsonify({
                "saved": False,
                "error": "save_failed",
                "message": "Failed to save completed log.",
            }), 400
        return jsonify({"saved": True, "log_id": log.log_id}), 201
    except Exception as exc:
        return jsonify({
            "error": "internal_error",
            "message": f"Unexpected internal error: {str(exc)}",
        }), 500

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

@app.post("/chat/<int:user_id>")
def chat(user_id: int):
    if user_id <= 0:
        return jsonify({
            "error": "invalid_user_id",
            "message": "user_id must be a positive integer",
        }), 400

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({
            "error": "bad_request",
            "message": "Expected JSON object with non-empty string field 'chat_input'.",
        }), 400

    chat_input = payload.get("chat_input")
    if not isinstance(chat_input, str) or not chat_input.strip():
        return jsonify({
            "error": "bad_request",
            "message": "chat_input must be a non-empty string.",
        }), 400

    trimmed_input = chat_input.strip()

    try:
        reply = controller.generate_chat_text(chat_input=trimmed_input, user_id=user_id)
        return jsonify({"reply": reply})
    except ValueError as exc:
        return jsonify({
            "error": "llm_failure",
            "message": f"Chat generation failed: {str(exc)}",
        }), 502
    except Exception as exc:
        return jsonify({
            "error": "internal_error",
            "message": f"Unexpected internal error: {str(exc)}",
        }), 500

if __name__ == "__main__":
    app.run(debug=True) # Run the app in debug mode, allow for automatic reloading of the server when code changes are made
