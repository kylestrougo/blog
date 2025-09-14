from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, HiddenField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class PostForm(FlaskForm):
    username = HiddenField(validators=[DataRequired()])  # Hardcoded via buttons
    text = TextAreaField('Your Post', validators=[DataRequired()], render_kw={"rows": 4})
    file = FileField('Upload Image (optional)', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')])
    submit = SubmitField('Submit')