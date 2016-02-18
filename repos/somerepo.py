# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


def always(data):
    """all Any time any event is triggered (Wildcard Event)."""
    pass


def commit_comment(data):
    """commit_comment	Any time a Commit is commented on."""
    pass


def create(data):
    """create	Any time a Branch or Tag is created."""
    pass


def delete(data):
    """delete	Any time a Branch or Tag is deleted."""
    pass


def deployment(data):
    """deployment	Any time a Repository has a new deployment created from the API."""
    pass


def deployment_status(data):
    """deployment_status	Any time a deployment for a Repository has a status update from the API."""
    pass


def fork(data):
    """fork	Any time a Repository is forked."""
    pass


def gollum(data):
    """gollum	Any time a Wiki page is updated."""
    pass


def issue_comment(data):
    """issue_comment	Any time an Issue or Pull Request is commented on."""
    pass


def issues(data):
    """issues	Any time an Issue is assigned, unassigned, labeled, unlabeled, opened, closed, or
            reopened."""


def member(data):
    """member	Any time a User is added as a collaborator to a non-Organization Repository."""
    pass


def membership(data):
    """membership	Any time a User is added or removed from a team. Organization hooks only."""
    pass


def page_build(data):
    """page_build	Any time a Pages site is built or results in a failed build."""
    pass


def public(data):
    """public	Any time a Repository changes from private to public."""
    pass


def pull_request_review_comment(data):
    """pull_request_review_comment	Any time a comment is created on a portion of the unified diff
                                of a pull request (the Files Changed tab)."""
    pass


def pull_request(data):
    """pull_request	Any time a Pull Request is assigned, unassigned, labeled, unlabeled, opened,
                    closed, reopened, or synchronized (updated due to a new push in the branch
                    that the pull request is tracking)."""
    pass


def push(data):
    """push	Any Git push to a Repository, including editing tags or branches. Commits via API
            actions that update references are also counted. This is the default event."""
    pass


def repository(data):
    """repository	Any time a Repository is created. Organization hooks only."""
    pass


def release(data):
    """release	Any time a Release is published in a Repository."""
    pass


def status(data):
    """status	Any time a Repository has a status update from the API"""
    pass


def team_add(data):
    """team_add	Any time a team is added or modified on a Repository."""
    pass


def watch(data):
    """watch	Any time a User stars a Repository."""
    print(data)
    print("called watch :)")
