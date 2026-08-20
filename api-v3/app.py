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
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
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
    userid= int(get_jwt_identity())
    all_notes = Note.query.filter_by(user_id=userid)
    print(all_notes)
    result = []
    for x in all_notes:
        result.append({"id":x.id,"title":x.title,"done":x.done})
    return jsonify(result)
    
#add
@app.route("/notes",methods=["POST"])
@jwt_required()
def addnotes():
    userid = int(get_jwt_identity())
    data = request.get_json()
    print(userid)
    note = Note(title=data["title"],user_id=userid).all()
    db.session.add(note)
    db.session.commit()
    return jsonify({"Status":"Data added succesfully"})
#update
@app.route("/notes/<int:noteid>",methods=["PUT"])
@jwt_required()
def update(noteid):
    data=request.get_json()
    userid = int(get_jwt_identity())
    note = Note.query.get(noteid)
    if note and note.user_id == userid:
        note.title = data["title"]
        note.done=data["done"]
        db.session.commit()
        return jsonify({"status":"updated","updated_value":{"id":note.id,"title":note.title,"done":note.done}})
    return jsonify({"Status":f" note id {noteid} not found in database"}),404
#see first one
@app.route("/notes/<int:noteid>",methods=["GET"])
@jwt_required()
def getsingle(noteid):
    userid = int(get_jwt_identity())
    note = Note.query.get(noteid)
    if note and note.user_id==userid:
        return jsonify({"id":note.id,"title":note.title,"done":note.done})
    return jsonify({"Status":f" note id {noteid} not found in database"}),404

@app.route("/notes/<int:noteid>",methods=["DELETE"])
@jwt_required()
def delnote(noteid):
    userid = int(get_jwt_identity())
    note = Note.query.get(noteid)
    if note and note.user_id==userid:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"Status":f" note {note.title} deleted from database"})
    return jsonify({"Status":f"note id {noteid} not found in database"}),404
with app.app_context():
    db.create_all()
if __name__=="__main__":
    app.run(debug=True)