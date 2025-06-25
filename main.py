from fastmcp import FastMCP, Context
from typing import Any, Dict, Optional
from dataclasses import dataclass

# --- Data Structures ---


@dataclass
class Blob:
    content: str
    metadata: Optional[dict] = None


class ServerState:
    """A class to hold the server's in-memory state."""

    def __init__(self):
        # Each blob is stored as a Blob dataclass
        self.blobs: Dict[str, Blob] = {}

    def reset(self):
        self.blobs.clear()


class BlobGuardMCP(FastMCP):
    """A custom FastMCP subclass that will hold all session states."""

    sessions: Dict[str, ServerState]


# --- MCP Server Setup ---

mcp = BlobGuardMCP("BlobGuard MCP")
mcp.sessions = {}  # type: ignore

# --- Session Management ---


def get_session_state(ctx: Context) -> ServerState:
    """
    Gets or creates the state for the current session, ensuring data isolation.
    It automatically uses a unique identifier from the underlying connection
    session. If no identifier can be found (e.g., in tests), it falls back
    to a default shared session.
    """
    mcp_instance: BlobGuardMCP = ctx.fastmcp  # type: ignore

    session_key = None
    # Use the unique ID of the transport session object for automatic isolation.
    session_obj = getattr(ctx, "session", None)
    if session_obj and hasattr(session_obj, "id"):
        session_key = session_obj.id

    # As a failsafe for test environments or non-compliant clients, use a default key.
    if not session_key:
        session_key = "default_session"

    if session_key not in mcp_instance.sessions:
        mcp_instance.sessions[session_key] = ServerState()

    return mcp_instance.sessions[session_key]


# --- Tools ---


def _reset_state(ctx: Context) -> str:
    """Resets the in-memory storage. For testing purposes only."""
    state = get_session_state(ctx)
    state.reset()
    return "State has been reset."


@mcp.tool()
def save_blob(
    ctx: Context,
    name: str,
    content: str,
    metadata: Optional[dict] = None,
    force: bool = False,
) -> Dict[str, Any]:
    """
    Save a blob with a given name and optional metadata.

    Parameters:
        name (str): The unique name for the blob.
        content (str): The content to store in the blob.
        metadata (dict, optional): Optional metadata to associate with the blob.
        force (bool, optional): If True, overwrite any existing blob with the same
            name. Default is False.

    Returns:
        dict: {"success": True} if saved, or {"error": ...} if the blob exists and force
        is not set.

    Example:
        save_blob(name="foo", content="hello world", metadata={"author": "alice"})
    """
    state = get_session_state(ctx)
    if not force and name in state.blobs:
        return {"error": f"Blob '{name}' already exists. Use force=True to overwrite."}
    state.blobs[name] = Blob(
        content=str(content), metadata=metadata if metadata is not None else None
    )
    return {"success": True}


@mcp.tool()
def get_blob(ctx: Context, name: str) -> dict:
    """
    Retrieve a blob and its metadata by name.

    Parameters:
        name (str): The name of the blob to retrieve.

    Returns:
        dict: {"content": content, "metadata": metadata} if found, or {"error": ...} if
            not found.

    Example:
        get_blob(name="foo")
    """
    state = get_session_state(ctx)
    if name not in state.blobs:
        return {"error": f"Blob '{name}' not found."}
    entry = state.blobs[name]
    return {"content": entry.content, "metadata": entry.metadata}


@mcp.tool()
def diff(ctx: Context, name1: str, name2: str) -> dict:
    """
    Return a unified diff between two blobs by name, similar to the output of the diff
    command.

    Parameters:
        name1 (str): The name of the first blob.
        name2 (str): The name of the second blob.

    Returns:
        dict: {"diff": unified_diff_string} if both blobs exist, or {"error": ...} if
            either is missing.

    Example:
        diff(name1="foo", name2="bar")
    """
    import difflib

    state = get_session_state(ctx)
    if name1 not in state.blobs:
        return {"error": f"Blob '{name1}' not found."}
    if name2 not in state.blobs:
        return {"error": f"Blob '{name2}' not found."}
    blob1 = state.blobs[name1].content.splitlines(keepends=True)
    blob2 = state.blobs[name2].content.splitlines(keepends=True)
    diff_lines = list(difflib.unified_diff(blob1, blob2, fromfile=name1, tofile=name2))
    return {"diff": "".join(diff_lines)}


if __name__ == "__main__":
    mcp.run()
