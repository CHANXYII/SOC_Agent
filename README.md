# AI Agentic System for Security Operations Center

An AI agent system that investigates security events, forms hypotheses,
maps evidence to MITRE ATT&CK techniques, and produces review-ready
incident reports with confidence levels and recommended next steps.

## Status

**Current phase: Prototype (Phase 1 of 11)**

See [`docs/`](./docs) for the full project plan and timeline (July–November 2026).

## Repository layout

```
docs/         Full project plan and reference documents
data/         Sample/training security event data (ClickHouse SQL)
prototype/    Phase 1 runnable prototype code
```

## Quick start

1. Load the sample data into ClickHouse — see [`data/`](./data)
2. Set up and run the prototype — see [`prototype/README.md`](./prototype/README.md)

## Infrastructure

```
                 ┌─────────────────────┐
                 │   ClickHouse         │
                 │   security_events    │
                 └──────────┬───────────┘
                             │ HTTP (JSONEachRow)
                             │ [clickhouse_client.py]
                             ▼
   data/sample_data.csv ──▶  Prototype (main.py)
   (fallback if            │
    ClickHouse is           │ group by campaign_id
    unreachable)             ▼
                 ┌─────────────────────┐
                 │   agent.py           │
                 │   Anthropic API      │──▶ per-campaign hypothesis,
                 │   (Claude Haiku 4.5) │    MITRE mapping, confidence
                 └──────────┬───────────┘
                             ▼
                 ┌─────────────────────┐
                 │   report.py          │──▶ report.md
                 └─────────────────────┘
```

- **ClickHouse** — primary store for the `security_events` table. Queried over HTTP by [`prototype/clickhouse_client.py`](./prototype/clickhouse_client.py); if it's unreachable, the prototype automatically falls back to the local CSV in [`data/`](./data).
- **Prototype orchestrator** ([`prototype/main.py`](./prototype/main.py)) — fetches malicious-flagged events, groups them into multi-step campaigns vs. isolated events, and drives investigation + report assembly.
- **Agent** ([`prototype/agent.py`](./prototype/agent.py)) — builds the investigation prompt per event group and calls the Anthropic API (`claude-haiku-4.5`) to produce a hypothesis, MITRE ATT&CK mapping, confidence level, and recommended next step.
- **Report** ([`prototype/report.py`](./prototype/report.py)) — assembles per-campaign sections into `report.md`.
- **Config** ([`prototype/config.py`](./prototype/config.py)) — single source of truth for all environment-derived settings; nothing else reads `os.environ` directly.

Required environment variables (see `.env.example`): `CLICKHOUSE_URL`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD`, `CLICKHOUSE_DATABASE`, `ANTHROPIC_API_KEY`.

## Environment setup

Copy `.env.example` to `.env` and fill in real credentials. Never commit `.env`.

```bash
cp .env.example .env
```

Install Python dependencies:

```bash
py -m pip install -r requirements.txt
```

## Roadmap

| Phase | Name | Target finish |
|---|---|---|
| 1 | Prototype | Jul 2026, Wk 1 |
| 2 | Planning | Jul 2026, Wk 3 |
| 3 | Data and Baseline | Aug 2026, Wk 3 |
| 4 | Agent Development | Sep 2026, Wk 1 |
| 5 | Fine-Tuning | Sep 2026, Wk 3 |
| 6 | Multi-Agent | Oct 2026, Wk 1 |
| 7 | Analysis and Evaluation | Oct 2026, Wk 3 |
| 8 | Scalability | Oct 2026, Wk 4 |
| 9 | Maintainability | Nov 2026, Wk 1 |
| 10 | Reporting | Nov 2026, Wk 3 |
| 11 | Release | Nov 2026, Wk 4 |

Full details in [`docs/`](./docs).
