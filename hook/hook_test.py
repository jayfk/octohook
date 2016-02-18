import os
import six
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
        if six.PY2:
            DEBUG_mocked.__nonzero__.return_value = True
        else:
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

    def test_signature_does_match(self):
        payload = "abdcdefg"
        signature = "sha1=01caaa4f0d511f5c24141c4a1b9777c4b79121f0"
        secret = "some-secret"
        self.assertFalse(
                hook.is_signed(
                    payload=payload,
                    signature=signature,
                    secret=secret
                )
        )

    def test_signature_does_not_match(self):
        payload = "abdcdefg"
        signature = "sha1=6d4d7c822a142b4270cea6b08917d507374834b2"
        secret = "some-secret"
        self.assertTrue(
                hook.is_signed(
                    payload=payload,
                    signature=signature,
                    secret=secret
                )
        )


class ImportRepoByNameTestCase(unittest.TestCase):

    @patch("hook.os.path.exists")
    def test_path_does_not_exist(self, exists_mocked):
        exists_mocked.return_value = False
        self.assertEqual(
            hook.import_repo_by_name("foo"),
            False
        )
        self.assertTrue(exists_mocked.called)

    @patch("hook.imp.load_source")
    @patch("hook.os.path.exists")
    def test_secret_is_set(self, exists_mocked, load_source):
        exists_mocked.return_value = True
        mocked_repo = Mock()
        load_source.return_value = mocked_repo
        os.environ["FOO_SECRET"] = "foos-secret"

        repo = hook.import_repo_by_name("foo")

        self.assertEqual(repo.SECRET, "foos-secret")


class CheckEnvironmentTestCase(unittest.TestCase):

    @patch("hook.os.walk")
    def test_secret_not_set(self, walk_mocked):
        walk_mocked.return_value = [("bar", "baz", ["repo_without_secret.py",])]
        with self.assertRaises(AssertionError):
            hook.check_environment()

    @patch("hook.os.environ")
    @patch("hook.os.walk")
    def test_secret_set(self, walk_mocked, environ_mocked):
        walk_mocked.return_value = [("bar", "baz", ["repo_with_secret.py",])]
        environ_mocked.__contains__.return_value = True
        hook.check_environment()
        environ_mocked.__contains__.assert_called_once_with('REPO_WITH_SECRET_SECRET')


if __name__ == '__main__':
    unittest.main()
