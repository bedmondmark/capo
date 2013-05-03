INSERT OR IGNORE INTO person (person_id, name) VALUES (1, 'Mark');
INSERT OR IGNORE INTO person (person_id, name) VALUES (2, 'James');
INSERT OR IGNORE INTO person (person_id, name) VALUES (3, 'Chris');
INSERT OR IGNORE INTO person (person_id, name) VALUES (4, 'Martin');

INSERT OR IGNORE INTO race (race_id, distance_km, race_date)
  VALUES (1, 5, '2013-01-05');
INSERT OR IGNORE INTO race (race_id, distance_km, race_date)
  VALUES (2, 5, '2013-02-06');

-- Race 1 *********************************************
-- Mark, 22 mins
INSERT OR IGNORE INTO race_time
(race_time_id, race_id, person_id, race_duration_secs)
  VALUES (1, 1, 1, 1320);
-- James, 23:15
INSERT OR IGNORE INTO race_time
(race_time_id, race_id, person_id, race_duration_secs)
  VALUES (2, 1, 2, 1395);

-- Race 2 *********************************************
-- Mark, 21:35 mins
INSERT OR IGNORE INTO race_time
(race_time_id, race_id, person_id, race_duration_secs)
  VALUES (3, 2, 1, 1295);
-- James, 22:15
INSERT OR IGNORE INTO race_time
(race_time_id, race_id, person_id, race_duration_secs)
  VALUES (4, 2, 2, 1335);