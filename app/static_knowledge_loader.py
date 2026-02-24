import os
import json

DATA_DIR = "data"

def load_static_knowledge():
    """Load and combine static JSON knowledge entries from the data directory."""
    all_entries = []

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            path = os.path.join(DATA_DIR, filename)

            with open(path, "r", encoding="utf-8") as f:
                entries = json.load(f)
                all_entries.extend(entries)

    return all_entries
