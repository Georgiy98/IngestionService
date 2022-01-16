class RetryException(Exception):
    """Class for gathering all exceptions were happened in case of total fail"""


class FatalDatabaseException(Exception):
    """Class of exceptions for operations that have no chance to be successful"""
