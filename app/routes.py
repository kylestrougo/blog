from flask import render_template, redirect, url_for
from app import app
from app.forms import LoginForm
from datetime import datetime

@app.route('/')
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

