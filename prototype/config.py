"""
Centralized configuration. Nothing else in this codebase should read
os.environ directly - import from here instead. This is the one place
to look when moving from prototype to a real environment later.
"""

import os

from dotenv import load_dotenv

load_dotenv()

CLICKHOUSE_URL = os.environ.get("CLICKHOUSE_URL", "https://ch.need.cat/")
CLICKHOUSE_USER = os.environ.get("CLICKHOUSE_USER", "admin")
CLICKHOUSE_PASSWORD = os.environ.get("CLICKHOUSE_PASSWORD", "nine")
CLICKHOUSE_DATABASE = os.environ.get("CLICKHOUSE_DATABASE", "soc_agent_db")
CLICKHOUSE_TABLE = os.environ.get("CLICKHOUSE_TABLE", "security_events")

ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4.5")
ANTHROPIC_MAX_TOKENS = int(os.environ.get("ANTHROPIC_MAX_TOKENS", 500))

REPORT_OUTPUT_PATH = os.environ.get("REPORT_OUTPUT_PATH", "report.md")
ISOLATED_EVENTS_SAMPLE_SIZE = int(os.environ.get("ISOLATED_EVENTS_SAMPLE_SIZE", 20))
