Create a JSON response with exactly these top-level fields:

- case_summary
- legal_issues
- legal_basis
- practical_references
- recommendations
- limitations

The legal_basis array must only contain law retrieved from the legal retrieval tool.
The practical_references array must only contain web examples or related practical references.
Recommendations must be options, not commands, and should be ordered from low-intensity to high-intensity actions.
Always include a limitations field explaining that the system is only decision support.
