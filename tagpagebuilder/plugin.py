import jinja2
from pathlib import Path
from collections import defaultdict
from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type
from .utilities import info
from .helpers import get_metadata


class TagPageBuilderPlugin(BasePlugin):
    config_scheme = (
        ("topics", Type(list)),
        ("document_folder", Type(str, default="docs")),
        ("page_template", Type(str)),
    )

    def __init__(self):
        self.topics = []
        self.document_folder = "docs"
        self.page_template = None

    def on_config(self, config):
        info("Assigning plugin configuraton options")

        self.topics = self.config.get("topics")
        self.document_folder = Path(
            self.config.get("document_folder") or self.tags_folder
        )

        # Ensure that the document_folder folder is absolute, and it exists
        if not self.document_folder.is_absolute():
            self.document_folder = (
                Path(config["docs_dir"]) / ".." / self.document_folder
            )
        if not self.document_folder.exists():
            self.document_folder.mkdir(parents=True)

        if self.config.get("page_template"):
            self.page_template = Path(self.config.get("page_template"))

    def on_files(self, files, config):
        info("Generating files")

        for topic_name in self.topics:
            topic_files = self.get_topic_files(
                topic_name=topic_name, files=files, config=config
            )

            self.generate_tags_file(topic_name=topic_name, topic_files=topic_files)

    def get_topic_files(self, topic_name, files, config):
        info(f"Getting files under topic: {topic_name}")

        topic_files = []

        for file in files:
            if not file.src_path.endswith(".md"):
                continue
            file_metadata = get_metadata(file.src_path, config["docs_dir"])
            if file_metadata is not None:
                if "topic" in file_metadata:
                    if "," in file_metadata["topic"]:
                        for single_topic in str(file_metadata["topic"]).split(","):
                            if single_topic == topic_name:
                                info(f"Adding {file.src_path} to {topic_name}")
                                topic_files.append(get_metadata(file.src_path, config["docs_dir"]))
                    else:
                        if file_metadata["topic"] == topic_name:
                            info(f"Adding {file.src_path} to {topic_name}")
                            topic_files.append(get_metadata(file.src_path, config["docs_dir"]))

        return topic_files

    def generate_topic_page(self, data, topic_name):
        info(f"Generating a topic page for: {topic_name}")
        if self.page_template is None:
            template_path = Path(__file__).parent / Path("templates")
            environment = jinja2.Environment(
                loader=jinja2.FileSystemLoader(str(template_path))
            )
            template = environment.get_template("page.md.template")
        else:
            environment = jinja2.Environment(
                loader=jinja2.FileSystemLoader(
                    searchpath=str(self.tags_template.parent)
                )
            )
            template = environment.get_template(str(self.page_template.name))
        output_text = template.render(
            tags=sorted(data.items(), key=lambda t: t[0].lower()),
            topic_name=topic_name,
        )
        return output_text

    def generate_tags_file(self, topic_name, topic_files):
        info(f"Generating a topics page file for {topic_name}")
        sorted_topic_files = sorted(
            topic_files, key=lambda e: e.get("year", 5000) if e else 0
        )
        tag_dict = defaultdict(list)
        for e in sorted_topic_files:
            if not e:
                continue
            if "title" not in e:
                e["title"] = "Untitled"
            tags = e.get("tags", [])
            if tags is not None:
                for tag in tags:
                    tag_dict[tag].append(e)

        t = self.generate_topic_page(data=tag_dict, topic_name=topic_name)

        with open(f"{self.document_folder}/{topic_name}.md", "w") as f:
            f.write(t)
