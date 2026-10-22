import pytest

from utils import storage


@pytest.fixture(autouse=True)
def clean_state(tmp_path, monkeypatch):
    """Give every test an empty state and a temporary data file."""
    storage.clear_all()
    monkeypatch.setattr(storage, "DATA_FILE", str(tmp_path / "tracker.json"))
    yield
    storage.clear_all()
