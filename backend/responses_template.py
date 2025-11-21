import yaml
import os

# Load templates.yml once when server starts
with open(os.path.join(os.path.dirname(__file__), "templates.yml"), "r", encoding="utf-8") as f:
    templates = yaml.safe_load(f)

def render_template(key, lang="en", **kwargs):
    
    """
    Fetch a template by key and language, fill placeholders like {name}, {score}.
    Falls back to English if the language is missing.
    """
    text_dict = templates.get(key, {})
    text = text_dict.get(lang, text_dict.get("en", f"[Missing template: {key}]"))
    return text.format(**kwargs) if kwargs else text
