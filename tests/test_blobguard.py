import importlib
import main
import pytest  # type: ignore
from fastmcp import Client
from main import BlobGuardMCP
import json


@pytest.fixture
async def client():
    """
    Provides an isolated FastMCP client for each test by reloading the main
    module and explicitly resetting the application state for the session.
    """
    importlib.reload(main)
    mcp_instance: BlobGuardMCP = main.mcp
    # Register the reset tool dynamically for testing only.
    mcp_instance.tool()(main._reset_state)
    async with Client(mcp_instance) as c:
        # We call the session-aware reset tool to ensure a clean slate.
        # The main.py logic will handle the test environment's lack of a real client_id.
        await c.call_tool("_reset_state")
        yield c


@pytest.mark.asyncio
async def test_save_and_get_blob(client):
    # Save a blob
    result = json.loads(
        (
            await client.call_tool(
                "save_blob",
                {"name": "foo", "content": "hello world", "metadata": {"type": "text"}},
            )
        )[0].text
    )
    assert result == {"success": True}

    # Get the blob
    result = json.loads((await client.call_tool("get_blob", {"name": "foo"}))[0].text)
    assert result["content"] == "hello world"
    assert result["metadata"] == {"type": "text"}

    # Saving again without force should error
    result = json.loads(
        (await client.call_tool("save_blob", {"name": "foo", "content": "new text"}))[
            0
        ].text
    )
    assert "error" in result
    assert "already exists" in result["error"]

    # Saving with force should overwrite
    result = json.loads(
        (
            await client.call_tool(
                "save_blob", {"name": "foo", "content": "new text", "force": True}
            )
        )[0].text
    )
    assert result == {"success": True}
    result = json.loads((await client.call_tool("get_blob", {"name": "foo"}))[0].text)
    assert result["content"] == "new text"

    # Save a blob with no metadata
    result = json.loads(
        (await client.call_tool("save_blob", {"name": "bar", "content": "bar text"}))[
            0
        ].text
    )
    assert result == {"success": True}
    result = json.loads((await client.call_tool("get_blob", {"name": "bar"}))[0].text)
    assert result["content"] == "bar text"
    assert result["metadata"] is None

    # Getting a missing blob should error
    result = json.loads(
        (await client.call_tool("get_blob", {"name": "missing"}))[0].text
    )
    assert "error" in result
    assert "not found" in result["error"]


@pytest.mark.asyncio
async def test_diff_blobs(client):
    # Save two blobs
    await client.call_tool(
        "save_blob", {"name": "a", "content": "line1\nline2\nline3\n"}
    )
    await client.call_tool(
        "save_blob", {"name": "b", "content": "line1\nlineX\nline3\n"}
    )

    # Diff them
    result = json.loads(
        (await client.call_tool("diff", {"name1": "a", "name2": "b"}))[0].text
    )
    diff_text = result["diff"]
    assert diff_text.startswith("--- a\n++ b\n") or diff_text.startswith(
        "--- a\n+++ b\n"
    )
    assert "-line2\n" in diff_text
    assert "+lineX\n" in diff_text

    # Diff with missing blob
    result = json.loads(
        (await client.call_tool("diff", {"name1": "a", "name2": "missing"}))[0].text
    )
    assert "error" in result
    assert "not found" in result["error"]
    result = json.loads(
        (await client.call_tool("diff", {"name1": "missing", "name2": "a"}))[0].text
    )
    assert "error" in result
    assert "not found" in result["error"]

    # Diff identical blobs
    await client.call_tool("save_blob", {"name": "c", "content": "same\ntext\n"})
    await client.call_tool("save_blob", {"name": "d", "content": "same\ntext\n"})
    result = json.loads(
        (await client.call_tool("diff", {"name1": "c", "name2": "d"}))[0].text
    )
    # Unified diff for identical files is empty
    assert result["diff"] == ""
