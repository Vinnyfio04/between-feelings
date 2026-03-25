"""
Combined unit tests for the controller layer.
Run from project root: python tester.py
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# `controller/` holds authentication.py, controller.py, db_logging.py, etc.
CONTROLLER_DIR = Path(__file__).resolve().parent / "controller"
if str(CONTROLLER_DIR) not in sys.path:
    sys.path.insert(0, str(CONTROLLER_DIR))

import authentication as auth
import controller as c
import db_logging


class TestAuthentication(unittest.TestCase):
    @patch("authentication.get_connection")
    def test_user_exists_returns_true_when_username_found(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.fetchone.return_value = (True,)

        exists = auth.user_exists("demo_user")

        self.assertTrue(exists)
        mock_cur.execute.assert_called_once()

    def test_user_exists_true(self):
        assert auth.user_exists("JohnDoe") == True

    def test_user_exists_false(self):
        assert auth.user_exists("EvilUser") == False


class TestController(unittest.TestCase):
    def test_get_logs(self):
        rows = c.get_logs(3)


class TestDbLogging(unittest.TestCase):
    @patch("db_logging.get_connection")
    def test_get_logs_returns_emotion_logs_for_rows(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.fetchall.return_value = [
            (
                10,
                3,
                "Anxious",
                "Before the meeting",
                "2025-01-01",
                "deadline",
                8,
                "poor",
                "QA",
            ),
        ]

        logs = db_logging.get_logs(3)

        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].log_id, 10)
        self.assertEqual(logs[0].user_id, 3)
        self.assertEqual(logs[0].label, "Anxious")
        self.assertEqual(logs[0].situation_description, "Before the meeting")
        self.assertEqual(logs[0].log_date, "2025-01-01")
        self.assertEqual(logs[0].perceived_trigger, "deadline")
        self.assertEqual(logs[0].intensity, 8)
        self.assertEqual(logs[0].sleep_quality, "poor")
        self.assertEqual(logs[0].follow_up_qa, "QA")
        mock_cur.execute.assert_called_once()
        mock_cur.close.assert_called_once()
        mock_conn.close.assert_called_once()

    # Add tests for save_log, update_log, and delete_log as they get implemented



if __name__ == "__main__":
    unittest.main()
