"""
Jinja2 Template Rendering for GPT Prompts

Provides utilities to render Jinja2 templates with automatic JSON-safe formatting.
Useful for creating dynamic prompts from templates.
"""

from jinja2 import Environment, FileSystemLoader


def render_template(template_name, **kwargs):
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('prompts'))

    # Make JSON safe if str
    for k, v in kwargs.items():
        kwargs[k] = replace_in_value(v)

    # Load the template with the given type (html, txt, etc.)
    template = env.get_template(template_name)

    # Use **kwargs as the data for rendering the template
    return template.render(**kwargs)

def replace_in_value(value):
    if isinstance(value, str):
        return value.replace('"', '')
    elif isinstance(value, dict):
        return {k: replace_in_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [replace_in_value(v) for v in value]
    else:
        return value
