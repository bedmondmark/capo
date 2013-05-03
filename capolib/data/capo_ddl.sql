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

CREATE VIEW results AS
  SELECT race.race_id, race.race_date, person.person_id AS runner_id,
    person.name AS runner_name, race_time.race_duration_secs
  FROM race_time
    NATURAL JOIN person
    NATURAL JOIN race;
