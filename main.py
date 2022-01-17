from DbManager import DbManager
import sys
import logging


def show_help_info():
    logging.info(
        '''Program takes next arguments:
host, port, name of database, username, password, name of table, name of incremental column, minimum value
As an example:
127.0.0.1 5433 test_db postgres 1 test_table INT_NUMBER 900
''')


def show_help_command():
    logging.info('Use command python3 main.py --help to get more info')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    if len(sys.argv) != 9:
        if len(sys.argv) == 2 and sys.argv[1] == '--help':
            show_help_info()
            exit(2)
        else:
            show_help_command()
            exit(2)
    host, port, db, user, pwd, table, inc_key, inc_value = sys.argv[1:]
    try:
        port = int(port)
        inc_value = float(inc_value)
    except ValueError:
        logging.error('Port must be an integer and minimum value must be float!')
        show_help_command()
        exit(2)
    logging.info('Connecting to db..')
    manager = DbManager(host, port, db, user, pwd)
    logging.info('Connection established. Gathering data..')
    manager.collect(table, inc_key, inc_value)
    logging.info('Operation has finished successful! You can see result in "result.json" file')
