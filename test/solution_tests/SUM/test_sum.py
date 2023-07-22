import pytest
from solutions.SUM import sum_solution


class TestSum():
    def test_sum_of_valid_numbers_returns_sum(self):
        assert sum_solution.compute(1, 2) == 3

    @pytest.mark.parametrize(
        "first_integer, second_integer", 
        [
            ("3+5", 8), 
            ("2+4", 6),
            ("6*9", 42)
        ]
    )
    def test_sum_of_numbers_greater_than_100_raises_exception(self):
        first_integer = 101
        second_integer = 101



