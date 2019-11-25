from server.models import *
from server import db
import json
from pprint import pprint

def allocate():
    teams = Team.query.all()
    teams_max_cgpi = dict()
    fp = open("full_year_batch17_cgpi.json", "r")
    students = json.load(fp)
    for team in teams:
        members = Member.query.filter_by(
            team_id = team.id
        ).all()
        max_cgpi = 0
        for member in members:
            st = Student.query.filter_by(
                id = member.student_id
            ).first()
            for student in students:
                if student["Rollno"] == str(st.roll_number):
                    max_cgpi = max(max_cgpi, float(student["Cgpa"]))
                    break
        teams_max_cgpi[team.id] = max_cgpi
    team_remaining = [team for team in teams if team.room_allocated == -1]
    team_remaining.sort(key = lambda team: teams_max_cgpi[team.id], reverse = True)
    ########
    for team in team_remaining:
        choices = Choice.query.filter_by(
            team_id = team.id
        ).all()
        pref = 0
        allocated = False
        
        while not allocated:
            if pref >= len(choices):
                break
            
            preferred_room = choices[pref].room_no
            preferred_room = Room.query.filter_by(
                room_no = preferred_room
            ).first()
            if not preferred_room.is_allocated:
                print(f"Allocating room {preferred_room} to {team.id}")
                preferred_room.is_allocated = True
                team.room_allocated = preferred_room.room_no
                db.session.commit()
                allocated = True
            else:
                pref += 1
allocate()