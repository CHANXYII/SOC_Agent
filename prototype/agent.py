"""
Agent reasoning logic lives here: turning raw events into a prompt,
and calling the LLM. Kept separate from data access and reporting so that
when phase 6 (Multi-Agent) splits this into severalspecialized agents,
this is the only file that needs to grow.
"""

from anthropic import Anthropic

import prototype.config as config


_client = Anthropic()   # reads ANTHROPIC_API_KEY from env


def build_prompt(events, label: str) -> str:
    lines = [f"Investigate the following security event group: {label}", ""]
    for event in events:
        lines.append(
            f"- [{event['event_time']}] source={event['source_ip']} dest={event['dest_ip']} "
            f"user={event['user_name']} log_source={event['log_source']} "
            f"type={event['event_type']} severity={event['severity']} "
            f"mitre={event['mitre_technique']} log=\"{event['raw_log']}\""
        )
    lines.append("")
    lines.append(
        "Based only on the evidence above, respond in this exact format:\n"
        "Hypothesis: <one sentence, what likely happened>\n"
        "Supporting evidence: <bullet list of which log lines support this, referencing event_id>\n"
        "MITRE mapping: <list technique IDs and name involved>\n"
        "Confidence: <low|medium|high> - <one sentence why>\n"
        "Recommended next step: <one sentence, what to do next>\n"
        "Limitations: <one sentence on what evidence is missing or ambiguous>"
    )
    return "\n".join(lines)


def investigate(events, label: str) -> str:
    """Send a event group to the LLM and return its investigation text."""
    prompt = build_prompt(events, label)
    response = _client.messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=config.ANTHROPIC_MAX_TOKENS,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return "".join(block.text for block in response.content if block.type == "text")
