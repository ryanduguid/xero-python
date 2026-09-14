"""Australian payroll requests use fabricated data and an inert transport."""

from unittest.mock import Mock

import pytest

from xero_python.api_client import ApiClient, Configuration, ModelFinder
from xero_python.api_client.deserializer import deserialize
from xero_python.api_client.serializer import serialize
from xero_python.payrollau import PayrollAuApi, models


@pytest.fixture
def api():
    client = ApiClient(Configuration())
    client.call_api = Mock(return_value=None)
    return PayrollAuApi(client)


@pytest.mark.parametrize("as_model", [False, True])
def test_partial_updates_preserve_only_supplied_fields(api, as_model):
    employee = {"MiddleNames": "Example"}
    pay_run = {"PayRunStatus": "DRAFT"}
    if as_model:
        employee = models.Employee(middle_names="Example")
        pay_run = models.PayRun(pay_run_status=models.PayRunStatus.DRAFT)
    api.update_employee("tenant", "employee", [employee])
    assert serialize(api.api_client.call_api.call_args.kwargs["body"]) == [
        {"MiddleNames": "Example"}
    ]
    api.update_pay_run("tenant", "pay-run", [pay_run])
    assert serialize(api.api_client.call_api.call_args.kwargs["body"]) == [
        {"PayRunStatus": "DRAFT"}
    ]


@pytest.mark.parametrize("as_model", [False, True])
@pytest.mark.parametrize(
    "missing", ["FirstName", "LastName", "DateOfBirth", "HomeAddress", None]
)
def test_employee_creation_keeps_required_fields(api, as_model, missing):
    payload = {
        "FirstName": "Example",
        "LastName": "Person",
        "DateOfBirth": "/Date(331344000000)/",
        "HomeAddress": {
            "AddressLine1": "1 Example Street",
            "City": "Sydney",
            "Region": "NSW",
            "PostalCode": "2000",
            "Country": "AUSTRALIA",
        },
    }
    if missing:
        payload.pop(missing)
    employee = (
        deserialize("Employee", payload, ModelFinder(models)) if as_model else payload
    )
    if missing:
        with pytest.raises(ValueError, match=missing):
            api.create_employee("tenant", [employee])
        api.api_client.call_api.assert_not_called()
    else:
        api.create_employee("tenant", [employee])
        assert serialize(api.api_client.call_api.call_args.kwargs["body"]) == [payload]


@pytest.mark.parametrize("as_model", [False, True])
def test_pay_run_creation_requires_calendar_and_allows_one_record(api, as_model):
    incomplete = models.PayRun() if as_model else {}
    with pytest.raises(ValueError, match="PayrollCalendarID"):
        api.create_pay_run("tenant", [incomplete])
    complete = (
        models.PayRun(payroll_calendar_id="calendar")
        if as_model
        else {"PayrollCalendarID": "calendar"}
    )
    with pytest.raises(ValueError, match="one pay run"):
        api.create_pay_run("tenant", [complete, complete])
    api.api_client.call_api.assert_not_called()
    api.create_pay_run("tenant", [complete])
    assert serialize(api.api_client.call_api.call_args.kwargs["body"]) == [
        {"PayrollCalendarID": "calendar"}
    ]


@pytest.mark.parametrize("value", [None, False, True])
def test_leave_line_flag_is_optional_and_preserves_explicit_values(value):
    line = models.LeaveLine(is_qualifying_earnings=value)
    assert serialize(line) == ({} if value is None else {"IsQualifyingEarnings": value})


@pytest.mark.parametrize("as_model", [False, True])
@pytest.mark.parametrize("value", [None, False, True])
def test_leave_type_response_flag_is_omitted_from_pay_item_requests(
    api, as_model, value
):
    leave = models.LeaveType(name="Annual leave", is_qualifying_earnings=value)
    item = models.PayItem(leave_types=[leave])
    original = serialize(item)
    payload = item if as_model else original
    api.create_pay_item("tenant", payload)
    assert serialize(api.api_client.call_api.call_args.kwargs["body"]) == {
        "LeaveTypes": [{"Name": "Annual leave"}]
    }
    assert leave.is_qualifying_earnings is value
    assert serialize(item) == original


@pytest.mark.parametrize(
    "model", [models.DeductionType, models.LeaveType, models.ReimbursementType]
)
@pytest.mark.parametrize("length", [49, 50, 51, 100])
def test_pay_item_names_use_their_own_limits(model, length):
    if length > 50:
        with pytest.raises(ValueError):
            model(name="a" * length)
    else:
        assert model(name="a" * length).name == "a" * length


def test_earnings_rate_requirement_and_longer_name_limit_remain():
    with pytest.raises(ValueError, match="is_qualifying_earnings"):
        models.EarningsRate()
    assert (
        models.EarningsRate(
            name="a" * 100, is_qualifying_earnings=False
        ).is_qualifying_earnings
        is False
    )
    with pytest.raises(ValueError):
        models.EarningsRate(name="a" * 101, is_qualifying_earnings=False)


@pytest.mark.parametrize("payload", [{}, {"LeaveTypes": None}, {"LeaveTypes": []}])
def test_absent_leave_type_collections_keep_their_shape(api, payload):
    api.create_pay_item("tenant", payload)
    assert api.api_client.call_api.call_args.kwargs["body"] == payload
