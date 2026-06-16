#!/usr/bin/env python3
"""
M3loop — Sheet 一次性初始化脚本
"""
import gspread
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]
CREDS = service_account.Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
SHEET_ID = "1TS4pQ5RsFD6aVuHcgPb2enmuBPT8bdzflzVQZq9sbsw"

def setup():
    gc = gspread.authorize(CREDS)
    ss = gc.open_by_key(SHEET_ID)

    # --- Queue tab ---
    ws1 = ss.sheet1
    ws1.update_title("Queue")
    ws1.update("A1", [["QueueTopic","Status","UpdatedAt","Iteration","Score","Failures","ReportLink"]],
               value_input_option="RAW")
    ws1.update("A2", [["[ ] 第一个调研主题","READY","","1","","",""]], value_input_option="RAW")
    print("✅ Queue tab ready")

    # --- State tab ---
    try:
        ws2 = ss.add_worksheet("State", rows=100, cols=6)
    except Exception:
        ws2 = ss.worksheet("State")
    ws2.update("A1", [["Date","Topic","Result","Score","Failures","Note"]],
               value_input_option="RAW")
    print("✅ State tab ready")

    # --- Rubric tab ---
    try:
        ws3 = ss.add_worksheet("Rubric", rows=20, cols=3)
    except Exception:
        ws3 = ss.worksheet("Rubric")
    ws3.update("A1", [["Item","Weight","Description"]], value_input_option="RAW")
    rubric = [
        ["Factual accuracy", "30%", "All claims backed by sources"],
        ["Scope completeness", "25%", "Covers all required dimensions"],
        ["Actionable output", "25%", "Conclusion has clear next steps"],
        ["Structure & clarity", "20%", "Readable, well-organized"],
    ]
    for i, row in enumerate(rubric, start=2):
        ws3.update(f"A{i}", [row], value_input_option="RAW")
    print("✅ Rubric tab ready")
    print("\n🎉 M3loop setup complete!")

if __name__ == "__main__":
    setup()
