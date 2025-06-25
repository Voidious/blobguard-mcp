# BlobGuard MCP

TODO

## Purpose

TODO

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
You can interact with the server using the following tools:

TODO

## Running Tests

This project includes a test suite to verify its functionality. The tests use `pytest` and run in-memory without needing to keep the server running in a separate process.

To run the tests, execute the following command from the root directory:

```
