from mcp_fred.utils.token_estimator import TokenEstimator


def test_token_estimator_should_save_to_file() -> None:
    estimator = TokenEstimator(default_safe_limit=100)
    records = [{"a": "x" * 10} for _ in range(50)]
    tokens = estimator.estimate_records(records)
    assert tokens > 0
    assert estimator.should_save_to_file(tokens, model_limit=120)


def test_token_estimator_screen_safe() -> None:
    estimator = TokenEstimator(default_safe_limit=10_000)
    records = [{"value": i} for i in range(5)]
    tokens = estimator.estimate_records(records)
    assert not estimator.should_save_to_file(tokens, model_limit=20_000)


def test_token_estimator_handles_nested_geojson() -> None:
    estimator = TokenEstimator(default_safe_limit=5_000)
    records = [
        {
            "id": "01",
            "name": "Alabama",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0.0, 0.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]]],
            },
        }
    ]
    tokens = estimator.estimate_records(records)
    assert tokens > 0
    assert not estimator.should_save_to_file(tokens, model_limit=10_000)
