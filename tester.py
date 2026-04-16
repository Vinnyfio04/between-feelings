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
import emotion_log
import prompt_generation
import text_generation


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


    # Test emotion log stuff
    def test_emotion_log_to_string(self):
        titles = "\nLog ID | User ID | Label | Situation Description | Log Date | Perceived Trigger | Intensity | Sleep Quality | Follow-Up Q&A"
        log = emotion_log.EmotionLog(1, 1, "Anxious", "Before the meeting", "2025-01-01", "deadline", 8, "poor", "QA")
        # print(titles)
        # print(log)

    # Test prompt generation stuff
    def test_format_logs(self):
        logs = db_logging.get_logs(3)

        formatted_logs = prompt_generation._format_logs(logs)

        # print("")

        i = 0
        while i <= 3:
            # print(formatted_logs[i])
            i += 1

    def test_build_patterns_summary_prompt(self):
        logs = db_logging.get_logs(3)
        prompt = prompt_generation.build_patterns_summary_prompt(logs)
        # print(prompt)


class TestPatternSummaryJsonParsing(unittest.TestCase):
    @patch("text_generation.generate_text")
    @patch("text_generation.build_patterns_summary_prompt")
    def test_generate_patterns_summary_valid_json_returns_dict(
        self, mock_build_prompt, mock_generate_text
    ):
        log = emotion_log.EmotionLog(
            1, 1, "Anxious", "Before meeting", "2025-01-01", "deadline", 8, "poor", "QA"
        )
        mock_build_prompt.return_value = "prompt"
        mock_generate_text.return_value = (
            '{"hero_summary":"h","short_summary":"s","quick_insights":["i1"],"detailed_summary":"d"}'
        )

        result = text_generation.generate_patterns_summary(logs=[log])

        self.assertIsInstance(result, dict)
        self.assertEqual(result["hero_summary"], "h")

    @patch("text_generation.generate_text")
    @patch("text_generation.build_patterns_summary_prompt")
    def test_generate_patterns_summary_malformed_json_raises_value_error(
        self, mock_build_prompt, mock_generate_text
    ):
        log = emotion_log.EmotionLog(
            1, 1, "Anxious", "Before meeting", "2025-01-01", "deadline", 8, "poor", "QA"
        )
        mock_build_prompt.return_value = "prompt"
        mock_generate_text.return_value = '{"hero_summary": "h"'

        with self.assertRaisesRegex(ValueError, "not valid JSON"):
            text_generation.generate_patterns_summary(logs=[log])

    @patch("text_generation.generate_text")
    @patch("text_generation.build_patterns_summary_prompt")
    def test_generate_patterns_summary_empty_response_raises_value_error(
        self, mock_build_prompt, mock_generate_text
    ):
        log = emotion_log.EmotionLog(
            1, 1, "Anxious", "Before meeting", "2025-01-01", "deadline", 8, "poor", "QA"
        )
        mock_build_prompt.return_value = "prompt"
        mock_generate_text.return_value = "   "

        with self.assertRaisesRegex(ValueError, "empty"):
            text_generation.generate_patterns_summary(logs=[log])

    @patch("text_generation.generate_text")
    @patch("text_generation.build_patterns_summary_prompt")
    def test_generate_patterns_summary_missing_required_key_raises_value_error(
        self, mock_build_prompt, mock_generate_text
    ):
        log = emotion_log.EmotionLog(
            1, 1, "Anxious", "Before meeting", "2025-01-01", "deadline", 8, "poor", "QA"
        )
        mock_build_prompt.return_value = "prompt"
        mock_generate_text.return_value = (
            '{"hero_summary":"h","short_summary":"s","quick_insights":["i1"]}'
        )

        with self.assertRaisesRegex(ValueError, "missing required field"):
            text_generation.generate_patterns_summary(logs=[log])

    @patch("text_generation.generate_text")
    @patch("text_generation.build_patterns_summary_prompt")
    def test_generate_patterns_summary_non_dict_top_level_raises_value_error(
        self, mock_build_prompt, mock_generate_text
    ):
        log = emotion_log.EmotionLog(
            1, 1, "Anxious", "Before meeting", "2025-01-01", "deadline", 8, "poor", "QA"
        )
        mock_build_prompt.return_value = "prompt"
        mock_generate_text.return_value = '["not", "an", "object"]'

        with self.assertRaisesRegex(ValueError, "top level"):
            text_generation.generate_patterns_summary(logs=[log])

    @patch("text_generation.generate_text")
    @patch("text_generation.build_patterns_summary_prompt")
    def test_generate_patterns_summary_wrong_field_type_raises_value_error(
        self, mock_build_prompt, mock_generate_text
    ):
        log = emotion_log.EmotionLog(
            1, 1, "Anxious", "Before meeting", "2025-01-01", "deadline", 8, "poor", "QA"
        )
        mock_build_prompt.return_value = "prompt"
        mock_generate_text.return_value = (
            '{"hero_summary":"h","short_summary":"s","quick_insights":"not-a-list","detailed_summary":"d"}'
        )

        with self.assertRaisesRegex(ValueError, "must be of type list"):
            text_generation.generate_patterns_summary(logs=[log])


class TestFollowupPromptFormatting(unittest.TestCase):
    def test_build_followup_questions_prompt_uses_labeled_single_log_block(self):
        log = emotion_log.EmotionLog(
            user_id=99,
            log_id=42,
            label="Stressed",
            description="I felt overwhelmed before class.",
            date="2026-04-16",
            trigger="upcoming presentation",
            intensity=4,
            sleep_quality="Average",
            follow_up_qa="Q1: earlier note\nA1: response",
        )

        prompt = prompt_generation.build_followup_questions_prompt(log)

        self.assertIn("Label: Stressed", prompt)
        self.assertIn("Description: I felt overwhelmed before class.", prompt)
        self.assertIn("Date: 2026-04-16", prompt)
        self.assertIn("Trigger: upcoming presentation", prompt)
        self.assertIn("Intensity: 4", prompt)
        self.assertIn("Sleep Quality: Average", prompt)
        self.assertNotIn("42 | 99 |", prompt)
        self.assertNotIn("follow_up_qa", prompt)
        self.assertNotIn("Q1: earlier note", prompt)
        self.assertNotIn("A1: response", prompt)


if __name__ == "__main__":
    unittest.main()
