from myproject.main import get_message


def test_get_message() -> None:
    assert get_message() == "Hello from myproject CLI"
