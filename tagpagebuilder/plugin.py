from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type
from .utilities import info

class TagHierarchyPlugin(BasePlugin):
    config_scheme = (
        ("topics", Type(str)),
        ("document_folder", Type(str, default="docs")),
        ("page_template", Type(str)),
    )

    def __init__(self):
        self.topics = None
        self.document_folder = "docs"
        self.page_template = None

    def on_config(self, config):
        info("Assigning pluging configuraton options")