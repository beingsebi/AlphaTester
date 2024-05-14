import psycopg2
from datetime import datetime
from utils.constants import DbConstants


def get_data(
    instrument: str,
    startDatetime: datetime,
    endDatetime: datetime,
):
    try:
        with psycopg2.connect(
            database=DbConstants.DB_PARAMS["database"],
            user=DbConstants.DB_PARAMS["user"],
            host=DbConstants.DB_PARAMS["host"],
            password=DbConstants.DB_PARAMS["password"],
            port=DbConstants.DB_PARAMS["port"],
        ) as conn:

            sql = f"SELECT date, time, open, high, low, close, spread FROM public.\"{instrument}\" WHERE date >= '{startDatetime.date()}' AND time >= '{startDatetime.time()}' AND date <= '{endDatetime.date()}' AND time <= '{endDatetime.time()}'"
            cur = conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            return data
    except Exception as e:
        print("Error: " + str(e))
