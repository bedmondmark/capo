CREATE TABLE race (
	race_id INTEGER PRIMARY KEY AUTOINCREMENT,
	race_date TEXT,
	race_start_time TEXT
);

CREATE TABLE person (
	person_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL
);

CREATE TABLE race_time (
	race_time_id        INTEGER PRIMARY KEY AUTOINCREMENT,
	race_id             INTEGER NOT NULL    REFERENCES race( race_id ),
	person_id           INTEGER NOT NULL    REFERENCES person( person_id ),
	race_duration_secs  INTEGER NOT NULL
);