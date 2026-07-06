from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
)

from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)


class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=30),
        ],
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8),
        ],
    )

    confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password"),
        ],
    )

    submit = SubmitField("Create Account")