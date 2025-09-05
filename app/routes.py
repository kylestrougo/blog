from flask import render_template, redirect, url_for, request, flash
from app import app
from app.forms import LoginForm, PostForm
from datetime import datetime
import os
from werkzeug.utils import secure_filename

CORRECT_PASSWORD = "pass"

# Configurations
UPLOAD_FOLDER = 'app/static/uploads'   # folder where files will be saved
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/index')
def index():
    # Example posts
    posts = [
        {"username": "Alice", "date": "August 31, 2025",
         "text": "I found a tiny cafe this morning —\nthe light hit the counter just right.\nHot chocolate and a croissant,\nand somehow the world felt slower."},
        {"username": "Ben", "date": "September 1, 2025",
         "text": "Took the long route home tonight.\nThe city hums — fluorescent and alive.\nI sketched the idea for a tiny app:\na pocket notebook that actually listens."},
        {"username": "Ben", "date": "September 2, 2025",
         "text": "Took the long route home tonight.\nThe city hums — fluorescent and alive.\nI sketched the idea for a tiny app:\na pocket notebook that actually listens."}
    ]

    # Convert date strings to datetime objects for sorting
    for post in posts:
        post['date_obj'] = datetime.strptime(post['date'], "%B %d, %Y")

    # Sort posts by date descending (most recent first)
    posts.sort(key=lambda x: x['date_obj'], reverse=True)

    # Remove the temporary datetime object (optional)
    for post in posts:
        del post['date_obj']

    # Define colors per user
    user_colors = {
        "Alice": "#4B5320",  # Army Green
        "Ben": "#4B0082"     # Dark Purple
    }

    return render_template('index.html', title='Home', posts=posts, user_colors=user_colors)

@app.route('/')
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == CORRECT_PASSWORD:
            return redirect(url_for("index"))
        else:
            flash("Enter the correct password")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    filename = None
    post_data = None

    if request.method == 'POST':
        selected_user = request.form.get('selected_user')  # user1 or user2
        form.username.data = selected_user  # set hidden field

        if form.validate_on_submit():
            username = form.username.data
            text = form.text.data
            file = form.file.data
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            post_data = {
                "username": username,
                "text": text,
                "filename": filename,
                "date": current_time
            }

            return render_template('post.html', form=form, **post_data)

    return render_template('post.html', form=form)