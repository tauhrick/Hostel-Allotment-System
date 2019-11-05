DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS rounds;
DROP TABLE IF EXISTS choices;


CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    roll_number INTEGER UNIQUE,
    name TEXT,
    email_id TEXT UNIQUE,
    phone_number TEXT,
    cgpi FLOAT,
    year INTEGER
    password TEXT,
);

CREATE TABLE IF NOT EXISTS admins (
    user_name TEXT PRIMARY KEY,
    password TEXT
);

CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    size INTEGER,
    is_lock BOOLEAN,
    room_no INTEGER
);

CREATE TABLE IF NOT EXISTS member (
    student_id INTEGER,
    team_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES "students"(id),
    FOREIGN KEY (team_id) REFERENCES "teams"(id)
);

CREATE TABLE IF NOT EXISTS rooms (
    room_no INTEGER,
    location_x INTEGER,
    location_y INTEGER,
    location_z INTEGER,
    is_allocated BOOLEAN,
    room_capacity INTEGER
);

CREATE TABLE IF NOT EXISTS rounds (
    round_no INTEGER,
    start_time TIMESTAMP,
    duration INTEGER
);

CREATE TABLE IF NOT EXISTS choices (
    team_id INTEGER,
    choice_no INTEGER,
    room_no INTEGER,
    FOREIGN KEY (team_id) REFERENCES "teams"(id),
    FOREIGN KEY (room_no) REFERENCES "rooms"(room_no)
);
