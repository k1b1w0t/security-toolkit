import pytest

from app import passwords


@pytest.mark.parametrize("pw", ["", "short", "1234567"])
def test_too_short(pw):
    assert "at least" in passwords.problem_with(pw)


def test_too_long():
    assert "at most" in passwords.problem_with("ab" * 65)


@pytest.mark.parametrize("pw", ["password", "Password", "12345678", "qwertyui", "aaaaaaaa"])
def test_common_passwords_rejected(pw):
    assert "common" in passwords.problem_with(pw)


def test_username_rejected():
    assert "username" in passwords.problem_with("MyUserName", "myusername")


@pytest.mark.parametrize("pw", ["tr0ub4dor", "blue-train-4", "x9!kQ2#m"])
def test_acceptable_passwords(pw):
    assert passwords.problem_with(pw, "alice") is None