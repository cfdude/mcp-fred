from mcp_fred.transports import (
    OPTIONAL_TOOL_NAMES,
    TOOL_HANDLERS,
    TOOL_REGISTRY,
    ToolSpec,
    build_tool_registry,
)


def test_tool_registry_includes_job_tools() -> None:
    assert "fred_job_list" in TOOL_REGISTRY
    assert "fred_job_cancel" in TOOL_REGISTRY
    for name in ("fred_job_list", "fred_job_cancel"):
        spec = TOOL_REGISTRY[name]
        assert isinstance(spec, ToolSpec)
        assert callable(spec.handler)
        assert TOOL_HANDLERS[name] is spec.handler


def test_optional_tools_can_be_excluded() -> None:
    registry = build_tool_registry(include_optional=False)
    assert "fred_job_status" in registry
    for name in OPTIONAL_TOOL_NAMES:
        assert name not in registry
