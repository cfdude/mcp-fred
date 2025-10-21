import json
from pathlib import Path

from mcp_fred.utils.json_to_csv import JSONToCSVConverter

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "maps"


def test_converter_flattens_nested_maps() -> None:
    converter = JSONToCSVConverter()
    records = json.loads((FIXTURES_DIR / "shape_values.json").read_text(encoding="utf-8"))[
        "shape_values"
    ]
    csv_output = converter.to_csv(records)
    assert "properties_state_abbr" in csv_output
    assert "properties_region" in csv_output
    assert "geography_type" in csv_output
    assert "geography_coordinates" in csv_output
    assert "Polygon" in csv_output


def test_converter_handles_regional_data() -> None:
    converter = JSONToCSVConverter()
    records = json.loads((FIXTURES_DIR / "regional_data.json").read_text(encoding="utf-8"))[
        "regional_data"
    ]
    fieldnames, iterator = converter.prepare(records)
    assert "metadata_observation_date" in fieldnames
    rows = list(iterator)
    assert rows[0]["series_id"].startswith("LAUST")
    assert rows[0]["metadata_units"] == "Percent"
