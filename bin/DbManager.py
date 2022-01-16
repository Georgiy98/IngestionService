import psycopg2.extensions
import typing
from utils.retry import retry


class DbManager:
    """Context manager for connection with Postgres Server and acting with it"""
    connection: psycopg2.extensions.connection = None

    def __init__(self, host, port, db_name, username, pwd):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.pwd = pwd

    def _get_all_tables(self) -> typing.List[str]:
        """It gets all table names from db it's connected to"""

    def _get_all_columns(self, table_name: str) -> typing.List[str]:
        """It gets all column names from table"""

    @retry(5)
    def __enter__(self):
        # TODO: establish connection
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)
        # TODO: close connection
        pass

    @retry(5)
    def collect(self, table_name: str,
                incremental_key: str,
                incremental_value: typing.Union[int, float]
                ) -> dict:
        """It collects all records from table in database, where incremental value more than incremental key
        :returns dict
        """
