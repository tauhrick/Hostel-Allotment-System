from server import db
from server.models import *
import requests

ss = db.session

def add_rooms():
	rooms = [
	    [4, 1, 0],
	    [5, 1, 0],
	    [6, 1, 0],
	    [7, 1, 0],
	    [8, 1, 0],
	    [1, 4, 0],
	    [1, 5, 0],
	    [1, 6, 0],
	    [1, 7, 0],
	    [1, 8, 0],
	    [4, 3, 0],
	    [5, 3, 0],
	    [6, 3, 0],
	    [7, 3, 0],
	    [8, 3, 0],
	    [3, 4, 0],
	    [3, 5, 0],
	    [3, 6, 0],
	    [3, 7, 0],
	    [3, 8, 0],  

	    [4, 1, 1],
	    [5, 1, 1],
	    [6, 1, 1],
	    [7, 1, 1],
	    [8, 1, 1],
	    [1, 4, 1],
	    [1, 5, 1],
	    [1, 6, 1],
	    [1, 7, 1],
	    [1, 8, 1],
	    [4, 3, 1],
	    [5, 3, 1],
	    [6, 3, 1],
	    [7, 3, 1],
	    [8, 3, 1],
	    [3, 4, 1],
	    [3, 5, 1],
	    [3, 6, 1],
	    [3, 7, 1],
	    [3, 8, 1],
	    
	    [4, 1, 2],
	    [5, 1, 2],
	    [6, 1, 2],
	    [7, 1, 2],
	    [8, 1, 2],
	    [1, 4, 2],
	    [1, 5, 2],
	    [1, 6, 2],
	    [1, 7, 2],
	    [1, 8, 2],
	    [4, 3, 2],
	    [5, 3, 2],
	    [6, 3, 2],
	    [7, 3, 2],
	    [8, 3, 2],
	    [3, 4, 2],
	    [3, 5, 2],
	    [3, 6, 2],
	    [3, 7, 2],
	    [3, 8, 2],
	    [4, 1, 3],
	    [5, 1, 3],
	    [6, 1, 3],
	    [7, 1, 3],
	    [8, 1, 3],
	    [1, 4, 3],
	    [1, 5, 3],
	    [1, 6, 3],
	    [1, 7, 3],
	    [1, 8, 3],
	    [4, 3, 3],
	    [5, 3, 3],
	    [6, 3, 3],
	    [7, 3, 3],
	    [8, 3, 3],
	    [3, 4, 3],
	    [3, 5, 3],
	    [3, 6, 3],
	    [3, 7, 3],
	    [3, 8, 3],
	];
	for room_no in range(len(rooms)):
		room = Room(
			room_no = room_no,
			location_x = rooms[room_no][0],
			location_y = rooms[room_no][1],
			location_z = rooms[room_no][2],
			is_allocated = False,
			room_capacity = 3
		)
		ss.add(room)
		ss.commit()


def add_students():
	URL = 'http://localhost:8000/register_student/'
	students = [
		('17501', '17548', '17534', '123'),
		('17542', '17514', '17524', '123'),
		('17531', '17505', '17540', '123'),
	]
	for s in students:
		payload = {
			'roll_number_1': s[0],
			'roll_number_2': s[1],
			'roll_number_3': s[2],
			'phone_number_1': s[0],
			'phone_number_2': s[1],
			'phone_number_3': s[2],
			'password': s[3]
		}
		r = requests.post(URL, data=payload)
		print(f"Students ({s})  added")


def main():
	try:
		add_rooms()
	except ConnectionRefusedError:
		print("Server not running")
		pass
	except:
		pass
	add_students()


if __name__ == "__main__":
	main()