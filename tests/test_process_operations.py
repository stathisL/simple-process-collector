import unittest

from src import process_operations


class TestProcessOperations(unittest.TestCase):
    """
    Unit tests for the process_operations module.
    """

    def test_get_already_running_process_name(self):
        self.assertEqual(process_operations.check_if_process_running("systemd"), True)

    def test_get_process_with_empty_name(self):
        self.assertRaises(Exception, lambda: process_operations.check_if_process_running(""))

    def test_get_relative_process_name(self):
        self.assertRaises(Exception, lambda: process_operations.check_if_process_running("sistemd"))

    def test_proc_id_get_correct_name(self):
        self.assertEqual(process_operations.find_process_id_by_name("systemd")[0]["name"], "systemd")

    def test_proc_id_get_correct_pid_from_name(self):
        self.assertEqual(process_operations.find_process_id_by_name("systemd")[0]["pid"], 1)

    def test_proc_id_get_nonexistent_pid_from_name(self):
        self.assertRaises(IndexError, lambda: process_operations.find_process_id_by_name("sustemd")[0])


if __name__ == '__main__':
    unittest.main()
