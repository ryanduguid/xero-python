# -*- coding: utf-8 -*-
"""Checks that App Store enum fields accept only their documented values."""

import pytest

from xero_python.appstore import models

DOCUMENTED = [
    ("Product", "type", ["FIXED", "PER_SEAT", "METERED", "SIMPLE"]),
    ("Plan", "status", ["ACTIVE", "CANCELED", "PENDING_ACTIVATION"]),
    ("Subscription", "status", ["ACTIVE", "CANCELED", "PAST_DUE"]),
    ("SubscriptionItem", "status", ["ACTIVE", "CANCELED", "PENDING_ACTIVATION"]),
]


def set_value(model_name, field, value):
    """Assign the value through the field setter that validates it.

    The constructors require several unrelated fields, so the setter is
    exercised on a bare instance: it only validates and stores the value.
    """
    model = getattr(models, model_name)
    instance = model.__new__(model)
    setattr(instance, field, value)
    return getattr(instance, field)


@pytest.mark.parametrize("model_name,field,values", DOCUMENTED)
def test_documented_values_are_accepted(model_name, field, values):
    for value in values:
        assert set_value(model_name, field, value) == value


@pytest.mark.parametrize("model_name,field,values", DOCUMENTED)
def test_undocumented_none_string_is_rejected(model_name, field, values):
    # the literal string "None" is not one of the documented values
    with pytest.raises(ValueError):
        set_value(model_name, field, "None")
    with pytest.raises(ValueError):
        set_value(model_name, field, "NOT_A_STATUS")
