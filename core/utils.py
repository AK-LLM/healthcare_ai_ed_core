import json
import os

def get_strings(lang="en"):
    loc_file = os.path.join("locales", lang, "strings.json")
    if os.path.exists(loc_file):
        with open(loc_file) as f:
            return json.load(f)
    return {}
