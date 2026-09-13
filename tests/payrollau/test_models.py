# -*- coding: utf-8 -*-
"""Checks for documented Australian payroll model fields and enum values."""

import pytest

from xero_python.api_client import ModelFinder
from xero_python.api_client.deserializer import deserialize
from xero_python.api_client.serializer import serialize
from xero_python.payrollau import models


def test_tax_declaration_keeps_the_leave_loading_sgc_flag():
    # given a tax declaration returned with the documented SGC flag
    data = {
        "EmployeeID": "cdfb8371-0b21-4b8a-8903-1024df6c391e",
        "EligibleToReceiveLeaveLoading": True,
        "IncludeLeaveLoadingInSGC": True,
        "IncludeLeaveLoadingInQualifyingEarnings": False,
    }
    # when decoding it
    declaration = deserialize("TaxDeclaration", data, ModelFinder(models))
    # then the flag survives decoding and serialising
    assert declaration.include_leave_loading_in_sgc is True
    assert declaration.include_leave_loading_in_qualifying_earnings is False
    assert serialize(declaration)["IncludeLeaveLoadingInSGC"] is True


def test_payslip_keeps_documented_get_fields():
    # given a payslip response holding the documented fields
    data = {
        "PayslipID": "5037f8ef-e9b5-40a6-9ec1-0f6f7ebb4787",
        "LastName": "Smith",
        "EmployeeGroup": "Sales",
        "LastEdited": "/Date(1573370889000+0000)/",
        "EarningsLines": [
            {
                "EarningsRateID": "ab874dfb-ab09-4c91-954e-43acf6fc23b4",
                "Amount": 100,
                "LumpSumETaxYear": 2021,
            }
        ],
    }
    # when decoding it
    payslip = deserialize("Payslip", data, ModelFinder(models))
    # then the group, edit time and lump sum year are all retained
    assert payslip.employee_group == "Sales"
    assert payslip.last_edited is not None
    assert payslip.earnings_lines[0].lump_sum_e_tax_year == 2021
    assert serialize(payslip.earnings_lines[0])["LumpSumETaxYear"] == 2021


def employee_with(**kwargs):
    """Build an employee with the fields the model requires."""
    return models.Employee(
        first_name="Albus", last_name="Dumbledore", date_of_birth="1980-07-01", **kwargs
    )


@pytest.mark.parametrize("value", ["V", "I", "D", "R", "F", "C", "T"])
def test_employee_accepts_documented_termination_reasons(value):
    # given a documented termination code
    employee = employee_with(termination_reason=value)
    # then it is kept
    assert employee.termination_reason == value


@pytest.mark.parametrize("value", ["None", "X"])
def test_employee_rejects_undocumented_termination_reasons(value):
    with pytest.raises(ValueError):
        employee_with(termination_reason=value)


@pytest.mark.parametrize("value", ["NONE", "UNIONFEES", "WORKPLACEGIVING"])
def test_deduction_type_accepts_documented_categories(value):
    deduction_type = models.DeductionType(deduction_category=value)
    assert deduction_type.deduction_category == value


@pytest.mark.parametrize("value", ["None", "UNION FEES"])
def test_deduction_type_rejects_undocumented_categories(value):
    with pytest.raises(ValueError):
        models.DeductionType(deduction_category=value)
