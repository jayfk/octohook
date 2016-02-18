import os

import unittest
from mock import patch, Mock

os.environ["DEBUG"] = "False"

import hook


class HookTestCase(unittest.TestCase):

    def setUp(self):
        self.app = hook.app.test_client()

    def test_repo_does_not_exist(self):
        resp = self.app.post("/some-foo/")
        self.assertEqual(resp.status_code, 404)

    @patch("hook.import_repo_by_name")
    @patch("hook.DEBUG")
    def test_signature_not_required_when_in_debug(self, DEBUG_mocked, import_repo_by_name_mocked):
        import_repo_by_name_mocked.return_value = True
        DEBUG_mocked.__bool__.return_value = True

        resp = self.app.post(
                "/some-foo/",
                data=b'{"bogus":"data"}',
                headers={"X-Github-Event": "delete"}
        )
        self.assertEqual(resp.status_code, 200)

    @patch("hook.import_repo_by_name")
    def test_signature_does_not_exist(self, import_repo_by_name_mocked):
        import_repo_by_name_mocked.return_value = True

        resp = self.app.post("/some-foo/")
        self.assertEqual(resp.status_code, 404)

    @patch("hook.is_signed")
    @patch("hook.import_repo_by_name")
    def test_not_signed(self, import_repo_by_name_mocked, is_signed_mocked):
        repo = Mock()
        repo.SECRET = "secret"
        import_repo_by_name_mocked.return_value = repo
        is_signed_mocked.return_value = False

        resp = self.app.post(
                "/some-foo/",
                headers={'X-Hub-Signature': "sig"},
                data="bla"
        )
        self.assertEqual(resp.status_code, 404)
        is_signed_mocked.assert_called_once_with(
                payload="bla", signature="sig", secret="secret"
        )


    @patch("hook.is_signed")
    @patch("hook.import_repo_by_name")
    def test_event_not_set(self, import_repo_by_name_mocked, is_signed_mocked):
        repo = Mock()
        repo.SECRET = "secret"
        import_repo_by_name_mocked.return_value = repo
        is_signed_mocked.return_value = True

        resp = self.app.post(
                "/some-foo/",
                headers={'X-Hub-Signature': "sig"},
                data="bla"
        )
        self.assertEqual(resp.status_code, 400)

    @patch("hook.is_signed")
    @patch("hook.import_repo_by_name")
    def test_functions_are_called(self, import_repo_by_name_mocked, is_signed_mocked):
        repo = Mock()
        repo.SECRET = "secret"
        import_repo_by_name_mocked.return_value = repo
        is_signed_mocked.return_value = True

        resp = self.app.post(
                "/some-foo/",
                headers={'X-Hub-Signature': "sig", "X-Github-Event": "delete"},
                data="bla"
        )
        repo.always.assert_called_once_with(None)
        repo.delete.assert_called_once_with(None)
        self.assertEqual(resp.status_code, 200)


class IsSignedTestCase(unittest.TestCase):
    pass


class ImportRepoByNameTestCase(unittest.TestCase):
    pass


class CheckEnvironmentTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
