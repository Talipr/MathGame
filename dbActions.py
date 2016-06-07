import sqlite3
import settings


def create_table(db_connection):
    """
    create a table in case it is not exist
    :param db_connection : connection to db object
    """
    with db_connection:
        cur = db_connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS scores(Name TEXT, score INTEGER);")


def insert_new_score(name, level, db_connection):
    """
    by the user's score, will insert his name or his highest score
    :param name : the name of the player
    :param level : player's level
    :param db_connection : connection to db object
    """
    score = get_score(name, db_connection)
    if score is None:
        insert_new_name(name, level, db_connection)
    elif score[0] < level:
        update_score(name, level, db_connection)


def get_score(name, db_connection):
    """
    gets user's score, or None if the user does not exist
    :param name : the name of the player
    :param db_connection : connection to db object
    :return: user's score or None
    """
    with db_connection:
        cur = db_connection.cursor()
        cur.execute("SELECT Score FROM scores WHERE Name = '%s';" % name)
        result = cur.fetchone()
        return result


def insert_new_name(name, level, db_connection):
    """
    in case user does not exist, inserts his name and hist score
    :param name : the name of the player
    :param level : player's level
    :param db_connection : connection to db object
    """
    cur = db_connection.cursor()
    cur.execute("INSERT INTO scores (Name, score) VALUES (?, ?);", (name, level))
    db_connection.commit()


def update_score(name, level, db_connection):
    """
    in case user exists, updates his score if its higher than he has
    :param name : the name of the player
    :param level : player's level
    :param db_connection : connection to db object
    """
    with db_connection:
        cur = db_connection.cursor()
        cur.execute("UPDATE scores SET score= ? WHERE Name = ?;", (level, name))
        db_connection.commit()


def show_high_scores(db_connection):
    """
    shows top 10 player's scores
    :param db_connection:  connection to the db
    """
    with db_connection:
        cur = db_connection.cursor()
        cur.execute("select * from scores order by score DESC limit 10;")
        result = cur.fetchall()
        print "here top 10 scores:"
        for score in result:
            print score
