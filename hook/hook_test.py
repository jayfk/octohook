import os
import six
import unittest
from mock import patch, Mock

os.environ["DEBUG"] = "False"

import hook


class HookTestCase(unittest.TestCase):

    def setUp(self):
        self.app = hook.app.test_client()
        self.repo = Mock()
        self.repo.SECRET = "secret"
        hook.app.add_url_rule(
                        rule="/repo/",
                        endpoint="repo",
                        view_func=hook.hook,
                        methods=["POST"],
                        defaults={"repo": self.repo}
        )

    def test_repo_does_not_exist(self):
        resp = self.app.post("/some-foo/")
        self.assertEqual(resp.status_code, 404)

    @patch("hook.DEBUG")
    def test_signature_not_required_when_in_debug(self, DEBUG_mocked):
        if six.PY2:
            DEBUG_mocked.__nonzero__.return_value = True
        else:
            DEBUG_mocked.__bool__.return_value = True

        resp = self.app.post(
                "/repo/",
                data=b'{"bogus":"data"}',
                headers={"X-Github-Event": "delete"}
        )
        self.assertEqual(resp.status_code, 200)

    @patch("hook.import_repo_by_name")
    def test_signature_does_not_exist(self, import_repo_by_name_mocked):
        import_repo_by_name_mocked.return_value = True

        resp = self.app.post("/repo/")
        self.assertEqual(resp.status_code, 404)

    @patch("hook.is_signed")
    def test_not_signed(self, is_signed_mocked):

        is_signed_mocked.return_value = False

        resp = self.app.post(
                "/repo/",
                headers={'X-Hub-Signature': "sig"},
                data="bla"
        )
        self.assertEqual(resp.status_code, 404)
        is_signed_mocked.assert_called_once_with(
                payload="bla", signature="sig", secret="secret"
        )

    @patch("hook.is_signed")
    def test_event_not_set(self, is_signed_mocked):
        is_signed_mocked.return_value = True

        resp = self.app.post(
                "/repo/",
                headers={'X-Hub-Signature': "sig"},
                data="bla"
        )
        self.assertEqual(resp.status_code, 400)

    @patch("hook.is_signed")
    def test_functions_are_called(self, is_signed_mocked):
        is_signed_mocked.return_value = True

        resp = self.app.post(
                "/repo/",
                headers={'X-Hub-Signature': "sig", "X-Github-Event": "delete"},
                data="bla"
        )
        #self.repo.always.assert_called_once_with(None)
        #self.repo.delete.assert_called_once_with(None)
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

    @patch("hook.imp.load_source")
    def test_secret_is_set(self, load_source):
        mocked_repo = Mock()
        load_source.return_value = mocked_repo
        os.environ["FOO_SECRET"] = "foos-secret"

        repo = hook.import_repo_by_name("foo")

        self.assertEqual(repo.SECRET, "foos-secret")

    @patch("hook.imp.load_source")
    def test_secret_not_set(self, load_source):
        mocked_repo = Mock()
        load_source.return_value = mocked_repo
        with self.assertRaises(AssertionError):
            repo = hook.import_repo_by_name("repo-without-secret")

    @patch("hook.DEBUG")
    @patch("hook.imp.load_source")
    def test_secret_not_set_debug(self, load_source, DEBUG_mocked):
        mocked_repo = Mock()
        load_source.return_value = mocked_repo

        if six.PY2:
            DEBUG_mocked.__nonzero__.return_value = True
        else:
            DEBUG_mocked.__bool__.return_value = True

        repo = hook.import_repo_by_name("repo-without-secret")


class BuildRoutesTestCase(unittest.TestCase):

    @patch("hook.import_repo_by_name")
    @patch("hook.app")
    @patch("hook.os.walk")
    def test_build_routes(self, walk_mocked, app_mocked, import_repo_by_name_mocked):
        walk_mocked.return_value = [("bar", "baz", ["repo_without_secret.py",])]
        import_repo_by_name_mocked.return_value = 'repo-import'
        hook.build_routes()
        app_mocked.add_url_rule.assert_called_once_with(
            defaults={'repo': 'repo-import'},
                endpoint='repo_without_secret',
                methods=['POST'], rule='/repo_without_secret/',
                view_func=hook.hook
        )

    """
    @patch("hook.os.environ")
    @patch("hook.os.walk")
    def test_secret_set(self, walk_mocked, environ_mocked):
        walk_mocked.return_value = [("bar", "baz", ["repo_with_secret.py",])]
        environ_mocked.__contains__.return_value = True
        hook.check_environment()
        environ_mocked.__contains__.assert_called_once_with('REPO_WITH_SECRET_SECRET')"""


if __name__ == '__main__':
    unittest.main()
