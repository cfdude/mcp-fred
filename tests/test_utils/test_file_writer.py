from pathlib import Path

from mcp_fred.utils.file_writer import FileWriter


def test_file_writer_chunked_csv(tmp_path: Path) -> None:
    writer = FileWriter()
    path = tmp_path / "out.csv"
    fieldnames = ["id", "value"]
    rows = [{"id": str(i), "value": str(i * 2)} for i in range(5)]

    progress: list[tuple[int, int]] = []
    writer.write_csv(
        path,
        fieldnames,
        rows,
        chunk_size=2,
        progress_callback=lambda total_rows, total_bytes: progress.append(
            (total_rows, total_bytes)
        ),
    )

    content = path.read_text(encoding="utf-8").strip().splitlines()
    assert content[0] == "id,value"
    assert len(content) == 6
    assert progress[-1][0] == len(rows)
    assert progress[-1][1] >= len("id,value\n")


def test_file_writer_json(tmp_path: Path) -> None:
    writer = FileWriter()
    path = tmp_path / "data.json"
    payload = {"series": [1, 2, 3]}

    writer.write_json(path, payload)

    content = path.read_text(encoding="utf-8")
    assert "series" in content
