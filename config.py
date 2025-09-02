import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SERVER_NAME = '192.168.1.117:5000' # Replace with your server's hostname and port
    APPLICATION_ROOT = '/' # Set if your app is hosted under a subpath
    PREFERRED_URL_SCHEME = 'https'