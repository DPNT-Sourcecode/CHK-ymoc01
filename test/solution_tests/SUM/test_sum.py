import pytest
from solutions.SUM import sum_solution


class TestSum():
    def test_sum_of_valid_numbers_returns_sum(self):
        assert sum_solution.compute(1, 2) == 3

    @pytest.mark.parametrize(
        "first_integer, second_integer", 
        [
            (100, 1), 
            (1, 100),
            (100, 100)
        ]
    )
    def test_sum_of_numbers_greater_than_100_raises_exception(self, first_integer, second_integer):
        with pytest.raises(ValueError):
            sum_solution.compute(first_integer, second_integer)

    @pytest.mark.parametrize(
        "first_integer, second_integer", 
        [
            (0, 99), 
            (99, 0),
            (0, 0)
        ]
    )
    def test_sum_of_numbers_greater_than_100_raises_exception(self, first_integer, second_integer):
        with pytest.raises(ValueError):
            sum_solution.compute(first_integer, second_integer)


