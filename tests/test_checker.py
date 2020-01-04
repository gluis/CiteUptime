import unittest
from unittest.mock import MagicMock
import unittest.mock as mock

from libs.checker import checker

import requests
import subprocess


class DummyObject:
    args = []
    returncode = 0
    status_code = 0
    content = ''


class TestChecker(unittest.TestCase):

    def setUp(self):
        self.c = checker.Checker("example.com", [["/", "Example"]])
        self.f2 = checker.Checker(
            "example.com", [["/", "PWKQEOBWUQNQPQRHILUN"]])
        self.f3 = checker.Checker(
            "PWKQEOBWUQNQPQRHILUN.org", [["/", "Example"]])

    def test_ping_host_success(self):
        """
        Test that pinging host works and responds properly
        """
        completed_process = DummyObject()
        completed_process.returncode = 0
        subprocess.run = mock.create_autospec(
            subprocess.run, return_value=completed_process)
        response = self.c._Checker__ping_host()
        self.assertEqual(response, 0)

    def test_ping_host_fail(self):
        """
        Test that pinging fails gracefully
        """
        response = self.f3._Checker__ping_host()
        self.assertNotEqual(response, 0)

    def test_check_page_success(self):
        """
        Test that retrieving content from page successfully calls next method
        """
        # c = checker.Checker("example.com", [["/", "Example"]])
        c = self.c
        c._Checker__check_page_content = mock.Mock()
        c._Checker__write_to_log = mock.Mock()
        c._Checker__check_page()
        c._Checker__check_page_content.assert_called()

    def test_check_page_fail(self):
        """
        Test that not retrieving page writes to log
        """
        c = self.f3
        c._Checker__check_page_content = mock.Mock()
        c._Checker__write_to_log = mock.Mock()
        c._Checker__check_page()
        c._Checker__check_page_content.assert_not_called()

    def test_check_page_content_success(self):
        """
        Test content match
        """
        c = self.c
        c._Checker__write_to_log = mock.Mock()
        c._Checker__check_page()
        c._Checker__write_to_log.assert_not_called()

    def test_check_page_content_fail(self):
        """
        Test that not retrieving page writes to log
        """
        c = self.f2
        c._Checker__write_to_log = mock.Mock()
        c._Checker__check_page()
        c._Checker__write_to_log.assert_called()


if __name__ == "__main__":
    unittest.main()
