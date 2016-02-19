from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://yourface:rocks@localhost/yourfaceDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
admin = Admin(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password_hash = db.Column(db.String(60), nullable=False)
    first_name_kr = db.Column(db.String(50), nullable=False)
    last_name_kr = db.Column(db.String(50), nullable=False)
    first_name_en = db.Column(db.String(50), nullable=False)
    middle_name_en = db.Column(db.String(50))
    last_name_en = db.Column(db.String(50), nullable=False)
    student_number = db.Column(db.Integer, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, password_hash, first_name_kr, last_name_kr, first_name_en, middle_name_en, last_name_en, student_number, last_login):
        self.username = username
        self.password_hash = password_hash
        self.first_name_kr = first_name_kr
        self.last_name_kr = last_name_kr
        self.first_name_en = first_name_en
        self.middle_name_en = middle_name_en
        self.last_name_en = last_name_en
        self.student_number = student_number
        self.last_login = last_login

    def __repr__(self):
        return '<User %r>' % self.username

admin.add_view(ModelView(User,db.session))

@app.route("/hello")
def hello():
    ha=bcrypt.generate_password_hash('asdf')
    return str(type(ha)) + str(len(ha)) + " " + str(ha)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
