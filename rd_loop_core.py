#!/usr/bin/env python3
"""
M3loop — R&D Loop Engine
Reads Queue from Sheet, manages state, outputs iteration results.
Sheet: https://docs.google.com/spreadsheets/d/1TS4pQ5RsFD6aVuHcgPb2enmuBPT8bdzflzVQZq9sbsw/edit
"""
import gspread
from google.oauth2 import service_account
import datetime, json, sys

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]
CREDS = service_account.Credentials.from_service_account_file(
    "service_account.json", scopes=SCOPES
)
SHEET_ID = "1TS4pQ5RsFD6aVuHcgPb2enmuBPT8bdzflzVQZq9sbsw"

def get_ws(name="Queue"):
    return gspread.authorize(CREDS).open_by_key(SHEET_ID).worksheet(name)

def get_all_records(ws):
    return ws.get_all_records()

def find_next_topic(rows):
    for i, row in enumerate(rows):
        t = str(row.get("QueueTopic", ""))
        if t.strip().startswith("[ ]"):
            return i, t.replace("[ ]", "").strip(), rows[i]
    return -1, "", None

def mark_in_progress(sheet_row):
    ws = get_ws()
    today = datetime.date.today().isoformat()
    ws.update(range_name=f"B{sheet_row}", values=[["IN_PROGRESS"]])
    ws.update(range_name=f"C{sheet_row}", values=[[today]])

def mark_complete(sheet_row, score, report_url="", failures=""):
    ws = get_ws()
    ws.update(range_name=f"B{sheet_row}", values=[["COMPLETE"]])
    ws.update(range_name=f"E{sheet_row}", values=[[score]])
    ws.update(range_name=f"F{sheet_row}", values=[[failures]])
    ws.update(range_name=f"G{sheet_row}", values=[[report_url]])

def mark_failed(sheet_row, iteration, failures):
    ws = get_ws()
    ws.update(range_name=f"B{sheet_row}", values=[["FAILED"]])
    ws.update(range_name=f"D{sheet_row}", values=[[iteration]])
    ws.update(range_name=f"F{sheet_row}", values=[[failures]])

def append_state(topic, result, score, failures):
    ws = get_ws("State")
    today = datetime.date.today().isoformat()
    ws.append_row([today, topic, result, score, failures])

def run():
    ws = get_ws()
    rows = get_all_records(ws)
    idx, topic, _ = find_next_topic(rows)
    if idx < 0:
        print("Queue empty.")
        return
    sheet_row = idx + 2
    print(f"TOPIC: {topic} | Row: {sheet_row}")
    mark_in_progress(sheet_row)
    print("Status: IN_PROGRESS — waiting for Generator + Verifier in Mavis")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run()
