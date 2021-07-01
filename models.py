from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)


# Model
class Country(db.Model):
    __tablename__ = 'country'
    
    id = db.Column(db.Integer, primary_key=True)
    code3 = db.Column(db.String(3), unique=True)
    currency = db.Column(db.String(3))
    name = db.Column(db.String(80), unique=True)
    year = db.Column(db.Integer())
    ppp = db.Column(db.Numeric(2))
    
    
    def __repr__(self):
        return '<Country {0}>'.format(self.name)


class Config(db.Model):
    __tablename__ = 'config'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True)
    value = db.Column(db.String(80))

    def __repr__(self):
        return '<Config {0}: {1}>'.format(self.key, self.value)

