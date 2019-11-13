from flask import session, jsonify
from server import app, db
from server.models import *
import json

from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


# todo: return room_status of current team
@app.route("/api/get_rooms/")
def get_rooms():
    rooms = Room.query.all()
    return json.dumps(rooms, cls = AlchemyEncoder)


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


@app.route("/api/remove_preference/<int:room_no>/", methods = ["POST"])
def remove_preference(room_no):
    choice = Choice.query.filter_by(
        team_id = session["team_id"],
        room_no = room_no
    ).first()
    db.session.delete(choice)
    db.session.commit()
    return "OK deleted"


# todo: add preferences to user info
# 
@app.route("/api/get_user_info/")
def get_user_info():
    user_info = dict(session)
    user_info['preferences'] = Choice.query.filter_by(
        team_id = session["team_id"],
    ).all()
    j = json.dumps(user_info, cls = AlchemyEncoder)
    j = json.loads(j)
    return jsonify(j)