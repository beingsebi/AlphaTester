"""
Module for connecting to PostgreSQL server and manipulating the database.
"""

import os
import sys
from typing import List

import pandas as pd
import psycopg2
import sqlalchemy

from utils.constants import DbConstants


def get_csv_files_from_directory(directory_path: str) -> List[str]:
    """
    Function to get paths to all CSV files in a given directory.
    :param directory_path: The directory to search for CSV files.
    :return: A list of all CSV files in the directory.
    """
    csv_files = []
    for file in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path,
                                       file)) and file.endswith(".csv"):
            csv_files.append(directory_path + file)
    return csv_files


# works with both absolute and relative paths
def insert_data_into_table(path_to_csv: str, table_name: str | None = None):
    """
    Gets db data from constants.py -> DbConstants -> DB_PARAMS
    Function to insert data into the PostgreSQL table from a CSV file.
    If table name is not provided, the name of the CSV file is used.
    If the table does not exist, it is created.
    """
    # Read the CSV file into a pandas DataFrame
    try:
        data = pd.read_csv(
            path_to_csv,
            # IMPORTANT: This is set to None because the CSV file does not have a header row
            header=None,
            # IMPORTANT: These are the column names
            names=["date", "time", "open", "high", "low", "close", "spread"],
        )
    except FileNotFoundError as e:
        print(f"Error reading CSV file: {e}")
        return
    except pd.errors.EmptyDataError as e:
        print(f"Error reading CSV file: {e}")
        return

    # if table name is not provided, use the name of the CSV file
    if table_name is None:
        # IMPORTANT: This is the expected format: NAME[_blabla].csv
        table_name = os.path.basename(path_to_csv)  # XAUUSD_2024_02.csv
        table_name = table_name.split(".")[0]  # XAUUSD_2024_02
        table_name = table_name.split("_")[0]  # XAUUSD

    try:
        with psycopg2.connect(
                database=DbConstants.DB_PARAMS["database"],
                user=DbConstants.DB_PARAMS["user"],
                host=DbConstants.DB_PARAMS["host"],
                password=DbConstants.DB_PARAMS["password"],
                port=DbConstants.DB_PARAMS["port"],
        ) as conn:
            print("Connected to the PostgreSQL server.", table_name, sep="\n")

            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS "{table_name.upper()}" (
                "date" DATE NOT NULL,
                "time" TIME WITHOUT TIME ZONE NOT NULL,
                "open" DOUBLE PRECISION NOT NULL,
                "high" DOUBLE PRECISION NOT NULL,
                "low" DOUBLE PRECISION NOT NULL,
                "close" DOUBLE PRECISION NOT NULL,
                "spread" INTEGER,
                PRIMARY KEY ("date", "time")
            );
            """

            cur = conn.cursor()
            conn.set_session(autocommit=True)
            cur.execute(create_table_query)
            conn.commit()

            engine = sqlalchemy.create_engine(
                f'postgresql://{DbConstants.DB_PARAMS["user"]}:{DbConstants.DB_PARAMS["password"]}'
                +
                f'@{DbConstants.DB_PARAMS["host"]}/{DbConstants.DB_PARAMS["database"]}'
            )

            data.to_sql(
                "insert_temp_table",
                engine,
                if_exists="replace",
                index=False,
                dtype={
                    "date": sqlalchemy.types.Date,
                    "time": sqlalchemy.types.Time,
                    "open": sqlalchemy.types.Float,
                    "high": sqlalchemy.types.Float,
                    "low": sqlalchemy.types.Float,
                    "close": sqlalchemy.types.Float,
                    "spread": sqlalchemy.types.BigInteger,
                },
            )

            query = f"""
            INSERT INTO "{table_name}" ("date", "time", "open", "high", "low", "close", "spread")
            SELECT "date", "time", "open", "high", "low", "close", "spread"
            FROM insert_temp_table
            ON CONFLICT ("date", "time") DO NOTHING;
            """
            cur.execute(query)
            print("done")

    except psycopg2.DatabaseError as error:
        print(error)


# insert_data_into_table("/home/sebi/Desktop/test_csvs/XAUUSD_2024_02.csv")
# insert_data_into_table("ZXAUUSD_2024_01.csv")

# path = sys.argv[1]
# insert_data_into_table(path)
