# BlobGuard MCP Tool Usage Rules

**Purpose:**
These rules are designed for use in AI-assisted coding editors (such as Cursor or Windsurf). They provide best practices and examples for using BlobGuard tools efficiently, ensuring maintainable, high-quality code by leveraging built-in utilities for blob storage, retrieval, and diffing.

---

## 1. Prefer BlobGuard Tools for Text Operations
- Always use the provided BlobGuard tools for saving, retrieving, and diffing blobs of text instead of custom file or string manipulation code.
- BlobGuard tools are optimized for consistency and traceability.

*Example:*
```python
# Instead of manual file I/O:
with open('data.txt', 'w') as f:
    f.write(data)
# Use:
save_blob('data.txt', data)
```

## 2. Saving and Updating Blobs
- Use `save_blob` to store or update a blob with a given name and optional metadata.
- Use the `force` flag to overwrite existing blobs if necessary.
- Always provide meaningful names and metadata for traceability.

*Example:*
```python
# Save a blob with metadata:
save_blob('config.json', config_json, metadata={'env': 'prod'}, force=True)
```

## 3. Retrieving Blobs
- Use `get_blob` to fetch a blob and its metadata by name.

*Example:*
```python
# Retrieve a blob:
result = get_blob('config.json')
content = result['content']
meta = result['metadata']
```

## 4. Diffing Blobs
- Use `diff` to compare two blobs by name and obtain a unified diff.
- Prefer diffing blobs for change tracking, reviews, or debugging instead of manual string comparison.

*Example:*
```python
# Get a diff between two versions:
diff = diff('config_v1.json', 'config_v2.json')
```

## 5. Metadata Management
- Use the `metadata` parameter to store relevant context (e.g., version, author, timestamp).
- Retrieve and inspect metadata to inform decisions or automate workflows.

*Example:*
```python
# Save with metadata:
save_blob('report.csv', report_data, metadata={'author': 'alice', 'date': '2024-06-01'})
# Access metadata:
result = get_blob('report.csv')
meta = result['metadata']
print(meta['author'])
```

## 6. Error Handling and Existence Checks
- Handle errors gracefully if a blob does not exist or a save would overwrite an existing blob without `force=True`.
- Always check return values and error messages from BlobGuard tools.

*Example:*
```python
try:
    result = get_blob('missing.txt')
    content = result['content']  # This will raise if 'error' in result
except KeyError:
    # Handle missing blob
    ...
```

## 7. Naming Conventions
- Use clear, descriptive, and unique names for blobs to avoid collisions and improve discoverability.
- Include versioning or environment information in blob names when appropriate.

*Example:*
```python
# Good:
save_blob('user_data_v2.json', data)
# Bad:
save_blob('data', data)
```

## 8. Batch Operations and Automation
- Use BlobGuard tools in scripts or workflows for batch processing, backups, or automated audits.
- Prefer programmatic use of BlobGuard over manual file management for repeatability and traceability.

## 9. Documentation and Rationale
- Document each tool call with a brief explanation of its purpose and expected outcome.
- Use comments to clarify why a blob is being saved, retrieved, or diffed.

*Example:*
```python
# Save daily backup for audit trail
save_blob('backup_2024-06-01.tar.gz', backup_data, metadata={'type': 'daily'})
```

## 10. Efficiency and Best Practices
- Avoid redundant saves or retrievals by caching results where appropriate.
- Use metadata to filter or select relevant blobs for processing.
- Regularly review and clean up unused blobs to maintain storage hygiene.

---

**Summary:**
Use BlobGuard tools for all blob-related operations in your codebase. Leverage metadata, diffing, and error handling features for robust, maintainable, and auditable workflows. Document your usage and follow naming conventions for clarity and traceability.
