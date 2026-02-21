from lava_speed.client import LavaSpeedClient


def test_client_defaults() -> None:
    client = LavaSpeedClient(base_url="https://example.com")

    assert client.base_url == "https://example.com"
    assert client.timeout_seconds == 10
