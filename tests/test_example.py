import pytest

from pytemplate.example import linspace, randomize


@pytest.mark.parametrize(
    "start,stop,n,expected",
    [
        (0, 1, 11, [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
        (2, 3, 5, [2.0, 2.25, 2.5, 2.75, 3.0]),
        (0, 10, 11, [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]),
        (0, 0.5, 6, [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]),
        (100, 102, 4, [100.0, 100.6667, 101.3333, 102.0]),
    ],
)
def test_linspace(start, stop, n, expected):
    """Test pytemplate.example.linspace."""

    assert linspace(start, stop, n) == pytest.approx(expected)


@pytest.mark.parametrize(
    "values,amount",
    [
        ([0, 1, 2], 10.0),
        ([1.1, 2.5, 300.7], 1.0),
    ],
)
def test_randomize(values, amount):
    """Test pytemplate.example.randomize."""

    assert randomize(values, amount) == pytest.approx(values, abs=amount)
