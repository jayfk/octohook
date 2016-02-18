import unittest
from hook import hook
from mock import patch


class HookTestCase(unittest.TestCase):

    def test_some_foo(self):
        self.assertEqual("foo", "foo")


class IsSignedTestCase(unittest.TestCase):
    pass


class ImportRepoByNameTestCase(unittest.TestCase):
    pass


class CheckEnvironmentTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
