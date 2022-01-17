from unittest import TestCase
from DbManager import DbManager
import json
import os
import os.path


class DbManagerTest(TestCase):
    manager: DbManager = None
    data: dict

    @classmethod
    def setUpClass(cls) -> None:
        with open('data.json', 'r') as file:
            data = json.load(file)
            cls.manager = DbManager(**data['psql_server'])
            cls.manager.cursor.execute('DROP TABLE test_table; COMMIT;')
            cls.manager.cursor.execute("""
    CREATE TABLE test_table(
    ID              SERIAL PRIMARY KEY  NOT NULL,
    NAME            TEXT                NOT NULL,
    INT_NUMBER      INT                 NOT NULL,
    REAL_NUMBER     REAL
);
            """)
            cls.data = data['db_manager_test']
            for rec in cls.data['db']:
                cls.manager.cursor.execute(
                    'INSERT INTO test_table (NAME, INT_NUMBER, REAL_NUMBER) VALUES (%s, %s, %s)',
                    (rec['name'], rec['int_number'], rec['real_number'])
                    # Is it real to use something like **rec here?
                )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.manager.__exit__(None, None, None)
        if os.path.isfile('result.json'):
            os.remove('result.json')

    def testCollectIntRequired(self):
        """test_collect_method_int_required"""
        self.manager.collect('test_table', 'int_number', 900000)
        with open('result.json', 'r') as answer:
            self.assertEqual(self.data['test_collect_method_int_required'], answer.read())

    def testCollectRealOptional(self):
        """test_collect_method_real_optional"""
        self.manager.collect('test_table', 'real_number', 900)
        with open('result.json', 'r') as answer:
            self.assertEqual(self.data['test_collect_method_real_optional'], answer.read())
