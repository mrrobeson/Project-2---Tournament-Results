#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import bleach
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament") 

def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    DB.commit()
    DB.close()
    return

def deletePlayers():
     """Remove all the player records from the database."""
     DB = connect()
     c = DB.cursor()
     c.execute("DELETE FROM players")
     DB.commit()
     DB.close()
     return

#deletePlayers()

def countPlayers():
     """Returns the number of players currently registered."""
     DB = connect()
     c = DB.cursor()
     c.execute("SELECT COUNT(*) from players")
     result = c.fetchone()
     count = result[0]
     DB.close()
     return count

#print countPlayers()
 

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (bleach.clean(name),))
    DB.commit()
    DB.close()

#registerPlayer('greg18')

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT * FROM full_standings")
    result = c.fetchall()
    #for i in range(0, len(result)-1, 2):
    print result
    #print result
    DB.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (winner,loser) VALUES (%s,%s)", (winner,    \
              loser))
    DB.commit()
    DB.close()

# reportMatch(128, 125)
# reportMatch(128, 125)
# reportMatch(127, 126)

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * from swiss_pair_view")
    pairings = c.fetchall()
    """Formats the player standings into pairs, and returns the list of tuple pairs."""
    pairs = []
    for i in range(0, len(pairings)-1, 2):
        pair = (pairings[i][0:2] + pairings[i+1][0:2])
        pairs.append(pair)
    return pairs
    DB.close()