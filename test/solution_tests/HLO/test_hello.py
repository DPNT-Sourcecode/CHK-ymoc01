from solutions.HLO import hello_solution

def test_hello_returns_hello_world_message():
    friend_name = "any string"
    assert hello_solution(friend_name) == "hello to the world"