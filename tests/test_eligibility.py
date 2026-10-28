from ytagent.eligibility import is_eligible


def test_eligible():
    assert is_eligible(1500, 4200)


def test_not_eligible():
    assert not is_eligible(900, 5000)
