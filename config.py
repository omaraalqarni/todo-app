import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))


# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://omar:omar@db:5432/todo-app'