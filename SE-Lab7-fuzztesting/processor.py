"""Water Utility Billing application with strict input validation.

Adapted from the user's Lab 6 water_utility_billing.py application.
"""

from math import isfinite
from numbers import Real


def validate_billing_inputs(accounts, base_fee):
    """Validate billing inputs; raise ValueError for malformed data."""
    if not isinstance(accounts, list):
        raise ValueError("accounts must be a list")
    if isinstance(base_fee, bool) or not isinstance(base_fee, Real):
        raise ValueError("base_fee must be a finite non-negative number")
    if not isfinite(float(base_fee)) or base_fee < 0:
        raise ValueError("base_fee must be a finite non-negative number")

    for index, account in enumerate(accounts):
        if not isinstance(account, dict):
            raise ValueError(f"account at index {index} must be a dictionary")

        for flag in ("is_active", "is_commercial", "has_leak_waiver"):
            if flag in account and not isinstance(account[flag], bool):
                raise ValueError(f"{flag} must be a boolean")

        usage_blocks = account.get("usage_blocks", [])
        if not isinstance(usage_blocks, list):
            raise ValueError("usage_blocks must be a list")
        for usage in usage_blocks:
            if isinstance(usage, bool) or not isinstance(usage, Real):
                raise ValueError("each usage value must be a finite number")
            if not isfinite(float(usage)):
                raise ValueError("each usage value must be a finite number")


def calculate_water_bill(accounts, base_fee):
    """Calculate total water charges while preserving the Lab 6 tariff rules."""
    validate_billing_inputs(accounts, base_fee)

    total_billed = 0.0
    flagged_accounts = 0

    for account in accounts:
        if not account.get("is_active", False):
            continue

        usage_blocks = account.get("usage_blocks", [])
        is_commercial = account.get("is_commercial", False)
        acct_total = float(base_fee)

        for usage in usage_blocks:
            if usage <= 0:
                flagged_accounts += 1
                continue

            if usage > 100:
                flagged_accounts += 1
                if not is_commercial:
                    acct_total += usage * 4.5
                    break
                acct_total += usage * 3.5
            elif usage > 50:
                acct_total += usage * 2.5
            else:
                acct_total += usage * 1.5

        if account.get("has_leak_waiver", False) and acct_total > 200.0:
            acct_total -= 50.0

        total_billed += acct_total

    status = "NORMAL"
    if flagged_accounts > 5:
        status = "EXCESSIVE_FLAGS"
    elif total_billed == 0.0:
        status = "NO_ACTIVITY"

    return {"total_billed": round(total_billed, 2), "status": status}


def check_meter_tampering(readings_matrix):
    """Detect two consecutive negative flow deltas in any meter's readings."""
    if not isinstance(readings_matrix, list):
        raise ValueError("readings_matrix must be a list")

    for meter_index, meter in enumerate(readings_matrix):
        if not isinstance(meter, list):
            raise ValueError(f"meter at index {meter_index} must be a list")
        for delta in meter:
            if isinstance(delta, bool) or not isinstance(delta, Real):
                raise ValueError("each meter reading must be a finite number")
            if not isfinite(float(delta)):
                raise ValueError("each meter reading must be a finite number")

    if not readings_matrix:
        return "NO_DATA"

    for meter in readings_matrix:
        backward_flow_count = 0
        for delta in meter:
            if delta < 0:
                backward_flow_count += 1
                if backward_flow_count >= 2:
                    return "TAMPER_SUSPECTED"
            else:
                backward_flow_count = 0
    return "CLEAR"


if __name__ == "__main__":
    sample_accounts = [{
        "is_active": True,
        "is_commercial": False,
        "has_leak_waiver": False,
        "usage_blocks": [30, 60],
    }]
    print("Water Utility Billing — sample execution")
    print("Bill:", calculate_water_bill(sample_accounts, 10))
    print("Meter status:", check_meter_tampering([[10, -2, -3]]))
