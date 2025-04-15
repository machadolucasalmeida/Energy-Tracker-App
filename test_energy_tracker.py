import pytest
import os
from energy_tracker import (
    add_appliance,
    calculate_daily_kwh,
    calculate_monthly_kwh,
    calculate_cost,
    save_appliances_to_csv,
    load_appliances_from_csv,
    get_positive_float,
    get_int
)

# ---------------------------
# Business Logic Tests
# ---------------------------

def test_add_appliance():
    app = add_appliance("Lamp", 60, 5)
    assert isinstance(app, dict)
    assert app["name"] == "Lamp"
    assert app["watts"] == 60
    assert app["hours_per_day"] == 5

def test_calculate_daily_kwh():
    # For example: 100W for 2 hours should equal (100*2)/1000 = 0.2 kWh
    daily = calculate_daily_kwh(100, 2)
    assert daily == pytest.approx(0.2)

def test_calculate_monthly_kwh():
    # If daily kWh is 0.2, then monthly kWh should be 0.2 * 30 = 6.0 kWh
    monthly = calculate_monthly_kwh(0.2)
    assert monthly == pytest.approx(6.0)

def test_calculate_cost():
    # If monthly consumption is 6 kWh and price is 0.5 per kWh, cost should be 6 * 0.5 = 3.0
    cost = calculate_cost(6, 0.5)
    assert cost == pytest.approx(3.0)


# ---------------------------
# CSV Persistence Tests
# ---------------------------

def test_csv_persistence(tmp_path):
    # Create a temporary file path for testing CSV persistence
    test_file = tmp_path / "test_appliances.csv"

    appliances = [
        {"name": "Lamp", "watts": 60, "hours_per_day": 5},
        {"name": "TV", "watts": 120, "hours_per_day": 4}
    ]

    # Save the appliances list to CSV
    save_appliances_to_csv(appliances, filename=str(test_file))
    # Now load it back
    loaded = load_appliances_from_csv(filename=str(test_file))
    
    # Check that loaded data has the same number of entries
    assert len(loaded) == len(appliances)
    # Verify each appliance's data (converting numeric fields to float)
    for i in range(len(appliances)):
        assert loaded[i]["name"] == appliances[i]["name"]
        assert loaded[i]["watts"] == pytest.approx(appliances[i]["watts"])
        assert loaded[i]["hours_per_day"] == pytest.approx(appliances[i]["hours_per_day"])


# ---------------------------
# Input Validation Tests Using Monkeypatch
# ---------------------------

def test_get_positive_float(monkeypatch):
    # Test sequence: first a negative number, then a non-numeric string, then a valid positive float.
    inputs = iter(["-5", "abc", "3.5"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    result = get_positive_float("Enter value: ")
    assert result == pytest.approx(3.5)

def test_get_int(monkeypatch):
    # Test sequence: non-numeric input, then an integer out of bounds, then a valid integer.
    inputs = iter(["abc", "0", "5"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    # With a valid range of 1 to 10, after invalid inputs, '5' should be accepted.
    result = get_int("Enter integer: ", 1, 10)
    assert result == 5

# ---------------------------
# Main block for running tests directly
# ---------------------------
if __name__ == "__main__":
    pytest.main()
