# BlobGuard MCP

BlobGuard MCP is a lightweight, session-isolated blob storage and diff server designed for LLM coding agents making large or frequent code edits. It helps offload text processing overhead, avoid hallucinations, and maintain fidelity of in-progress work.

## Purpose

BlobGuard MCP provides a multi-tenant, in-memory blob storage and diffing service, purpose-built for LLM coding agents. By handling blob storage and diffing outside the agent, it enables efficient, accurate management of large or numerous code changes, reducing hallucination risk and preserving the integrity of ongoing work.

## Multi-Session Support

This server is designed to be multi-tenant. It automatically creates a unique, isolated workspace for every client connection.

All blobs are automatically namespaced based on the connection. This means that multiple users or applications can interact with the server simultaneously without their data interfering with one another, ensuring a secure and predictable experience without any required client-side configuration.

## Installation

To get started with BlobGuard MCP, follow these installation instructions.

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Voidious/blobguard-mcp.git
    cd blobguard-mcp
    ```

2.  **Create and Activate a Virtual Environment**:

    For macOS/Linux:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

    For Windows:
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    Install the required Python packages using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

BlobGuard MCP is designed to be used as a server with an MCP-compatible client, such as an AI coding assistant in an editor like Cursor or VS Code.

To configure the server, find the "MCP Tools" or "MCP Servers" settings in your editor's configuration. Then, add a new server configuration block like this:

**For macOS/Linux/Windows (Git Bash/WSL/Cygwin):**
```json
"blobguard": {
  "command": "/path/to/your/clone/of/blobguard-mcp/run.sh"
}
```

**For Windows (Command Prompt or PowerShell):**
```json
"blobguard": {
  "command": "C:\\path\\to\\your\\clone\\of\\blobguard-mcp\\run.bat"
}
```

Make sure to replace the path with the actual location of the script in your cloned repository. The script will automatically activate the virtual environment and run the server.

**Note:** Use `run.sh` for Unix-like shells (macOS, Linux, Git Bash, WSL, Cygwin) and `run.bat` for native Windows Command Prompt or PowerShell.

Once configured, your AI coding assistant will be able to use the BlobGuard MCP tools.

### Usage Rules for AI-Assisted Coding Editors

For best results with BlobGuard MCP, load the file [blobguard-rules.md](./blobguard-rules.md) into your AI-assisted coding editor (such as Cursor or Windsurf) as rules. This enables your coding assistant to follow best practices and use BlobGuard MCP efficiently and effectively. You may also read the file if you wish, but its main purpose is to serve as a ruleset for your coding assistant.

## Available Tools

### save_blob
Save a blob with a given name and optional metadata.

**Parameters:**
- `name` (str): The unique name for the blob.
- `content` (str): The content to store in the blob.
- `metadata` (dict, optional): Optional metadata to associate with the blob.
- `force` (bool, optional): If True, overwrite any existing blob with the same name. Default is False.

**Returns:**
- `dict`: `{ "success": True }` if saved, or `{ "error": ... }` if the blob exists and force is not set.

**Example:**
```python
save_blob(name="foo", content="hello world", metadata={"author": "alice"})
```

### get_blob
Retrieve a blob and its metadata by name.

**Parameters:**
- `name` (str): The name of the blob to retrieve.

**Returns:**
- `dict`: `{ "content": content, "metadata": metadata }` if found, or `{ "error": ... }` if not found.

**Example:**
```python
get_blob(name="foo")
```

### diff
Return a unified diff between two blobs by name, similar to the output of the diff command.

**Parameters:**
- `name1` (str): The name of the first blob.
- `name2` (str): The name of the second blob.

**Returns:**
- `dict`: `{ "diff": unified_diff_string }` if both blobs exist, or `{ "error": ... }`