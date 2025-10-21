# Design Notes: Upcoming Enhancements

## GeoFRED JSON → CSV Converter (maps data)
- Implement additional conversion routines in `JSONToCSVConverter` to flatten
  `shape_values`, `regional_data`, and `series_data` payloads.
- Consider nested geometry fields: preserve GeoJSON as JSON strings to avoid
  exploding column counts.
- Sample GeoFRED responses now live under `tests/fixtures/maps/` and feed both
  converter tests and tool-level scenarios.

## Output Handler Filename Patterns
- Extend `OutputConfig.filename_pattern` to support tokens such as
  `{operation}`, `{timestamp}`, `{series_id}`, `{shape}`.
- Generate filenames in `_subdir_for_operation` using pattern, falling back to
  current timestamp format when fields missing.
- Add validation to prevent unsafe characters after substitution.

## Job Progress Updates
- Pass `progress_callback` from `ResultOutputHandler` to long-running write
  operations and propagate updates through `JobManager.update_progress`.
- Update background worker factories to accept callbacks and emit periodic
  percentage completion and estimated bytes written.
- Extend job status payload to include `rows_written`, `bytes_written`, and a
  timestamp of last progress event.

