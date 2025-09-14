from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.forms import PostForm
from datetime import datetime
import pytz
import os
from werkzeug.utils import secure_filename
from app.models import Post
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CORRECT_PASSWORD = "WIZARD"

# Configurations
UPLOAD_FOLDER = 'app/static/uploads'   # folder where files will be saved
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def send_email(to_email, subject, body_html):
    sender = "chi.chi.masters1@gmail.com"
    password = "qxdl tort frwr odkr"

    # Multipart so we can support both plain text + HTML
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    # Add both plain text fallback and HTML
    text_fallback = "Your email client does not support HTML emails."
    part1 = MIMEText(text_fallback, "plain")
    part2 = MIMEText(body_html, "html")

    msg.attach(part1)
    msg.attach(part2)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())

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
        if password.upper() == CORRECT_PASSWORD:
            return redirect(url_for("index"))
        else:
            flash("Enter the correct password")
            return redirect(url_for("login"))
    return render_template("login.html")


# --- ROUTE ---
@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()

    if request.method == 'POST':
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
                image_path=filename,
                created_at=datetime.utcnow()
            )
            db.session.add(new_post)
            db.session.commit()

            # --- Render email from template ---
            site_link = "http://192.168.1.117:5000/"
            email_html = render_template("email.html", username=username, text=text, site_link=site_link)

            # --- Send to correct recipient ---
            if username == "Bug":
                send_email("kstrougo@gmail.com", f"New letter from {username}", email_html)
            elif username == "Dumbo":
                send_email("chichi.masters1@gmail.com", f"New letter from {username}", email_html)

            return redirect(url_for('index'))
        else:
            flash("Error: " + str(form.errors), "danger")

    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('post.html', form=form, posts=posts)
