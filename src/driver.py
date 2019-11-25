import psycopg2, os, sys
from ftfutils import *

DEBUG = False
COL_WIDTH=20
FORMAT_STRING='{0: <' + str(COL_WIDTH) + '}'

# dbclass.cs.pdx.edu

def main():
    # Check for cli arguments
    if(len(sys.argv) !=3):
        log(Mode.ERROR, "Usage: python3 driver.py [host] \"<host>\"")
        exit(-1)

    # Get login info from environment variables
    db_user = os.getenv('PYDB_USER')
    db_password = os.getenv('PYDB_PASSWORD')

    # Get host info from user
    db_host = sys.argv[1]

    # Open the session
    session = psycopg2.connect(database=db_user, user=db_user, password=db_password, host=db_host)
    db = session.cursor()
    if(DEBUG): log(Mode.DEBUG, "Opened session to database: " + str(session))

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

    for col in cols:
        print(FORMAT_STRING.format(col), end="")
    print("\n", end="")

    for col in cols:
        for i in range(0, COL_WIDTH): print("-", end="")
    print("\n", end="")

    for row in rows:
        for i in row:
            print(FORMAT_STRING.format(i), end="")
        print("\n", end="")

    log(Mode.INFO, str(len(rows)) + " Results.")

if __name__ == '__main__': main()
