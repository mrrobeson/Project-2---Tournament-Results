-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
create database "tournament";

create table players(
	player_id	SERIAL,
	name		varchar(40)
);

create table matches(
	match_id		SERIAL,	
	winner			integer,
	loser			integer
);

-- Thought initially I would need a "record" table but I didn't 
-- create table record(
-- 	player_id		integer,
-- 	wins			integer,
-- 	losses			integer
-- );

--These are just some queries I used to test and build
-- SELECT a.player_id AS id, a.name, count(b.winner) AS wins, matches FROM count_matches
-- FROM players AS a
-- LEFT JOIN matches AS b
-- ON (a.player_id = b.winner)
-- GROUP BY a.name, id ORDER BY wins DESC

-- SELECT weather.city, weather.temp_lo, weather.temp_hi,
--        weather.prcp, weather.date, cities.location
--     FROM weather, cities
--     WHERE cities.name = weather.city

--Gets the num of matches for use in the full_standings VIEW
CREATE VIEW count_matches AS SELECT a.player_id, count(b.match_id) AS matches
FROM players AS a
LEFT JOIN matches AS b
ON (a.player_id = b.winner or a.player_id = b.loser)
GROUP BY a.player_id


--Used in the full_standings VIEW
CREATE VIEW players_name_wins AS SELECT a.player_id AS id, a.name, count(b.winner) AS wins
FROM players AS a
LEFT JOIN matches AS b
ON (a.player_id = b.winner)
GROUP BY a.name, id ORDER BY wins DESC

#View that contains the full standings
CREATE VIEW full_standings AS SELECT id, name, wins, matches
FROM players_name_wins AS a
LEFT JOIN count_matches AS b
ON id = player_id
ORDER BY wins DESC;

#View used to get the new matches based on number of wins
CREATE VIEW swiss_pair_view 
AS SELECT a.player_id, a.name, count(b.winner) as record  
FROM players AS a 
LEFT JOIN matches AS b ON a.player_id = b.winner
GROUP BY a.name, a.player_id ORDER BY record DESC