# TODO - MCP-FRED Development Tasks

**Last Updated:** 2025-11-03

## Quick Links
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [API_MAPPING.md](API_MAPPING.md) - FRED API → Tool mapping
- [CHANGELOG.md](../CHANGELOG.md) - Version history

---

## Current Sprint: Testing & Stability

### High Priority

- [ ] Add tests for STDIO transport (currently 0% coverage - 58 statements untested)
- [ ] Test MCP server integration with Claude Desktop
- [ ] Verify all job management tools work with large datasets
- [ ] Test async job processing with 100K+ observation datasets
- [ ] Add integration tests for complete FRED API workflows

### Medium Priority

- [ ] Simplify API client retry logic (reduce from enterprise complexity to basic 3-retry)
- [ ] Add filename pattern generation with variables in output handler
- [ ] Calibrate rate-limit parameters based on real FRED API usage
- [ ] Add worker pool for concurrent job processing
- [ ] Implement size estimation before executing requests

### Low Priority / Future Enhancements

- [ ] Add response caching for frequently requested data
- [ ] Add connection pooling for API client
- [ ] Implement streaming for very large datasets
- [ ] Add structured logging for debugging
- [ ] Add health check endpoint for monitoring

---

## Documentation Tasks

- [ ] Simplify ARCHITECTURE.md (remove excessive detail)
- [ ] Update README.md with installation and usage examples
- [ ] Add troubleshooting section to README
- [ ] Ensure all tool descriptions are accurate in API_MAPPING.md
- [ ] Add link to official FRED API docs instead of duplicating them

---

## Quality & Polish

- [ ] Run Ruff linting on entire codebase
- [ ] Fix any remaining linting warnings
- [ ] Ensure all functions have type hints
- [ ] Achieve 85%+ test coverage (currently 82.4%)
- [ ] Add docstrings to all public functions

---

## Deployment Preparation

- [ ] Create setup.py or finalize pyproject.toml
- [ ] Test package installation in clean environment
- [ ] Update CHANGELOG.md with all changes
- [ ] Tag release version
- [ ] Test with Claude Desktop before release

---

## Notes

- **Testing First**: Focus on testing STDIO transport and end-to-end workflows
- **Simplicity**: Remove complexity where possible (config, retry logic)
- **Real Usage**: Test with actual large FRED datasets before considering "done"
