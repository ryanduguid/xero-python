# -*- coding: utf-8 -*-
"""Checks for the Files association count query and response contract."""

import pytest

from xero_python.api_client import ApiClient
from xero_python.api_client.configuration import Configuration
from xero_python.file import FilesApi


class FakeAuthToken:
    def get_auth_settings(self):
        return {
            "type": "oauth2",
            "in": "header",
            "key": "Authorization",
            "value": "Bearer fake-access-token",
        }


class FakeRestResponse:
    def __init__(self, text):
        self.text = text
        self.data = text.encode("utf-8")
        self.status = 200
        self.reason = "OK"

    def getheaders(self):
        return {}

    def getheader(self, name, default=None):
        return default


class FakeRestClient:
    def __init__(self, text):
        self.text = text
        self.calls = []

    def GET(self, url, query_params=None, **kwargs):
        self.calls.append((url, query_params))
        return FakeRestResponse(self.text)


@pytest.fixture()
def files_api():
    configuration = Configuration()
    configuration.oauth2_token = FakeAuthToken()
    api_client = ApiClient(configuration)
    api_client.rest_client = FakeRestClient('{"9f1a": 2, "7c3b": 1}')
    return FilesApi(api_client)


def test_association_count_sends_one_comma_separated_parameter(files_api):
    # given two object ids
    object_ids = [
        "9f1a3f0e-4b5c-4d6e-8f70-1a2b3c4d5e6f",
        "7c3b2d1e-0a9b-4c8d-7e6f-5a4b3c2d1e0f",
    ]
    # when counting their associations
    files_api.get_associations_count("xero-tenant-id", object_ids)
    # then one ObjectIds parameter carries the documented comma separated list
    url, query_params = files_api.api_client.rest_client.calls[0]
    assert query_params == [("ObjectIds", ",".join(object_ids))]


def test_association_count_returns_the_response_object(files_api):
    # given a response holding a count per object id
    # when counting associations
    counts = files_api.get_associations_count(
        "xero-tenant-id", ["9f1a3f0e-4b5c-4d6e-8f70-1a2b3c4d5e6f"]
    )
    # then the generic object response is returned unchanged
    assert counts == {"9f1a": 2, "7c3b": 1}
