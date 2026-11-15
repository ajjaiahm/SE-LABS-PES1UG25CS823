"""Hypothesis-based fuzz tests for all three processor functions.

Install test dependencies with: python -m pip install pytest hypothesis
Run with: python -m pytest -v test_processor.py
"""

import math
import pytest
from hypothesis import given, settings, strategies as st

from processor import (
    calculate_water_bill,
    check_meter_tampering,
    validate_billing_inputs,
)


finite_numbers = st.floats(
    allow_nan=False, allow_infinity=False, width=32
)
valid_usage = st.lists(finite_numbers, min_size=0, max_size=12)
valid_accounts = st.lists(
    st.fixed_dictionaries(
        {
            "is_active": st.booleans(),
            "is_commercial": st.booleans(),
            "has_leak_waiver": st.booleans(),
            "usage_blocks": valid_usage,
        }
    ),
    min_size=0,
    max_size=8,
)


@settings(max_examples=150, deadline=None)
@given(accounts=valid_accounts, base_fee=finite_numbers.filter(lambda x: x >= 0))
def test_validate_billing_inputs_accepts_valid_generated_data(accounts, base_fee):
    assert validate_billing_inputs(accounts, base_fee) is None


@settings(max_examples=150, deadline=None)
@given(
    accounts=st.one_of(
        st.none(), st.text(), st.integers(),
        st.lists(st.one_of(st.none(), st.text(), st.integers()), max_size=5),
    ),
    base_fee=st.one_of(st.text(), st.none(), st.booleans()),
)
def test_validate_billing_inputs_rejects_malformed_data(accounts, base_fee):
    with pytest.raises(ValueError):
        validate_billing_inputs(accounts, base_fee)


@settings(max_examples=150, deadline=None)
@given(accounts=valid_accounts, base_fee=finite_numbers.filter(lambda x: x >= 0))
def test_calculate_water_bill_never_returns_invalid_result(accounts, base_fee):
    result = calculate_water_bill(accounts, base_fee)
    assert set(result) == {"total_billed", "status"}
    assert isinstance(result["total_billed"], float)
    assert math.isfinite(result["total_billed"])
    assert result["total_billed"] >= 0
    assert result["status"] in {"NORMAL", "NO_ACTIVITY", "EXCESSIVE_FLAGS"}


@settings(max_examples=150, deadline=None)
@given(
    accounts=st.lists(st.one_of(st.none(), st.integers(), st.text()), min_size=1, max_size=5),
    base_fee=finite_numbers.filter(lambda x: x >= 0),
)
def test_calculate_water_bill_rejects_non_dictionary_accounts(accounts, base_fee):
    with pytest.raises(ValueError):
        calculate_water_bill(accounts, base_fee)


@settings(max_examples=150, deadline=None)
@given(matrix=st.lists(st.lists(finite_numbers, max_size=15), max_size=8))
def test_check_meter_tampering_returns_documented_status(matrix):
    result = check_meter_tampering(matrix)
    assert result in {"NO_DATA", "CLEAR", "TAMPER_SUSPECTED"}


@settings(max_examples=150, deadline=None)
@given(matrix=st.one_of(st.none(), st.text(), st.integers(), st.lists(st.text(), min_size=1, max_size=5)))
def test_check_meter_tampering_rejects_malformed_matrix(matrix):
    with pytest.raises(ValueError):
        check_meter_tampering(matrix)


@pytest.mark.parametrize("matrix", [[[None]], [[True]], [[float("nan")]], [[float("inf")]], ["bad-meter"]])
def test_check_meter_tampering_rejects_invalid_readings(matrix):
    with pytest.raises(ValueError):
        check_meter_tampering(matrix)


@pytest.mark.parametrize("accounts, fee", [
    ([None], 10),
    ([{"is_active": True, "usage_blocks": "bad"}], 10),
    ([{"is_active": True, "usage_blocks": [float("nan")]}], 10),
    ([], float("inf")),
    ([], True),
])
def test_billing_input_validation_edge_cases(accounts, fee):
    with pytest.raises(ValueError):
        validate_billing_inputs(accounts, fee)
