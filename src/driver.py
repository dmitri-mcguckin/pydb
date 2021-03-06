#!/usr/bin/env python3

import psycopg2, os, sys
from ftfutils import *

DEBUG = False
LENGTHS = []

# dbclass.cs.pdx.edu

def check_env(env_var, var):
    if(var == None):
        log(Mode.ERROR, "The environment variable: " + env_var + " must be set in order to log in.")
        sys.exit(-1)
    else: log(Mode.INFO, "Recognized environment variable: " + env_var)


def main():
    # Check for cli arguments
    if(len(sys.argv) !=3):
        log(Mode.ERROR, "Usage: python3 driver.py [host] \"<query>\"")
        exit(-1)

    # Get login info from environment variables
    db_user = os.getenv('PYDB_USER')
    db_password = os.getenv('PYDB_PASSWORD')

    check_env('PYDB_USER', db_user)
    check_env('PYDB_PASSWORD', db_password)

    # Get host info from user
    db_host = sys.argv[1]

    # Open the session
    try:
        session = psycopg2.connect(database=db_user, user=db_user, password=db_password, host=db_host)
        db = session.cursor()
        if(DEBUG): log(Mode.DEBUG, "Opened session to database: " + str(session))
    except psycopg2.OperationalError as e:
        log(Mode.ERROR, "There was a fatal error trying to log in to the database:\n\t" + str(e))
        sys.exit(-1)

    # Make the query
    query = sys.argv[2]
    try:
        db.execute(query)
    except Exception as e:
        log(Mode.ERROR, str(e))
        session.close()
        if(DEBUG): log(Mode.DEBUG, "Closed session to database: " + str(session))
        exit(-1)

    cols = [desc[0] for desc in db.description]
    rows = db.fetchall()

    # Close the session
    session.close()
    if(DEBUG): log(Mode.DEBUG, "Closed session to database: " + str(session))

    for i, col in enumerate(cols):
        longest = len(col)

        for row in rows:
            if(len(str(row[i])) > longest): longest = len(str(row[i]))
        LENGTHS.append(longest + 1)

    print("| ", end="")
    for i, col in enumerate(cols):
        print(str('{0: <' + str(LENGTHS[i]) + '}| ').format(col), end="")
    print("\n", end="")

    for i, col in enumerate(cols):
        print("+", end="")
        for i in range(0, LENGTHS[i] + 1): print("-", end="")
    print("+\n", end="")

    for row in rows:
        print("| ", end="")
        for i, element in enumerate(row):
            print(str('{0: <' + str(LENGTHS[i]) + '}| ').format(str(element)), end="")
        print("\n", end="")
    print("\n", end="")

    log(Mode.INFO, str(len(rows)) + " Results.")

if __name__ == '__main__': main()
