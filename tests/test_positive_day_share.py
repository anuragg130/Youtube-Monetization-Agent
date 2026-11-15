import pytest

from ytagent.growth import positive_day_share


def test_positive_day_share():
    assert positive_day_share([100, 110, 108, 120, 120]) == 50.0
    assert positive_day_share([1, 2, 3]) == 100.0
    assert positive_day_share([3, 3, 1]) == 0.0
    assert positive_day_share([1, 2, 2, 2]) == 33.33


def test_positive_day_share_needs_two_values():
    with pytest.raises(ValueError):
        positive_day_share([5])
