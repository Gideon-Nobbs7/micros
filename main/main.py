from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_cors import CORS
# from routers import router


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nmf.db"
CORS(app)


db = SQLAlchemy(app)



class Fare(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    location = db.Column(db.String(200))
    price = db.Column(db.Integer)
    difficulty = db.Column(db.String(200))


class FarePayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    fare_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'fare_id', name='user_fare_uq')
    


@app.route("/hello", methods=["GET"])
def index():
    return "Hello"



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port=5000, debug=True)