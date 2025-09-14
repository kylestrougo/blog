import sqlalchemy as sa
from app import db

class Post(db.Model):
    __tablename__ = "posts"

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(50), nullable=False)
    text = sa.Column(sa.Text, nullable=False)
    image_path = sa.Column(sa.String(255), nullable=True)  # stores filename
    created_at = sa.Column(sa.DateTime, nullable=False)