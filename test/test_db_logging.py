# testing the db_logging module
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "controller"))
from db_logging import get_log, get_logs, save_log, update_log, delete_log
from emotion_log import EmotionLog

# Pure logic test
def test_get_logs_converts_rows_to_objects(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchall.return_value = [
        (1, 2, "Happy", "Test desc", "2025-01-01", "trigger", 5, "good", "qa")
    ]

    mocker.patch("db_logging.get_connection", return_value=mock_conn)

    logs = get_logs(2)

    assert len(logs) == 1
    assert logs[0].label == "Happy"
    assert logs[0].intensity == 5


# Controller-style tests
def test_get_log_returns_none_if_not_found(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = None

    mocker.patch("db_logging.get_connection", return_value=mock_conn)

    result = get_log(user_id=1, log_id=999)

    assert result is None

def test_get_log_returns_object(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = (
        1, 1, "Anxious", "desc", "2025-01-01", "deadline", 8, "poor", "qa"
    )

    mocker.patch("db_logging.get_connection", return_value=mock_conn)

    result = get_log(1, 1)

    assert result.label == "Anxious"

# Database operation tests

def test_save_log_success(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.execute.return_value = None
    mock_cur.fetchone.return_value = (123,)

    mocker.patch("db_logging.get_connection", return_value=mock_conn)

    log = EmotionLog(1, 1, "Happy", "desc", "2025", "trigger", 5, "good", "qa")

    result = save_log(log)

    assert result == 123
    mock_conn.commit.assert_called_once()
    mock_conn.rollback.assert_not_called()

def test_save_log_success_with_very_long_description(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.execute.return_value = None
    mock_cur.fetchone.return_value = (124,)

    mocker.patch("db_logging.get_connection", return_value=mock_conn)

    long_description = "test " * 1000
    log = EmotionLog(1, 1, "Happy", long_description, "2025", "trigger", 5, "good", "qa")

    result = save_log(log)

    assert result == 124
    mock_conn.commit.assert_called_once()
    mock_conn.rollback.assert_not_called()

def test_save_log_failure_rolls_back(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.execute.side_effect = Exception("DB error")

    mocker.patch("db_logging.get_connection", return_value=mock_conn)

    log = EmotionLog(1, 1, "Happy", "desc", "2025", "trigger", 5, "good", "qa")

    result = save_log(log)

    assert result is None
    mock_conn.rollback.assert_called_once()

def test_update_log_success(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.rowcount = 1  # simulate successful update

    mocker.patch("db_logging.get_connection", return_value=mock_conn)

    updated_log = EmotionLog(1, 1, "Updated", "desc", "2025", "trigger", 5, "good", "qa")

    result = update_log(1, updated_log)

    assert result is True
    mock_conn.commit.assert_called_once()

def test_update_log_no_rows_updated(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.rowcount = 0  # simulate failure

    mocker.patch("db_logging.get_connection", return_value=mock_conn)

    updated_log = EmotionLog(1, 1, "Updated", "desc", "2025", "trigger", 5, "good", "qa")

    result = update_log(1, updated_log)

    assert result is False
    mock_conn.rollback.assert_called_once()

def test_delete_log_success(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.rowcount = 1  # simulate successful delete

    mocker.patch("db_logging.get_connection", return_value=mock_conn)

    result = delete_log(1, 1)

    assert result is True
    mock_conn.commit.assert_called_once()

def test_delete_log_no_rows(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.rowcount = 0  # simulate failure

    mocker.patch("db_logging.get_connection", return_value=mock_conn)

    result = delete_log(1, 1)

    assert result is False
    mock_conn.rollback.assert_called_once()