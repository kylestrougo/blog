from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SubmitField, HiddenField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class PostForm(FlaskForm):
    username = HiddenField(validators=[DataRequired()])  # Will store 'user1' or 'user2'
    text = TextAreaField('Your Post', validators=[DataRequired()], render_kw={"rows": 4})
    file = FileField('File', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')])
    submit = SubmitField('Submit')