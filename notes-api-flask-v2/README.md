# Notes API (Flask)

A REST API for managing notes, built while learning backend fundamentals — starting with raw Flask + an in-memory store, then a real database, then authentication.

## Stack
- Flask
- Flask-SQLAlchemy (SQLite)
- Flask-JWT-Extended (authentication)
- Werkzeug security (password hashing)

## Features
- User signup and login with hashed passwords (never stored in plain text)
- JWT-based authentication — issued on login, required on all note routes
- Full CRUD for notes:
  - `POST /notes` — create a note
  - `GET /notes` — list all notes
  - `GET /notes/<id>` — get a single note
  - `PUT /notes/<id>` — update a note
  - `DELETE /notes/<id>` — delete a note

## Auth

All `/notes` routes require a valid JWT.

1. `POST /signup` — `{ "username": "...", "password": "..." }`
2. `POST /login` — same body, returns `{ "access_token": "..." }`
3. Send the token on every `/notes` request:
   `Authorization: Bearer <access_token>`

## Setup

```bash
pip install flask flask_sqlalchemy flask_jwt_extended
python app.py
```

The database (`notes.db`) and its tables are created automatically on first run via `db.create_all()` — no manual setup step needed.

## Status
🚧 In progress — next up: linking notes to the specific user who created them, so each user only sees their own notes.