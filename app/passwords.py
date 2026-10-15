"""The password rules, in one place. Used by registration, password change and the first-run admin."""

MIN_LENGTH = 8
MAX_LENGTH = 128

# Passwords attackers try first. A short password is only acceptable if it is not on this list.
COMMON = frozenset(
    {
        "password", "password1", "password12", "password123", "passw0rd", "p@ssw0rd", "p@ssword",
        "12345678", "123456789", "1234567890", "123123123", "987654321", "11111111", "00000000",
        "qwertyui", "qwertyuiop", "qwerty123", "1q2w3e4r", "1qaz2wsx", "zaq12wsx",
        "abc12345", "abcd1234", "iloveyou", "letmein1", "letmein123", "welcome1", "welcome123",
        "admin123", "administrator", "changeme", "trustno1", "football", "baseball", "sunshine",
        "princess", "whatever", "monkey123", "dragon123", "master123", "security", "toolkit123",
    }
)


def problem_with(password: str, username: str | None = None) -> str | None:
    """Return a message saying what is wrong with the password, or None if it is acceptable."""
    if len(password) < MIN_LENGTH:
        return f"Password must be at least {MIN_LENGTH} characters."
    if len(password) > MAX_LENGTH:
        return f"Password must be at most {MAX_LENGTH} characters."
    if password.lower() in COMMON or len(set(password)) == 1:
        return "That password is too common. Choose something less guessable."
    if username and password.lower() == username.lower():
        return "Password must not be the same as the username."
    return None