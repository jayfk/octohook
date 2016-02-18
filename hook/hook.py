# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import os
import imp
import hmac
import hashlib
import six

from flask import Flask, abort, request

DEBUG = os.environ.get("DEBUG", False) == 'True'
HOST = os.environ.get("HOST", '0.0.0.0')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DIR = os.path.join(ROOT_DIR, "repos")
GITHUB_EVENTS = [
    "commit_comment",
    "create",
    "delete",
    "deployment",
    "deployment_status",
    "fork",
    "gollum",
    "issue_comment",
    "issues",
    "member",
    "membership",
    "page_build",
    "public",
    "pull_request_review_comment",
    "pull_request",
    "push",
    "repository",
    "release",
    "status",
    "team_add",
    "watch"
]

app = Flask(__name__)


@app.route('/<repo>/', methods=["POST"])
def hook(repo):
    """Processes an incoming webhook, see GITHUB_EVENTS for possible events.
    """
    # import the code and check that it is there
    repo = import_repo_by_name(repo)
    if not repo:
        abort(404)
    event, signature = (
        request.headers.get('X-Github-Event', False),
        request.headers.get('X-Hub-Signature', False)
    )
    # If we are not running on DEBUG, the X-Hub-Signature header has to be set.
    # Raising a 404 is not the right http return code, but we don't
    # want to give someone that is attacking this endpoint a clue
    # that we are serving this repo alltogether if he doesn't
    # know our secret key
    if not DEBUG:
        if not signature:
            abort(404)
        # Check that the payload is signed by the secret key. Again,
        # if this is not the case, abort with a 404
        if not is_signed(payload=request.get_data(as_text=True), signature=signature, secret=repo.SECRET):
            abort(404)

    # make sure the event is set
    if event not in GITHUB_EVENTS:
        abort(400)

    data = request.get_json()

    # call the always function and the event function (when implemented)
    for function in ["always", event]:
        if hasattr(repo, function):
            getattr(repo, function)(data)

    return "ok"


def is_signed(payload, signature, secret):
    """
    https://developer.github.com/webhooks/securing/#validating-payloads-from-github
    """
    if six.PY3:
        payload = payload.encode("utf-8")
        secret = secret.encode("utf-8")

    digest = "sha1=" + hmac.new(
            secret,
            msg=payload,
            digestmod=hashlib.sha1
    ).hexdigest()
    return digest == signature


def import_repo_by_name(name):
    module_name = ".".join(["repos", name])
    full_path = os.path.join(REPO_DIR, name + ".py")
    if not os.path.exists(full_path):
        return False

    module = imp.load_source(module_name, full_path)
    env_var = "{name}_SECRET".format(name=name.upper())
    setattr(module, "SECRET", os.environ.get(env_var))

    return module


def check_environment():
    for _, _, filenames in os.walk(REPO_DIR):
        for filename in filenames:
            if filename.endswith(".py"):
                name, _, _ = filename.partition(".py")
                env_var = "{name}_SECRET".format(name=name.upper())
                if env_var not in os.environ:
                    raise AssertionError(
                            "You need to set {env_var}".format(
                                    env_var=env_var)
                    )


if __name__ == "__main__":
    check_environment()
    app.run(host=HOST, debug=DEBUG)
