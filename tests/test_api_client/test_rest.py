# -*- coding: utf-8 -*-
"""Transport level checks for xero_python.rest.RESTClientObject."""

import email
import io

import pytest
import urllib3
from urllib3.filepost import encode_multipart_formdata

from xero_python.api_client.configuration import Configuration
from xero_python.rest import RESTClientObject


class FakePoolManager:
    """Records request arguments instead of opening a connection."""

    def __init__(self):
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        response = urllib3.HTTPResponse(
            body=io.BytesIO(b"{}"), status=200, preload_content=False
        )
        return response


@pytest.fixture()
def rest_client():
    client = RESTClientObject(Configuration())
    client.pool_manager = FakePoolManager()
    return client


@pytest.mark.parametrize(
    "request_timeout,expected_total",
    [(0.25, 0.25), (1.0, 1.0), (1, 1)],
)
def test_scalar_timeout_reaches_transport(rest_client, request_timeout, expected_total):
    # given a scalar request timeout
    # when performing a request
    rest_client.request(
        "GET",
        "https://api.xero.com/api.xro/2.0/Invoices",
        _request_timeout=request_timeout,
    )
    # then the transport receives it as the total timeout
    method, url, kwargs = rest_client.pool_manager.calls[0]
    assert isinstance(kwargs["timeout"], urllib3.Timeout)
    assert kwargs["timeout"].total == expected_total


def test_pair_timeout_reaches_transport(rest_client):
    # given a connection and read timeout pair
    # when performing a request
    rest_client.request(
        "GET",
        "https://api.xero.com/api.xro/2.0/Invoices",
        _request_timeout=(0.25, 1.5),
    )
    # then both values reach the transport
    method, url, kwargs = rest_client.pool_manager.calls[0]
    assert kwargs["timeout"].connect_timeout == 0.25
    assert kwargs["timeout"].read_timeout == 1.5


def upload(rest_client, body, mime_type="text/plain"):
    """Send one multipart upload and return the encoded request body."""
    rest_client.request(
        "POST",
        "https://api.xero.com/files.xro/1.0/Files",
        headers={"Content-Type": "multipart/form-data"},
        post_params=[
            ("body", body),
            ("name", "quarter one.txt"),
            ("filename", "quarter one.txt"),
            ("mimeType", mime_type),
        ],
        body=body,
    )
    method, url, kwargs = rest_client.pool_manager.calls[0]
    encoded, content_type = encode_multipart_formdata(
        kwargs["fields"], boundary=kwargs["multipart_boundary"]
    )
    return kwargs, encoded, content_type


def parse_parts(encoded, content_type):
    message = email.message_from_bytes(
        b"Content-Type: "
        + content_type.encode("utf-8")
        + b"\r\nMIME-Version: 1.0\r\n\r\n"
        + encoded
    )
    return message.get_payload()


def test_multipart_boundary_does_not_split_file_content(rest_client):
    # given file content holding the previously hard coded boundary
    body = b"before\r\n-------boundary\r\nafter\r\n"
    kwargs, encoded, content_type = upload(rest_client, body)
    # then the boundary is unique to the request and absent from the content
    assert kwargs["multipart_boundary"] != "-----boundary"
    assert kwargs["multipart_boundary"].encode("utf-8") not in body
    # and the upload encodes as one part holding the whole payload
    parts = parse_parts(encoded, content_type)
    assert len(parts) == 1
    assert parts[0].get_payload(decode=True) == body


def test_multipart_part_declares_supplied_mime_type(rest_client):
    # given an upload declaring its media type
    kwargs, encoded, content_type = upload(
        rest_client, b"file bytes", mime_type="application/octet-stream"
    )
    # then the file part carries that media type
    parts = parse_parts(encoded, content_type)
    assert len(parts) == 1
    assert parts[0].get_content_type() == "application/octet-stream"
    assert parts[0].get_payload(decode=True) == b"file bytes"
