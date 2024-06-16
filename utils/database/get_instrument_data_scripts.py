import logging
from datetime import datetime

import psycopg2

from utils.constants import DbConstants

logger = logging.getLogger(__name__)


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
            sql = f'SELECT date, time, open, high, low, close, spread FROM public."{instrument}" WHERE 0 = 0 '
            if startDatetime is not None:
                sql += f"AND (date > '{startDatetime.date()}' OR (date = '{startDatetime.date()}' AND time >= '{startDatetime.time()}')) "
            if endDatetime is not None:
                sql += f"AND (date < '{endDatetime.date()}' OR (date = '{endDatetime.date()}' AND time <= '{endDatetime.time()}'))"

            cur = conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            return data
    except Exception as e:
        logger.debug("Error: " + str(e))


def get_last_available_date(instrument: str):
    try:
        with psycopg2.connect(
                database=DbConstants.DB_PARAMS["database"],
                user=DbConstants.DB_PARAMS["user"],
                host=DbConstants.DB_PARAMS["host"],
                password=DbConstants.DB_PARAMS["password"],
                port=DbConstants.DB_PARAMS["port"],
        ) as conn:
            sql = f'SELECT date, time FROM public."{instrument}" ORDER BY date DESC, time DESC LIMIT 1'
            cur = conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            if len(data) == 0:
                return None
            return datetime.combine(data[0][0], data[0][1])
    except Exception as e:
        logger.debug("Error: " + str(e))


def get_first_available_date(instrument: str):
    try:
        with psycopg2.connect(
                database=DbConstants.DB_PARAMS["database"],
                user=DbConstants.DB_PARAMS["user"],
                host=DbConstants.DB_PARAMS["host"],
                password=DbConstants.DB_PARAMS["password"],
                port=DbConstants.DB_PARAMS["port"],
        ) as conn:
            sql = f'SELECT date, time FROM public."{instrument}" ORDER BY date ASC, time ASC LIMIT 1'
            cur = conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            if len(data) == 0:
                return None
            return datetime.combine(data[0][0], data[0][1])
    except Exception as e:
        logger.debug("Error: " + str(e))
