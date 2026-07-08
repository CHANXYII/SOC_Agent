"""
Centralized configuration. Nothing else in this codebase should read
os.environ directly - import from here instead. This is the one place
to look when moving from prototype to a real environment later.
"""

import os

from dotenv import load_dotenv

load_dotenv()

CLICKHOUSE_URL = os.environ.get("CLICKHOUSE_URL", "https://ch.need.cat/")
CLICKHOUSE_USER = os.environ.get("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = os.environ.get("CLICKHOUSE_PASSWORD")
CLICKHOUSE_DATABASE = os.environ.get("CLICKHOUSE_DATABASE", "default")
CLICKHOUSE_TABLE = "security_events"

SAMPLE_DATA_CSV_PATH = os.environ.get("SAMPLE_DATA_CSV_PATH", "data/sample_data.csv")

ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
ANTHROPIC_MAX_TOKENS = 500

REPORT_OUTPUT_PATH = "report.md"
ISOLATED_EVENTS_SAMPLE_SIZE = 20
