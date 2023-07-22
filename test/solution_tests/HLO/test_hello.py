import pytest
from solutions.HLO import hello_solution

@pytest.mark.parametrize(
    "friend_name", 
    [
        "John",
        "Phil",
        "Phil W"
    ]
)
def test_hello_returns_hello_world_message(friend_name):
    assert hello_solution.hello(friend_name) == f"Hello, {friend_name}!"