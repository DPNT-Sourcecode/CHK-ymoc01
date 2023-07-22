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
            (100, 100),
            (1000, 1), 
            (1, 1000),
            (1000, 1000)
        ]
    )
    def test_sum_of_numbers_100_or_greater_raises_exception(self, first_integer, second_integer):
        with pytest.raises(ValueError) as exception:
            sum_solution.compute(first_integer, second_integer)

        assert str(exception.value) == "Inputs must be less than 100"

    @pytest.mark.parametrize(
        "first_integer, second_integer", 
        [
            (0, 99), 
            (99, 0),
            (0, 0),
            (-100, 99), 
            (99, -100),
            (-100, -100)
        ]
    )
    def test_sum_of_numbers_0_or_less_raises_exception(self, first_integer, second_integer):
        with pytest.raises(ValueError) as exception:
            sum_solution.compute(first_integer, second_integer)

        assert str(exception.value) == "Inputs must be greater than 0"

    @pytest.mark.parametrize(
        "first_argument, second_argument", 
        [
            ("9", 1), 
            (2, "14"),
            ("9", "1"),
            ([19], [5, 5])
        ]
    )
    def test_sum_with_invalid_types_raises_exception(self, first_argument, second_argument):
        with pytest.raises(TypeError) as exception:
            sum_solution.compute(first_argument, second_argument)
        
        assert str(exception.value) == "Inputs must be integers"