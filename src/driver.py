import psycopg2, os, sys
from ftfutils import *

DEBUG = False

def main():
    # Get login info from environment variables
    db_user = os.getenv('PYDB_USER')
    db_password = os.getenv('PYDB_PASSWORD')

    # Get host info from user
    uarg = sys.argv[1].split(':')
    db_host = uarg[0]
    db_port = uarg[1]

    log(Mode.INFO, "Connecting to database: " + db_user + "@" + db_host + ":" + db_port)
    if(DEBUG): log(Mode.DEBUG, "Hash: " + db_password)

    psycopg2.connect(database="spy", user=db_user, password=db_password, host=db_host, port=db_port)

if __name__ == '__main__': main()
