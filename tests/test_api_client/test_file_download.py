# -*- coding: utf-8 -*-
"""Checks for saving a file response into the configured download folder."""

import os

import pytest

from xero_python.api_client import ApiClient
from xero_python.api_client.configuration import Configuration


class FakeFileResponse:
    def __init__(self, data, content_disposition=None):
        self.data = data
        self.content_disposition = content_disposition

    def getheader(self, name, default=None):
        if name == "Content-Disposition":
            return self.content_disposition or default
        return default


@pytest.fixture()
def api_client(tmp_path):
    configuration = Configuration()
    configuration.temp_folder_path = str(tmp_path)
    return ApiClient(configuration)


def save(api_client, response):
    return api_client._ApiClient__deserialize_file(response)


@pytest.mark.parametrize(
    "filename", ["../escaped.txt", "..\\escaped.txt", "/tmp/escaped.txt"]
)
def test_download_stays_inside_download_folder(api_client, tmp_path, filename):
    # given a response naming a file outside the download folder
    outside = tmp_path.parent / "escaped.txt"
    outside.write_text("original content", encoding="utf-8")
    response = FakeFileResponse(
        b"replacement", 'attachment; filename="{}"'.format(filename)
    )
    # when saving the response
    path = save(api_client, response)
    # then the file is written inside the download folder
    assert os.path.dirname(os.path.abspath(path)) == str(tmp_path)
    assert os.path.basename(path) == "escaped.txt"
    # and the file outside the folder is untouched
    assert outside.read_text(encoding="utf-8") == "original content"


def test_download_does_not_overwrite_an_existing_file(api_client, tmp_path):
    # given a file already saved under the response filename
    existing = tmp_path / "report.txt"
    existing.write_text("first download", encoding="utf-8")
    response = FakeFileResponse(b"second download", 'attachment; filename="report.txt"')
    # when saving another response with the same name
    path = save(api_client, response)
    # then a unique file is allocated and the first one is preserved
    assert os.path.abspath(path) != str(existing)
    assert existing.read_text(encoding="utf-8") == "first download"
    with open(path, "rb") as saved:
        assert saved.read() == b"second download"


@pytest.mark.parametrize(
    "content_disposition,expected",
    [
        ('attachment; filename="quarter one.txt"', "quarter one.txt"),
        ("attachment; filename=report.txt", "report.txt"),
        ("attachment; filename*=UTF-8''quarter%20one.txt", "quarter one.txt"),
    ],
)
def test_download_keeps_the_declared_filename(
    api_client, tmp_path, content_disposition, expected
):
    # given a valid Content-Disposition header
    response = FakeFileResponse(b"file bytes", content_disposition)
    # when saving the response
    path = save(api_client, response)
    # then the whole filename is used and the bytes are preserved
    assert os.path.basename(path) == expected
    with open(path, "rb") as saved:
        assert saved.read() == b"file bytes"


@pytest.mark.parametrize(
    "content_disposition", [None, "attachment", "inline", "attachment; size=42"]
)
def test_download_without_a_filename_uses_a_temporary_name(
    api_client, tmp_path, content_disposition
):
    # given a header declaring no filename
    response = FakeFileResponse(b"file bytes", content_disposition)
    # when saving the response
    path = save(api_client, response)
    # then the bytes are saved under a temporary name in the download folder
    assert os.path.dirname(os.path.abspath(path)) == str(tmp_path)
    with open(path, "rb") as saved:
        assert saved.read() == b"file bytes"
