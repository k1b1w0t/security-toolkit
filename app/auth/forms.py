from flask import g
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, ValidationError

from .. import passwords


def _strip(value):
    return value.strip() if isinstance(value, str) else value


class LoginForm(FlaskForm):
    username = StringField("Username", filters=[_strip], validators=[DataRequired(), Length(max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=passwords.MAX_LENGTH)])


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        filters=[_strip],
        validators=[
            DataRequired(message="Username is required."),
            Length(min=3, max=50, message="Username must be 3-50 characters."),
            Regexp(r"^[A-Za-z0-9_]+$", message="Use only letters, numbers and underscores."),
        ],
    )
    password = PasswordField("Password", validators=[DataRequired(message="Password is required.")])
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired(message="Please confirm your password."), EqualTo("password", message="Passwords must match.")],
    )

    def validate_password(self, field):
        problem = passwords.problem_with(field.data, self.username.data)
        if problem:
            raise ValidationError(problem)


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current password",
        validators=[DataRequired(message="Enter your current password."), Length(max=passwords.MAX_LENGTH)],
    )
    new_password = PasswordField("New password", validators=[DataRequired(message="New password is required.")])
    confirm_password = PasswordField(
        "Confirm new password",
        validators=[DataRequired(message="Please confirm your new password."), EqualTo("new_password", message="Passwords must match.")],
    )

    def validate_new_password(self, field):
        if field.data == self.current_password.data:
            raise ValidationError("New password must be different from the current one.")
        user = g.get("user")
        problem = passwords.problem_with(field.data, user["username"] if user else None)
        if problem:
            raise ValidationError(problem)