"""
Turning a list of events + their investigations into a finished report.
This is the file phase 10 (Report Generation) will expand the most —
kept separate so that work doesn't tangle with data access or agent logic.
"""

from collections import defaultdict
import prototype.config as config


def group_by_campaign(events):
    """Group events by campaign_id, Events with empty campaing_id are isolated."""
    campaigns = defaultdict(list)
    isolated = []
    for event in events:
        if event["campaign_id"]:
            campaigns[event["campaign_id"]].append(event)
        else:
            isolated.append(event)
    return campaigns, isolated


def assemble(sections: list[str]) -> str:
    return "# SOC Agent Prototype Report\n\n" + "\n\n".join(sections)


def save(report_text: str, path: str = None):
    path = path or config.REPORT_OUTPUT_PATH
    with open(path, "w") as f:
        f.write(report_text)
