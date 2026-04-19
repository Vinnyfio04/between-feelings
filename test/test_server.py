from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from server import (
    app,
    get_user_logs,
    get_user_log,
    update_user_log,
    delete_user_log,
    create_user_log,
    generate_new_log_followup_questions,
    get_patterns_summary,
    user_exists,
    verify_password,
    create_user,
    chat,
    patterns_cache,
)


def test_get_user_logs_returns_list_of_dicts(mocker):
    log1 = mocker.Mock()
    log1.to_dict.return_value = {"log_id": 1, "label": "Happy"}
    log2 = mocker.Mock()
    log2.to_dict.return_value = {"log_id": 2, "label": "Calm"}

    mocker.patch("server.controller.get_logs", return_value=[log1, log2])

    with app.app_context():
        response = get_user_logs(1)

    assert response.get_json() == [
        {"log_id": 1, "label": "Happy"},
        {"log_id": 2, "label": "Calm"},
    ]


def test_get_user_log_returns_log_when_found(mocker):
    log = mocker.Mock()
    log.to_dict.return_value = {"log_id": 1, "label": "Happy"}
    mocker.patch("server.controller.get_log", return_value=log)

    with app.app_context():
        response = get_user_log(1, 1)

    assert response.get_json()["label"] == "Happy"


def test_get_user_log_returns_404_when_missing(mocker):
    mocker.patch("server.controller.get_log", return_value=None)

    with app.app_context():
        response, status = get_user_log(1, 99)

    assert status == 404
    assert response.get_json()["error"] == "not_found"


def test_update_user_log_returns_updated_true_on_success(mocker):
    existing_log = mocker.Mock()
    existing_log.label = "Happy"
    existing_log.description = "desc"
    existing_log.date = "2025-01-01"
    existing_log.trigger = "trigger"
    existing_log.intensity = 5
    existing_log.sleep_quality = "good"
    existing_log.follow_up_qa = "qa"

    mocker.patch("server.controller.get_log", return_value=existing_log)
    mocker.patch("server.controller.update_log", return_value=True)
    mocker.patch("server.controller.EmotionLog", side_effect=lambda **kwargs: mocker.Mock(**kwargs))

    with app.test_request_context(json={"label": "Updated"}):
        response = update_user_log(1, 1)

    assert response.get_json() == {"updated": True}


def test_update_user_log_returns_404_when_missing(mocker):
    mocker.patch("server.controller.get_log", return_value=None)

    with app.test_request_context(json={"label": "Updated"}):
        response, status = update_user_log(1, 1)

    assert status == 404
    assert response.get_json() == {"updated": False, "error": "not_found"}


def test_update_user_log_returns_400_when_update_fails(mocker):
    existing_log = mocker.Mock()
    existing_log.label = "Happy"
    existing_log.description = "desc"
    existing_log.date = "2025-01-01"
    existing_log.trigger = "trigger"
    existing_log.intensity = 5
    existing_log.sleep_quality = "good"
    existing_log.follow_up_qa = "qa"

    mocker.patch("server.controller.get_log", return_value=existing_log)
    mocker.patch("server.controller.update_log", return_value=False)
    mocker.patch("server.controller.EmotionLog", side_effect=lambda **kwargs: mocker.Mock(**kwargs))

    with app.test_request_context(json={"label": "Updated"}):
        response, status = update_user_log(1, 1)

    assert status == 400
    assert response.get_json() == {"updated": False}


def test_delete_user_log_returns_deleted_true_on_success(mocker):
    mocker.patch("server.controller.delete_log", return_value=True)
    thread_mock = mocker.Mock()
    thread_mock.start.return_value = None
    mocker.patch("server.threading.Thread", return_value=thread_mock)

    with app.app_context():
        response = delete_user_log(1, 1)

    assert response.get_json() == {"deleted": True}


def test_delete_user_log_returns_deleted_false_on_failure(mocker):
    mocker.patch("server.controller.delete_log", return_value=False)

    with app.app_context():
        response, status = delete_user_log(1, 1)

    assert status == 404
    assert response.get_json() == {"deleted": False}


def test_get_patterns_summary_returns_loading_when_cache_empty(mocker):
    patterns_cache.clear()
    thread_mock = mocker.Mock()
    thread_mock.start.return_value = None
    mocker.patch("server.threading.Thread", return_value=thread_mock)

    with app.app_context():
        response, status = get_patterns_summary(1)

    assert status == 202
    assert response.get_json() == {"status": "loading"}


def test_get_patterns_summary_returns_success_when_cached():
    patterns_cache.clear()
    patterns_cache[1] = {"status": "success", "data": {"summary": "ok"}, "error": None}

    with app.app_context():
        response, status = get_patterns_summary(1)

    assert status == 200
    assert response.get_json() == {"summary": "ok"}


def test_get_patterns_summary_returns_error_when_cached():
    patterns_cache.clear()
    patterns_cache[1] = {"status": "error", "data": None, "error": "failed"}

    with app.app_context():
        response, status = get_patterns_summary(1)

    assert status == 502
    assert response.get_json()["status"] == "error"


def test_user_exists_returns_exists_flag(mocker):
    mocker.patch("server.controller.user_exists", return_value=True)

    with app.app_context():
        response = user_exists("alice")

    assert response.get_json() == {"exists": True}


def test_verify_password_success_returns_user_id(mocker):
    mocker.patch("server.controller.verify_password", return_value=7)

    with app.app_context():
        response = verify_password("alice", "secret")

    assert response.get_json() == {"verified": True, "user_id": 7}


def test_verify_password_failure_returns_false(mocker):
    mocker.patch("server.controller.verify_password", return_value=None)

    with app.app_context():
        response = verify_password("alice", "wrong")

    assert response.get_json() == {"verified": False}


def test_create_user_returns_verified_and_user_id(mocker):
    mocker.patch("server.controller.create_user", return_value=11)

    with app.app_context():
        response = create_user("new_user", "pw")

    assert response.get_json() == {"verified": True, "user_id": 11}


def test_chat_returns_reply_on_success(mocker):
    mocker.patch("server.controller.generate_chat_text", return_value="Hello back")

    with app.test_request_context(json={"chat_input": "Hi"}):
        response = chat(1)

    assert response.get_json() == {"reply": "Hello back"}


def test_chat_returns_400_on_invalid_input():
    with app.test_request_context(json={"chat_input": ""}):
        response, status = chat(1)

    assert status == 400


def test_chat_returns_502_on_value_error(mocker):
    mocker.patch("server.controller.generate_chat_text", side_effect=ValueError("LLM fail"))

    with app.test_request_context(json={"chat_input": "Hi"}):
        response, status = chat(1)

    assert status == 502


def test_chat_returns_500_on_generic_exception(mocker):
    mocker.patch("server.controller.generate_chat_text", side_effect=Exception("Unexpected"))

    with app.test_request_context(json={"chat_input": "Hi"}):
        response, status = chat(1)

    assert status == 500


def test_generate_followup_questions_returns_questions(mocker):
    payload = {
        "label": "Happy",
        "description": "desc",
        "date": "2025-01-01",
        "trigger": "trigger",
        "intensity": 5,
        "sleep_quality": "good",
    }
    mocker.patch("server.controller.EmotionLog", side_effect=lambda **kwargs: mocker.Mock(**kwargs))
    mocker.patch("server.controller.generate_followup_questions", return_value=["q1", "q2"])

    with app.test_request_context(json=payload):
        response, status = generate_new_log_followup_questions(1)

    assert status == 200
    assert response.get_json() == {"questions": ["q1", "q2"]}


def test_generate_followup_questions_returns_400_on_invalid_payload():
    with app.test_request_context(json="bad"):
        response, status = generate_new_log_followup_questions(1)

    assert status == 400


def test_generate_followup_questions_returns_502_on_generation_error(mocker):
    payload = {
        "label": "Happy",
        "description": "desc",
        "date": "2025-01-01",
        "trigger": "trigger",
        "intensity": 5,
        "sleep_quality": "good",
    }
    mocker.patch("server.controller.EmotionLog", side_effect=lambda **kwargs: mocker.Mock(**kwargs))
    mocker.patch("server.controller.generate_followup_questions", side_effect=ValueError("bad model output"))

    with app.test_request_context(json=payload):
        response, status = generate_new_log_followup_questions(1)

    assert status == 502


def test_create_user_log_returns_saved_true_and_log_id(mocker):
    payload = {
        "label": "Happy",
        "description": "desc",
        "date": "2025-01-01",
        "trigger": "trigger",
        "intensity": 5,
        "sleep_quality": "good",
        "follow_up_qa": "qa",
    }
    mocker.patch("server.controller.EmotionLog", side_effect=lambda **kwargs: mocker.Mock(**kwargs))
    mocker.patch("server.controller.save_log", return_value=22)

    with app.test_request_context(json=payload):
        response, status = create_user_log(1)

    assert status == 201
    assert response.get_json() == {"saved": True, "log_id": 22}


def test_create_user_log_returns_400_when_save_fails(mocker):
    payload = {
        "label": "Happy",
        "description": "desc",
        "date": "2025-01-01",
        "trigger": "trigger",
        "intensity": 5,
        "sleep_quality": "good",
        "follow_up_qa": "qa",
    }
    mocker.patch("server.controller.EmotionLog", side_effect=lambda **kwargs: mocker.Mock(**kwargs))
    mocker.patch("server.controller.save_log", return_value=None)

    with app.test_request_context(json=payload):
        response, status = create_user_log(1)

    assert status == 400
    assert response.get_json()["saved"] is False


def test_create_user_log_returns_400_on_validation_error():
    payload = {
        "label": "Happy",
        "description": "desc",
        "date": "2025-01-01",
        "trigger": "trigger",
        "intensity": "5",
        "sleep_quality": "good",
        "follow_up_qa": "qa",
    }

    with app.test_request_context(json=payload):
        response, status = create_user_log(1)

    assert status == 400
