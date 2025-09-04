# prompt_to_xml/converter.py

import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List, Dict


def extract_dates(prompt: str) -> List[str]:
    dates = []
    for m in re.finditer(r"\b(?:\d{1,2}\s*[A-Za-z]+|\b[A-Za-z]+\s*\d{1,2}\b)", prompt):
        dates.append(m.group(0))
    return dates


def extract_numbers(prompt: str) -> List[str]:
    return re.findall(r"\b\d+\b", prompt)


def extract_names(prompt: str) -> List[str]:
    words = re.findall(r"\b[A-Z][a-zA-Z]+\b", prompt)
    months = {
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December",
        "Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    }
    cleaned = []
    for c in words:
        if c in months or len(c) <= 1:
            continue
        if c.lower() in prompt.lower():
            cleaned.append(c)
    seen, out = set(), []
    for n in cleaned:
        if n not in seen:
            out.append(n)
            seen.add(n)
    return out


def extract_items(prompt: str) -> List[str]:
    items = []
    for m in re.finditer(r"(?:to|for|buy|order|get)\s+([A-Za-z0-9\- ]{2,60})", prompt, flags=re.IGNORECASE):
        item = m.group(1).strip(" .,!") 
        items.append(item)
    return items


def detect_intent(prompt: str) -> str:
    if "book" in prompt.lower() and "flight" in prompt.lower():
        return "book_flight"
    elif "buy" in prompt.lower() or "order" in prompt.lower():
        return "purchase"
    return "general"


def build_xml(intent: str, entities: Dict[str, List[str]], context: Dict[str, str], raw: str) -> str:
    root = ET.Element("query")

    it = ET.SubElement(root, "intent")
    it.text = intent

    ents = ET.SubElement(root, "entities")
    for k, values in entities.items():
        for v in values:
            el = ET.SubElement(ents, k)
            el.text = str(v)

    ctx = ET.SubElement(root, "context")
    for k, v in context.items():
        el = ET.SubElement(ctx, k)
        el.text = str(v)

    raw_el = ET.SubElement(root, "raw")
    raw_el.text = raw

    # ✅ Pretty-print with indentation
    rough_string = ET.tostring(root, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def convert_to_xml(prompt: str) -> str:
    """Main exported function. Returns XML string for the prompt."""
    intent = detect_intent(prompt)
    dates = extract_dates(prompt)
    numbers = extract_numbers(prompt)
    names = extract_names(prompt)
    items = extract_items(prompt)

    entities = {}
    if dates:
        entities["date"] = dates
    if names:
        entities["name"] = names
    if numbers:
        entities["number"] = numbers
    if items:
        entities["item"] = items

    context = {}
    if "urgent" in prompt.lower() or "asap" in prompt.lower():
        context["priority"] = "high"
    else:
        context["priority"] = "normal"

    xml = build_xml(intent, entities, context, prompt)
    return xml


# If run as script for testing
if __name__ == "__main__":
    sample = "Book a flight to Berlin on Oct 1st. It's urgent."
    print(convert_to_xml(sample))
