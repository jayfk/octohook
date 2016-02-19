# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


def always(data):
    """Any time any event is triggered (Wildcard Event)."""
    print(data)


def commit_comment(data):
    """Any time a Commit is commented on.
    See: https://developer.github.com/v3/activity/events/types/#commitcommentevent
    """
    print(data)


def create(data):
    """Any time a Branch or Tag is created.
    See: https://developer.github.com/v3/activity/events/types/#createevent
    """
    print(data)


def delete(data):
    """Any time a Branch or Tag is deleted.
    See: https://developer.github.com/v3/activity/events/types/#deleteevent
    """
    print(data)


def deployment(data):
    """Any time a Repository has a new deployment created from the API.
    See: https://developer.github.com/v3/activity/events/types/#deploymentevent
    """
    print(data)


def deployment_status(data):
    """Any time a deployment for a Repository has a status update from the API.
    See: https://developer.github.com/v3/activity/events/types/#deploymentstatusevent
    """
    print(data)


def fork(data):
    """Any time a Repository is forked.
    See: https://developer.github.com/v3/activity/events/types/#forkevent
    """
    print(data)


def gollum(data):
    """Any time a Wiki page is updated.
    See: https://developer.github.com/v3/activity/events/types/#gollumevent
    """
    print(data)


def issue_comment(data):
    """Any time an Issue or Pull Request is commented on.
    See: https://developer.github.com/v3/activity/events/types/#issuecommentevent
    """
    print(data)


def issues(data):
    """Any time an Issue is assigned, unassigned, labeled, unlabeled, opened, closed, or reopened.
    See: https://developer.github.com/v3/activity/events/types/#issuesevent
    """
    print(data)


def member(data):
    """Any time a User is added as a collaborator to a non-Organization Repository.
    See: https://developer.github.com/v3/activity/events/types/#memberevent
    """
    print(data)


def membership(data):
    """Any time a User is added or removed from a team. Organization hooks only.
    See: https://developer.github.com/v3/activity/events/types/#membershipevent
    """
    print(data)


def page_build(data):
    """Any time a Pages site is built or results in a failed build.
    See: https://developer.github.com/v3/activity/events/types/#pagebuildevent
    """
    print(data)


def public(data):
    """Any time a Repository changes from private to public.
    See: https://developer.github.com/v3/activity/events/types/#publicevent
    """
    print(data)


def pull_request_review_comment(data):
    """Any time a comment is created on a portion of the unified diff of a pull request (the Files
    Changed tab).
    See: https://developer.github.com/v3/activity/events/types/#pullrequestreviewcommentevent
    """
    print(data)


def pull_request(data):
    """Any time a Pull Request is assigned, unassigned, labeled, unlabeled, opened, closed,
    reopened, or synchronized (updated due to a new push in the branch that the pull request is
    tracking).
    See: https://developer.github.com/v3/activity/events/types/#pullrequestevent
    """
    print(data)


def push(data):
    """Any Git push to a Repository, including editing tags or branches. Commits via API
            actions that update references are also counted. This is the default event.
    See: https://developer.github.com/v3/activity/events/types/#pushevent
    """
    print(data)


def repository(data):
    """Any time a Repository is created. Organization hooks only.
    See: https://developer.github.com/v3/activity/events/types/#repositoryevent
    """
    print(data)


def release(data):
    """Any time a Release is published in a Repository.
    See: https://developer.github.com/v3/activity/events/types/#releaseevent
    """
    print(data)


def status(data):
    """Any time a Repository has a status update from the API
    See: https://developer.github.com/v3/activity/events/types/#statusevent
    """
    print(data)


def team_add(data):
    """Any time a team is added or modified on a Repository.
    See: https://developer.github.com/v3/activity/events/types/#teamaddevent
    """
    print(data)


def watch(data):
    """Any time a User stars a Repository.
    See: https://developer.github.com/v3/activity/events/types/#watchevent
    """
    print(data)
