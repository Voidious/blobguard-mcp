from fastmcp import FastMCP, Context
from typing import Dict

# --- Data Structures ---


class ServerState:
    """A class to hold the server's in-memory state."""

    def __init__(self):
        self.blobs: Dict[str, str] = {}

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


if __name__ == "__main__":
    mcp.run()
