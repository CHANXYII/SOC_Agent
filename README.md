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

## Environment setup

Copy `.env.example` to `.env` and fill in real credentials. Never commit `.env`.

```bash
cp .env.example .env
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
