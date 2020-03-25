"""
Tests for checker class
"""

import unittest
import unittest.mock as mock
import subprocess

from libs.checker import checker


class DummyObject:
    """
    Dummy object to retrieve responses
    """
    args = []
    returncode = 0
    status_code = 0
    content = ''


class TestChecker(unittest.TestCase):
    """
    Tests for checker.py
    """

    def setUp(self):
        good_site = {"name": "example.com",
                     "ping": True, "paths": [["/", "Example"]]}
        good_site_no_ping = {"name": "example.com",
                             "ping": False, "paths": [["/", "Example"]]}
        fail_site1 = {"name": "example.com", "ping": True,
                      "paths": [["/", "PWKQEOBWUQNQPQRHILUN"]]}
        fail_site2 = {"name": "PWKQEOBWUQNQPQRHILUN.org",
                      "ping": True, "paths": [["/", "Example"]]}
        fail_site3 = {"name": "PWKQEOBWUQNQPQRHILUN.org",
                      "ping": False, "paths": [["/", "Example"]]}

        self.ckr = checker.Checker(good_site)
        self.fail2 = checker.Checker(fail_site1)
        self.fail3 = checker.Checker(fail_site2)
        self.fail4 = checker.Checker(fail_site3)
        self.no_ping = checker.Checker(good_site_no_ping)

    def test_ping_host_success(self):
        """
        Test that pinging host works and responds properly
        """
        completed_process = DummyObject()
        completed_process.returncode = 0
        subprocess.run = mock.create_autospec(
            subprocess.run, return_value=completed_process)
        response = self.ckr._Checker__ping_host()
        self.assertEqual(response, 0)

    def test_ping_host_fail(self):
        """
        Test that pinging fails gracefully
        """
        response = self.fail3._Checker__ping_host()
        self.assertNotEqual(response, 0)

    def test_check_page_success(self):
        """
        Test that retrieving content from page successfully calls next method
        """
        # c = checker.Checker("example.com", [["/", "Example"]])
        ckr = self.ckr
        ckr._Checker__check_page_content = mock.Mock()
        ckr._Checker__write_to_log = mock.Mock()
        ckr._Checker__check_page()
        ckr._Checker__check_page_content.assert_called()

    def test_check_page_fail(self):
        """
        Test that not retrieving page writes to log
        """
        ckr = self.fail3
        ckr._Checker__check_page_content = mock.Mock()
        ckr._Checker__write_to_log = mock.Mock()
        ckr._Checker__check_page()
        ckr._Checker__check_page_content.assert_not_called()

    def test_check_page_content_success(self):
        """
        Test content match
        """
        ckr = self.ckr
        ckr._Checker__write_to_log = mock.Mock()
        ckr._Checker__check_page()
        ckr._Checker__write_to_log.assert_not_called()

    def test_check_page_content_fail(self):
        """
        Test that not retrieving page writes to log
        """
        ckr = self.fail2
        ckr._Checker__write_to_log = mock.Mock()
        ckr._Checker__check_page()
        ckr._Checker__write_to_log.assert_called()

    def test_if_checker_receives_true_as_last_arg_ping_is_skipped(self):
        """
        Test that ping is skipped if last arg is true
        """
        response = self.fail4._Checker__ping_host()
        self.assertEqual(response, 0)

    def test_checker_without_ping_scans_content(self):
        """
        Test that content is scanned still if no ping is set
        """
        ckr = self.no_ping
        ckr._Checker__write_to_log = mock.Mock()
        ckr._Checker__check_page()
        ckr._Checker__write_to_log.assert_not_called()


if __name__ == "__main__":
    unittest.main()
