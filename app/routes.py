from flask import render_template, redirect, url_for, request, flash
from app import app
from app.forms import LoginForm
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
    filename = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('post.html', filename=filename)
    return render_template('post.html', filename=filename)
