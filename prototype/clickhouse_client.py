"""
All Clickhouse data access lives here. If the data source ever changes
(different DB, different schema, live SIEM feed instead of a table), 
this is the only file that should need to change.
"""

import csv
import json
import requests

import prototype.config as config


CSV_COLUMNS = [
    "event_id", "event_time", "source_ip", "dest_ip", "user_name",
    "log_source", "event_type", "severity", "mitre_technique",
    "raw_log", "is_malicious", "campaign_id",
]


def query(sql: str):
    """Run a SQL query against the Clickhouse database and return the results as a list of dicts."""
    response = requests.post(
        config.CLICKHOUSE_URL,
        params={"database": config.CLICKHOUSE_DATABASE, "default_format": "JSONEachRow"},
        data=sql,
        auth=(config.CLICKHOUSE_USER, config.CLICKHOUSE_PASSWORD),
        timeout=30
    )
    if not response.ok:
        raise RuntimeError(f"Clickhouse query failed ({response.status_code}): {response.text}")
    lines = [line for line in response.text.splitlines() if line.strip()]
    return [json.loads(line) for line in lines]


def fetch_malicious_events():
    """Pull all malicious-flagged events, ordered by campaign then time."""
    sql = f"""
        SELECT *
        FROM {config.CLICKHOUSE_TABLE}
        WHERE is_malicious = 1
        ORDER BY campaign_id, event_time
        FORMAT JSONEachRow
    """
    return query(sql)


def fetch_malicious_events_from_csv(path: str = None):
    """Fallback for when Clickhouse is unreachable: read the same events from the local sample CSV."""
    path = path or config.SAMPLE_DATA_CSV_PATH
    with open(path, newline="", encoding="utf-8") as f:
        rows = [dict(zip(CSV_COLUMNS, row)) for row in csv.reader(f)]

    for row in rows:
        row["event_id"] = int(row["event_id"])
        row["is_malicious"] = int(row["is_malicious"])

    malicious = [row for row in rows if row["is_malicious"] == 1]
    malicious.sort(key=lambda row: (row["campaign_id"], row["event_time"]))
    
    return malicious
