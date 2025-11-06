import os
from pathlib import Path

import pytest

from mcp_fred.utils.path_resolver import PathResolver, PathSecurityError


def test_path_resolver_creates_directories(tmp_path: Path) -> None:
    resolver = PathResolver(str(tmp_path / "storage"))
    resolved = resolver.resolve("my-project", "data.csv", subdir="series")
    assert resolved.parent.exists()
    assert resolved.name == "data.csv"


def test_path_resolver_invalid_component(tmp_path: Path) -> None:
    resolver = PathResolver(str(tmp_path))
    with pytest.raises(PathSecurityError):
        resolver.resolve("", "file.csv")


def test_path_resolver_permissions(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    storage = tmp_path / "root"
    storage.mkdir()
    resolver = PathResolver(str(storage))

    def fake_access(path: str, mode: int) -> bool:
        return False

    monkeypatch.setattr(os, "access", fake_access)

    with pytest.raises(PathSecurityError):
        resolver.resolve("proj", "file.csv")
