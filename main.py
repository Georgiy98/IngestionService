from DbManager import DbManager
import sys


def show_help_info():
    print(
        '''Program takes next arguments:
host, port, name of database, username, password, name of table, name of incremental column, minimum value
As an example:
127.0.0.1 5433 test_db postgres 1 test_table INT_NUMBER 900
''')


def show_help_command():
    print('Use command python3 main.py --help to get more info')


if __name__ == '__main__':
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
        print('Port must be an integer and minimum value must be float!')
        show_help_command()
    print('Connecting to db..')
    manager = DbManager(host, port, db, user, pwd)
    print('Connection established. Gathering data..')
    manager.collect(table, inc_key, inc_value)
    print('Operation has finished successful! You can see result in "result.json" file')
