from Cloud.packages.security import secrets_manager
from Cloud.packages.constants import constants
import psycopg2
import json


##############################################################################################

def connection_handler():
    secret = json.loads(secrets_manager.get_secret(constants.AURORA_SECRET_NAME))

    # connect to the db client
    try:
        conn = psycopg2.connect(dbname=secret["dbname"],
                                user=secret["username"],
                                password=secret["password"],
                                host=secret["host"],
                                port="5432")

        return conn

    except Exception as e:
        print(e)

    return


def get_bis_users(conn=None):
    cur = conn.cursor()
    cur.execute('SELECT * FROM public."Users"')
    result = cur.fetchall()
    conn.commit()

    # a tuple is returned, this will get the item in index 1 which is the user email
    user_list = [itm[1] for itm in result]
    return user_list

##############################################################################################
