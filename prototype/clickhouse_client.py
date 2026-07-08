"""
All Clickhouse data access lives here. If the data source ever changes
(different DB, different schema, live SIEM feed instead of a table), 
this is the only file that should need to change.
"""

import json
import requests

import prototype.config as config


def query(sql: str):
    """Run a SQL query against the Clickhouse database and return the results as a list of dicts."""

    response = requests.post(
        config.CLICKHOUSE_URL,
        params={"database": config.CLICKHOUSE_DATABASE, "default_format": "JSONEachRow"},
        data=sql,
        auth=(config.CLICKHOUSE_USER, config.CLICKHOUSE_PASSWORD),
        timeout=30
    )
    response.raise_for_status()
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
