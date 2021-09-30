from Cloud.packages.security import secrets_manager
from Cloud.packages.constants import constants
import psycopg2
import datetime
import dateutil
import calendar
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


def get_date_values(get_current=False):
    now = datetime.datetime.now()
    month = now + dateutil.relativedelta.relativedelta(months=0 if get_current else -1)
    num_days = calendar.monthrange(month.year, month.month)[1]  # num_days = 28
    month_format = str(month.month).zfill(2)

    # query parameters
    start_date = f"{month.year}{month_format}01"
    end_date = f"{month.year}{month_format}{num_days}"
    return start_date, end_date


def get_all_payments(conn=None, get_current=False):
    # query parameters
    start_date, end_date = get_date_values(get_current)
    min_price = 10  # dollars

    command = \
        """
        
            SELECT * FROM public."Subscriptions"
            WHERE CAST("Created" as date) BETWEEN '{}' and '{}'
            AND "Amount" > {} AND "Reference" IS NOT NULL AND TRIM("Reference") <> ''
            ORDER by "Id"
    
        """.format(start_date, end_date, min_price)

    # query table
    cur = conn.cursor()
    cur.execute(command)
    result = cur.fetchall()
    conn.commit()

    total_entries = len(result)
    commission = total_entries * 5  # 5 dollars per user
    total_income = sum([itm[5] for itm in result])
    output = {"total_payments": total_entries, "total_income": total_income, "commission": commission}
    return output


##############################################################################################

if __name__ == '__main__':
    conn = connection_handler()
    data = get_all_payments(conn, get_current=True)
    print(data)
