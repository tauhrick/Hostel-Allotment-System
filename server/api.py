from flask import session, jsonify
from server import app, db
from server.models import *


# todo: return room_status of current team
@app.route("/api/get_rooms/")
def get_rooms():
    rooms = Room.query.all()
    return jsonify(rooms)


@app.route("/api/add_preference/<int:room_no>/", methods = ["POST"])
def add_preference(room_no):
    choice = Choice(
        team_id = session["team_id"],
        choice_no = 1,
        room_no = room_no
    )
    db.session.add(choice)
    db.session.commit()
    return "OK added"


@app.route("/api/remove_preference/<int:room_no>/")
def remove_preference(room_no):
    choice = Choice.query.filter_by(
        team_id = session["team_id"],
        room_no = room_no
    ).first()
    db.session.delete(choice)
    db.session.commit()
    return "OK deleted"


# todo: add preferences to user info
@app.route("/api/get_user_info/")
def get_user_info():
    return jsonify(dict(session))
