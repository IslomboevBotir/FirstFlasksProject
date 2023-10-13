from flask_sqlalchemy import SQLAlchemy

from settings import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://projectdb:projectdb@localhost/projectdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
