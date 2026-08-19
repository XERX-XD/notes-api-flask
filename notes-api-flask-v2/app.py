from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "some-secret-key-change-this-later"
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
#signup
@app.route("/signup",methods=["POST"])
def signup():
    data = request.get_json()
    user = User(username=data["username"],password_hash=generate_password_hash(data["password"]))
    db.session.add(user)
    db.session.commit()
    return jsonify({"Status":"user added "})
#login
@app.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password_hash,data["password"]):
        print("correct")
        token = create_access_token(identity=str(user.id))
        return jsonify({"access_token":token})
    return jsonify({"error": "invalid username or password"}), 401
#all see
@app.route("/notes",methods=["GET"])
@jwt_required()
def seeall():
    all_notes = Note.query.all()
    print(all_notes)
    result = []
    for x in all_notes:
        result.append({"id":x.id,"title":x.title,"done":x.done})
    return jsonify(result)
    
#add
@app.route("/notes",methods=["POST"])
@jwt_required()
def addnotes():
    data = request.get_json()
    note = Note(title=data["title"])
    db.session.add(note)
    db.session.commit()
    return jsonify({"Status":"Data added succesfully"})
with app.app_context():
    db.create_all()
if __name__=="__main__":
    app.run(debug=True)