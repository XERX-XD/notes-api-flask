from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

@app.route("/")
def home():
    return "Notes api - xerx"


@app.route("/notes",methods=["POST"])
def addnotes():
    data = request.get_json()
    new_note = Note(title=data["title"])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"id": new_note.id, "title": new_note.title, "done": new_note.done}), 201
@app.route("/notes",methods=["GET"])
def getnotes():
    all_notes = Note.query.all()
    result=[]
    for x in all_notes:
        result.append({"id":x.id,"title":x.title,"done":x.done})
    print(result)
    return jsonify(result)

@app.route("/notes/<int:noteid>",methods=["DELETE"])
def delnote(noteid):
    note = Note.query.get(noteid)
    if note:
        print(note.title)
        db.session.delete(note)
        db.session.commit()
        return jsonify({"Status":f" note {note.title} deleted from database"})
    return jsonify({"Status":f"note id {noteid} not found in database"}),404
@app.route("/notes/<int:noteid>",methods=["GET"])
def singlesee(noteid):
    x = Note.query.get(noteid)
    if x:
        return jsonify({"id":x.id,"title":x.title,"done":x.done})
    return jsonify({"Status":f" note id {noteid} not found in database"}),404
@app.route("/notes/<int:noteid>",methods=["PUT"])
def updatevel(noteid):
    data = request.get_json()
    note = Note.query.get(noteid)
    if note:
        note.title=data["title"]
        note.done=data["done"]
        db.session.commit()
        return jsonify({"Status":"updated","updated_note":
                        {"id":note.id,"title":note.title,"done":note.done}})
    return jsonify({"Status":f" note id {noteid} not found in database"}),404
with app.app_context():
    db.create_all()
if __name__=="__main__":
    app.run(debug=True)