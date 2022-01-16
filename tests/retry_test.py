import unittest
import logging
import os
import functools
import json
from utils.retry import retry
from exceptions import RetryException


def raise_error_all_time():
    raise ZeroDivisionError


def raise_error_one_time():
    if raise_error_one_time.raised:
        return 200
    else:
        raise_error_one_time.raised = True
        raise ZeroDivisionError


def raise_two_different_errors():
    if raise_two_different_errors.counter == 0:
        raise_two_different_errors.counter += 1
        raise ZeroDivisionError
    elif raise_two_different_errors.counter == 1:
        raise_two_different_errors.counter += 1
        raise ValueError
    else:
        return 200


class RetryTest(unittest.TestCase):

    def check_expectations(func):
        """decorator for comparing expected data and result"""

        @functools.wraps(func)
        def wrapper(self):
            func(self)
            with open('logs.txt', 'r') as file:
                self.assertEqual(self.data[self.cur_test], file.read()[self.cur_text_position:])

        return wrapper

    @classmethod
    def setUpClass(cls) -> None:
        logging.basicConfig(filename='logs.txt')
        with open('data.json', 'r') as file:
            cls.data = json.load(file)['retry_test']

        cls.cur_text_position = 0

    def setUp(self) -> None:
        self.cur_test = self.shortDescription()
        with open('logs.txt', 'r') as file:
            self.cur_text_position = len(file.read())

    @classmethod
    def tearDownClass(cls) -> None:
        logging.shutdown()
        if os.path.isfile('logs.txt'):
            os.remove('logs.txt')

    @check_expectations
    def testOnePermanentError(self):
        """the_same_error_all_time"""
        self.assertRaises(RetryException, retry(3)(raise_error_all_time))

    @check_expectations
    def testOneTemporaryError(self):
        """one_time_failed_then_success"""
        raise_error_one_time.raised = False
        self.assertEqual(200, retry(3)(raise_error_one_time)())

    @check_expectations
    def testTwoErrors(self):
        """two_different_fails_then_success"""
        raise_two_different_errors.counter = 0
        self.assertEqual(200, retry(3)(raise_two_different_errors)())

    @check_expectations
    def testSuccess(self):
        """without_errors"""
        self.assertEqual(200, retry(3)(lambda: 200)())

    @check_expectations
    def testFuncWithArgs(self):
        """without_errors"""
        self.assertEqual(200, retry(3)(lambda a, b: 200)(1, 2))

    @check_expectations
    def testWithExclude(self):
        """do_not_retry_if_division_by_zero_error"""
        self.assertRaises(RetryException, retry(
            3, exclude=ZeroDivisionError)(raise_error_all_time))

    @check_expectations
    def testWithExcludeTuple(self):
        """do_not_retry_if_division_by_zero_error"""
        self.assertRaises(RetryException, retry(
            3, exclude=(ZeroDivisionError, ValueError))(raise_error_all_time))

    @check_expectations
    def testWithInclude(self):
        """the_same_error_all_time"""
        self.assertRaises(RetryException, retry(
            3, include=ZeroDivisionError)(raise_error_all_time))

    @check_expectations
    def testWithIncludeAndExclude(self):
        """the_same_error_all_time"""
        self.assertRaises(RetryException, retry(
            3, include=ZeroDivisionError, exclude=FileExistsError)(raise_error_all_time))

    @check_expectations
    def testWithIncludeAndExclude(self):
        """do_not_retry_if_division_by_zero_error"""
        self.assertRaises(RetryException, retry(
            3, include=FileExistsError, exclude=ZeroDivisionError)(raise_error_all_time))
