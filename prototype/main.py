"""
SOC Agent Prototype - Phase 1 entrypoint.

This file only orchestrates: fetch -> group -> investigation -> assemble -> save.
No SQL, no prompts, no LLM calls should live here - see clickhouse_client.py, agent.py, and report.py.

Setup:
    pip install requests openai --break-system-packages

Environment variables:
    CLICKHOUSE_URL, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD, CLICKHOUSE_DATABASE, OPENROUTER_API_KEY
"""

import requests
import prototype.config as config
import prototype.clickhouse_client as clickhouse
import prototype.agent as agent
import prototype.report as report


def main():
    print("Fetching malicious events from Clickhouse...")
    try:
        events = clickhouse.fetch_malicious_events()
    except (requests.RequestException, RuntimeError) as exc:
        print(f"Clickhouse unavailable ({exc}); falling back to {config.SAMPLE_DATA_CSV_PATH}")
        events = clickhouse.fetch_malicious_events_from_csv()
    print(f"Fetched {len(events)} malicious-flagged events.")

    campaigns, isolated = report.group_by_campaign(events)
    print(f"Found {len(campaigns)} multi-step campaigns and {len(isolated)} isolated events.")

    sections = []
    for campaign_id, campaign_events in campaigns.items():
        print(f"Investigating campaign {campaign_id} with {len(campaign_events)} events...")
        investigation = agent.investigate(campaign_events, label=f"Campaign {campaign_id}")
        sections.append(f"## Campaign {campaign_id}\n\n{investigation}\n")

    if isolated:
        sample = isolated[:config.ISOLATED_EVENTS_SAMPLE_SIZE]

        print(f"Investigating {len(isolated)} isolated events...")
        investigation = agent.investigate(sample, label="Isolated single-step Suspicious Events sample")
        sections.append(f"## Isolated Events Sample\n\n{investigation}")
    
    full_report = report.assemble(sections)
    report.save(full_report)

    print(f"Report saved to {config.REPORT_OUTPUT_PATH}")
    print(full_report)

if __name__ == "__main__":
    main() 
