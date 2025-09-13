from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.forms import PostForm
from datetime import datetime
import pytz
import os
from werkzeug.utils import secure_filename
from app.models import Post

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
    # Fetch posts from database ordered by most recent first
    posts = Post.query.order_by(Post.created_at.desc()).all()

    # Convert UTC timestamps to local time
    local_tz = pytz.timezone('America/New_York')  # Replace with your timezone
    for post in posts:
        if post.created_at.tzinfo is None:
            # If timestamp is naive (no timezone), assume it's UTC
            post.created_at = pytz.utc.localize(post.created_at)
        post.created_at = post.created_at.astimezone(local_tz)

    # Define colors per user (extend as needed)
    user_colors = {
        "Dumbo": "#4B5320",  # Army Green
        "Bug": "#4B0082"  # Dark Purple
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

    if request.method == 'POST':
        # Get username from hidden field
        selected_user = form.username.data

        if form.validate_on_submit():
            if not selected_user:
                flash("Please select a username!", "danger")
                return redirect(url_for('post'))

            username = selected_user
            text = form.text.data
            file = form.file.data
            filename = None

            # Handle optional file upload
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Save post to DB
            new_post = Post(
                username=username,
                text=text,
                image_path=filename,  # store only filename
                created_at=datetime.utcnow()
            )
            db.session.add(new_post)
            db.session.commit()

            #flash("Post successfully created!", "success")
            return redirect(url_for('index'))
        else:
            flash("Error: " + str(form.errors), "danger")

    # Query latest posts to display on page
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('post.html', form=form, posts=posts)