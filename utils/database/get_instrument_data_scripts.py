import psycopg2
from datetime import date, time
from utils.constants import DbConstants


def get_data(
    instrument: str,
    startDate: date,
    startTime: time,
    endDate: date,
    endTime: time,
):
    try:
        with psycopg2.connect(
            database=DbConstants.DB_PARAMS["database"],
            user=DbConstants.DB_PARAMS["user"],
            host=DbConstants.DB_PARAMS["host"],
            password=DbConstants.DB_PARAMS["password"],
            port=DbConstants.DB_PARAMS["port"],
        ) as conn:
            sql = f"SELECT * FROM public.\"{instrument}\" WHERE date >= '{startDate}' AND time >= '{startTime}' AND date <= '{endDate}' AND time <= '{endTime}'"
            cur = conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            return data
    except Exception as e:
        print("Error: " + str(e))
