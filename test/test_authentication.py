from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "controller"))
from authentication import user_exists, verify_password, create_user


def test_user_exists_returns_true_when_found(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = (True,)

    mocker.patch("authentication.get_connection", return_value=mock_conn)

    result = user_exists("alice")

    assert result is True


def test_user_exists_returns_false_when_not_found(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = (False,)

    mocker.patch("authentication.get_connection", return_value=mock_conn)

    result = user_exists("missing_user")

    assert result is False


def test_verify_password_returns_none_if_user_missing(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = None

    mocker.patch("authentication.get_connection", return_value=mock_conn)

    result = verify_password("alice", "secret")

    assert result is None


def test_verify_password_returns_user_id_when_password_matches(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = (7, "secret")

    mocker.patch("authentication.get_connection", return_value=mock_conn)

    result = verify_password("alice", "secret")

    assert result == 7


def test_verify_password_returns_none_when_password_does_not_match(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = (7, "secret")

    mocker.patch("authentication.get_connection", return_value=mock_conn)

    result = verify_password("alice", "wrong")

    assert result is None


def test_create_user_returns_user_id_and_commits(mocker):
    mock_conn = mocker.Mock()
    mock_cur = mocker.Mock()

    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = (11, "pw")

    mocker.patch("authentication.get_connection", return_value=mock_conn)

    result = create_user("new_user", "pw")

    assert result == 11
    mock_conn.commit.assert_called_once()
