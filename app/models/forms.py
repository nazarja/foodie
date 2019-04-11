from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class SignForm(FlaskForm):
    """
        Flask WTF_Forms was only used for user sign in and sign up.
        Required fields are validated with DataRequired() and
        additional validation is limited to providing a username and
        password no shorter than 4 characters.
    """

    # Fields - require some validation
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Submit')

    # username
    def validate_username(self, username):
        if len(username.data) < 4:
            raise ValidationError('username must be longer than 4 characters')

    # password
    def validate_password(self, password):
        if len(password.data) < 4:
            raise ValidationError('password must be longer than 4 characters')



