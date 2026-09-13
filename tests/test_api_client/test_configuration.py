# -*- coding: utf-8 -*-
import xero_python
from xero_python.api_client.configuration import Configuration


def test_configuration_applies_explicit_arguments():
    # given a saved default configuration built without arguments
    try:
        first = Configuration()
        assert first.debug is False
        # when requesting another configuration with explicit arguments
        token = object()
        second = Configuration(debug=True, oauth2_token=token)
        # then the requested values are applied
        assert second.debug is True
        assert second.oauth2_token is token
        # and the saved default is unchanged
        assert Configuration().debug is False
        assert Configuration().oauth2_token is None
    finally:
        Configuration.set_default(None)


def test_configuration_keeps_default_support():
    # given a default configuration set explicitly
    default = Configuration()
    default.temp_folder_path = "default-folder"
    Configuration.set_default(default)
    try:
        # when asking for a configuration without arguments
        # then a copy of the default is returned
        copied = Configuration()
        assert copied is not default
        assert copied.temp_folder_path == "default-folder"
    finally:
        Configuration.set_default(None)


def test_debug_report_states_package_version():
    # given the installed package version
    # when building the debug report
    report = Configuration().to_debug_report()
    # then the report names that version
    assert "SDK Package Version: {}".format(xero_python.__version__) in report
