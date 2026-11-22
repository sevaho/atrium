"""Local stdio MCP server in the agent pod: OCR files sent over Telegram with Mistral OCR."""

import base64
import json
import mimetypes
import os
import urllib.request
from pathlib import Path

from mcp.server.mcpserver import MCPServer

# Only Telegram uploads, never .env or config.yaml next to them.
ALLOWED = [Path("/opt/data/cache/images"), Path("/opt/data/cache/documents")]

server = MCPServer("ocr")


@server.tool()
def ocr_file(path: str) -> str:
    """Text of an image or PDF the user sent over Telegram, as markdown, read with Mistral OCR."""
    file = Path(path).resolve()
    if not any(file.is_relative_to(allowed) for allowed in ALLOWED):
        raise ValueError(f"only files under {', '.join(map(str, ALLOWED))} can be read")
    mime = mimetypes.guess_type(file.name)[0] or ""
    if mime != "application/pdf" and not mime.startswith("image/"):
        raise ValueError(f"only PDFs and images can be read, this is {mime or 'unknown'}")
    data_url = f"data:{mime};base64,{base64.b64encode(file.read_bytes()).decode()}"
    kind = "image_url" if mime.startswith("image/") else "document_url"
    request = urllib.request.Request(
        f"{os.environ['LITELLM_URL']}/ocr",
        data=json.dumps({"model": "mistral-ocr", "document": {"type": kind, kind: data_url}}).encode(),
        headers={"Authorization": f"Bearer {os.environ['LITELLM_API_KEY']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        pages = json.load(response)["pages"]
    return "\n\n".join(page["markdown"] for page in pages)[:12000]


if __name__ == "__main__":
    server.run()
