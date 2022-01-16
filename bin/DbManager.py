import typing
from utils.retry import retry
import psycopg2
import psycopg2.extensions
from exceptions import FatalDatabaseException
from pprint import pformat


class DbManager:
    """Context manager for connection with Postgres Server and acting with it"""

    NUMERIC_TYPES = (
        'real', 'integer', 'numeric', 'oid', 'bigint', 'smallint', 'double precision'
    )
    connection: psycopg2.extensions.connection = None
    cursor: psycopg2.extensions.cursor = None

    def __init__(self, host: str, port: int, db_name: str, username: str, pwd: str):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.pwd = pwd
        self.establish_connection()

    @retry(5, exclude=ValueError)
    def establish_connection(self):
        self.connection = psycopg2.connect(
            host=self.host,
            port=int(self.port),
            database=self.db_name,
            user=self.username,
            password=self.pwd
        )
        self.cursor = self.connection.cursor()

    def _get_all_tables_names(self) -> typing.Tuple[str]:
        """It gets all table names from db it's connected to"""
        self.cursor.execute('''
            SELECT table_name FROM information_schema.tables;
        ''')
        return tuple(item[0] for item in self.cursor.fetchall())

    def _get_all_columns(self, table_name: str) -> typing.Tuple[str]:
        """It gets all column names from table"""
        self.cursor.execute(f'''
        SELECT column_name 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE table_name = '{table_name}';
        ''')
        res = self.cursor.fetchall()
        return tuple(item[0] for item in res)

    def _get_column_type(self, table_name: str, column_name: str) -> str:
        self.cursor.execute(f'''
                SELECT data_type
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE table_name = '{table_name}' AND column_name = '{column_name}';
                ''')
        return self.cursor.fetchone()[0]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    @retry(5, exclude=(ValueError, FatalDatabaseException))
    def collect(self, table_name: str,
                incremental_key: str,
                incremental_value: typing.Union[int, float]
                ) -> dict:
        """It collects all records from table in database, where incremental value more than incremental key
        :returns dict
        """

        def check():
            if type(incremental_value) not in (int, float):
                raise ValueError(f'incremental_value must be instance of int/float')
            if table_name not in self._get_all_tables_names():
                raise FatalDatabaseException(f'No table named "{table_name}" in database')
            if incremental_key not in self._get_all_columns(table_name):
                raise FatalDatabaseException(f'No column named "{incremental_key}" in {table_name}')
            if self._get_column_type(table_name, incremental_key) not in self.NUMERIC_TYPES:
                raise FatalDatabaseException(f'Column "{incremental_key}" is not a number')

        def gather_and_save_data():
            columns = self._get_all_columns(table_name)
            self.cursor.execute(f'''
            SELECT {', '.join(columns)} FROM {table_name} WHERE {incremental_key} > {incremental_value};
            ''')
            with open('result.json', 'w') as file:
                file.write('[')
                while records := self.cursor.fetchmany(10000):
                    file.write(pformat(
                        [{key: value for key, value in zip(columns, record)} for record in records]
                    ).replace('None', 'null').replace('False', 'false').replace('True', 'true')[1: -1])
                file.write(']')

        check()
        gather_and_save_data()
