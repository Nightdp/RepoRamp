from webapp.main import health


def test_health() -> None:
    assert health() == {"status": "ok"}
