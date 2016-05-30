import sqlite3
import Settings


def create_table(con):
    """
    create a table in case it is not exist
    :param con
    """
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS scores(Name TEXT, score INTEGER);")


def insert_new_score(name, level, con, table_name):
    """
    by the user's score, will insert his name or his highest score
    :param name
    :param level
    :param con
    :param table_name
    """
    score = get_score(table_name, name, con)
    if score == None:
        insert_new_name(table_name, name, level, con)
    elif score[0] < level:
        update_score(table_name, name, level, con)


def get_score(table_name, name, con):
    """
    gets user's score, or None if the user does not exist
    :param table_name
    :param name
    :param con
    :return: user's score or None
    """
    with con:
        cur = con.cursor()
        cur.execute("SELECT Score FROM {table} WHERE Name = \"{value}\";".format(table=table_name, value=name))
        result = cur.fetchone()
        return result


def insert_new_name(table_name, name, level, con):
    """
    in case user does not exist, inserts his name and hist score
    :param table_name
    :param name
    :param level
    :param con
    """
    cur = con.cursor()
    cur.execute("INSERT INTO {table} (Name, score) VALUES {values};".format(table=table_name, values=(name, level)))
    con.commit()


def update_score(table_name, name, level, con):
    """
    in case user exists, updates his score if its higher than he has
    :param table_name
    :param name
    :param level
    :param con
    """
    with con:
        cur = con.cursor()
        cur.execute("UPDATE {table} SET score={level} WHERE Name = \"{name}\";".format(table=table_name, level=level,
                                                                                 name=name))
        con.commit()

