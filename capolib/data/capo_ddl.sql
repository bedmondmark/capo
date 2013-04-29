CREATE TABLE race (
	race_id INTEGER PRIMARY KEY AUTOINCREMENT,
	race_date TEXT NOT NULL,
  distance_km INTEGER NOT NULL,
	start_time TEXT
);

CREATE TABLE person (
	person_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL UNIQUE
);

CREATE TABLE race_time (
	race_time_id        INTEGER PRIMARY KEY AUTOINCREMENT,
	race_id             INTEGER NOT NULL    REFERENCES race,
	person_id           INTEGER NOT NULL    REFERENCES person,
	race_duration_secs  INTEGER NOT NULL
);