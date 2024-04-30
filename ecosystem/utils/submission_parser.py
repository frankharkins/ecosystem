"""Parser for issue submission."""
from collections import defaultdict
from pathlib import Path
import mdformat
import yaml

from ecosystem.models.repository import Repository


def _clean_section(section: str) -> {str: str}:
    """For a section, return a tuple with a title and "clean section".
    A clean section is without new lines and strip spaces"""
    paragraphs = section.split("\n")
    section = (" ").join(
        [paragraph.strip() for paragraph in paragraphs[1:] if paragraph]
    )
    title = paragraphs[0].strip()
    return (title, section)


def _section_titles_to_ids(sections: dict[str, str]) -> dict[str, str]:
    """Given a section title, find its `id` from the issue template"""
    issue_template = yaml.load(
        Path(".github/ISSUE_TEMPLATE/submission.yml").read_text(),
        Loader=yaml.SafeLoader,
    )
    label_to_id = {
        form["attributes"]["label"]: form["id"]
        for form in issue_template["body"]
        if form["type"] != "markdown"
    }
    return {label_to_id[key]: value for key, value in sections.items()}


def parse_submission_issue(body_of_issue: str) -> Repository:
    """Parse issue body.

    Args:
        body_of_issue: body of an GitHub issue in markdown

    Return: Repository
    """

    issue_formatted = mdformat.text(body_of_issue)

    sections = defaultdict(
        None, [_clean_section(s) for s in issue_formatted.split("### ")[1:]]
    )
    args = _section_titles_to_ids(sections)

    args = {
        key: (None if value == "_No response_" else value)
        for key, value in args.items()
    }

    if args["labels"] is None:
        args["labels"] = []
    else:
        args["labels"] = [l.strip() for l in args["labels"].split(",")]

    return Repository(**args)
