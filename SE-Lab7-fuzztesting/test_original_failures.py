
import pytest
from hypothesis import given, strategies as st

from processor_original import (
    calculate_water_bill,
    check_meter_tampering
)


@given(st.sampled_from([None, 10, "invalid", []]))
def test_original_rejects_invalid_accounts(account):
    with pytest.raises(ValueError):
        calculate_water_bill([account], 10)


@given(st.sampled_from(["invalid", None, [], {}]))
def test_original_rejects_invalid_usage(usage):
    with pytest.raises(ValueError):
        calculate_water_bill(
            [{"is_active": True, "usage_blocks": [usage]}],
            10
        )


@given(st.sampled_from(["invalid", None, {}, []]))
def test_original_rejects_invalid_meter_readings(reading):
    with pytest.raises(ValueError):
        check_meter_tampering([[reading]])
