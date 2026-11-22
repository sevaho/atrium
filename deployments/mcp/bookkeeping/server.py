"""Purpose-built bookkeeping tools on top of the boekhouding spreadsheet and the invoices folder.

The agent never gets raw Sheets/Drive access: it can only read, list invoices and
append rows into the transactions tab, never edit or delete existing rows.
"""

import io
import json
import os
from datetime import date

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from mcp.server.fastmcp import FastMCP
from pypdf import PdfReader

SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
INVOICES_FOLDER_ID = os.environ["INVOICES_FOLDER_ID"]
credentials = service_account.Credentials.from_service_account_info(
    json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]),
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.readonly"],
)
sheets = build("sheets", "v4", credentials=credentials).spreadsheets()
drive = build("drive", "v3", credentials=credentials)

mcp = FastMCP("bookkeeping", host="0.0.0.0", port=8000)

# Columns B..M of the transactions tab. MONTH (D) and TYPE (I) are formulas in the
# template, so add_transaction never writes them.
COLUMNS = ["date_paid", "invoice_date", "month", "settled", "account", "value", "category", "type", "accounted", "supplier", "description", "invoice"]


@mcp.tool()
def get_definitions() -> dict:
    """Allowed accounts, categories (name -> income/expense) and known suppliers."""
    rows = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="definitions!B1:H200").execute().get("values", [])
    header = next(i for i, row in enumerate(rows) if row and row[0] == "Accounts")
    rows = [row + [""] * (7 - len(row)) for row in rows[header + 1 :]]
    return {
        "accounts": [row[0] for row in rows if row[0]],
        "categories": {row[2]: row[3] for row in rows if row[2]},
        "suppliers": [row[6] for row in rows if row[6]],
    }


@mcp.tool()
def list_transactions() -> list[dict]:
    """All booked transactions, with their sheet row number. The invoice field holds the Drive file id."""
    rows = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="transactions!B1:M1000", valueRenderOption="FORMULA").execute().get("values", [])
    header = next(i for i, row in enumerate(rows) if row and row[0] == "DATE PAID")
    return [
        {"row": header + 2 + i, **dict(zip(COLUMNS, row))}
        for i, row in enumerate(rows[header + 1 :])
        if row and row[0] != ""
    ]


@mcp.tool()
def list_invoices() -> list[dict]:
    """Invoice files anywhere under the invoices folder (e.g. IN/2026/11), with their folder path,
    flagged booked when a transaction already links to them."""
    files, folders = [], [(INVOICES_FOLDER_ID, "")]
    while folders:
        folder_id, path = folders.pop()
        children = drive.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="files(id, name, mimeType, createdTime, webViewLink)",
            pageSize=1000,
        ).execute()["files"]
        for child in children:
            if child["mimeType"] == "application/vnd.google-apps.folder":
                folders.append((child["id"], f"{path}{child['name']}/"))
            else:
                files.append({**child, "path": path})
    linked = json.dumps([t.get("invoice", "") for t in list_transactions()])
    return [{**f, "booked": f["id"] in linked} for f in sorted(files, key=lambda f: f["createdTime"], reverse=True)]


@mcp.tool()
def read_invoice(file_id: str) -> str:
    """Text of an invoice PDF from the invoices folder. Empty text means a scanned PDF: ask the user for the details."""
    invoice = next((f for f in list_invoices() if f["id"] == file_id), None)
    if invoice is None:
        raise ValueError("file is not in the invoices folder")
    if invoice["mimeType"] != "application/pdf":
        raise ValueError(f"only PDFs can be read, this is {invoice['mimeType']}")
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, drive.files().get_media(fileId=file_id))
    while not downloader.next_chunk()[1]:
        pass
    return "\n".join(page.extract_text() or "" for page in PdfReader(buffer).pages)[:8000]


@mcp.tool()
def add_transaction(
    date_paid: str,
    account: str,
    amount: float,
    category: str,
    supplier: str = "",
    description: str = "",
    invoice_date: str = "",
    invoice_file_id: str = "",
    settled: bool = True,
) -> dict:
    """Append one transaction in the first empty row. Dates are YYYY-MM-DD, amount is positive:
    the sign follows the category type. Not accounted yet, that happens at the accountant."""
    definitions = get_definitions()
    if account not in definitions["accounts"]:
        raise ValueError(f"unknown account {account!r}, allowed: {definitions['accounts']}")
    if category not in definitions["categories"]:
        raise ValueError(f"unknown category {category!r}, allowed: {list(definitions['categories'])}")
    if amount <= 0:
        raise ValueError("amount must be positive, the category decides income or expense")
    date.fromisoformat(date_paid)
    if invoice_date:
        date.fromisoformat(invoice_date)

    invoice = ""
    if invoice_file_id:
        f = next((f for f in list_invoices() if f["id"] == invoice_file_id), None)
        if f is None:
            raise ValueError("invoice is not in the invoices folder")
        if f["booked"]:
            raise ValueError("this invoice is already booked")
        invoice = f'=HYPERLINK("{f["webViewLink"]}", "{f["name"].replace(chr(34), "")}")'

    rows = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="transactions!B1:B1000").execute().get("values", [])
    header = next(i for i, row in enumerate(rows) if row and row[0] == "DATE PAID")
    empty = next((i for i in range(header + 1, len(rows)) if not rows[i] or rows[i][0] == ""), len(rows))
    row = empty + 1

    value = -amount if definitions["categories"][category] == "expense" else amount
    sheets.values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"transactions!B{row}:C{row}", "values": [[date_paid, invoice_date]]},
                {"range": f"transactions!E{row}:H{row}", "values": [[settled, account, value, category]]},
                {"range": f"transactions!J{row}:M{row}", "values": [[False, supplier, description, invoice]]},
            ],
        },
    ).execute()
    return {"row": row, "value": value}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
