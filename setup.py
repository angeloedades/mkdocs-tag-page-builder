import os
from setuptools import setup, find_packages


def read_file(fname):
    "Read a local file"
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="mkdocs-tag-page-builder",
    version="0.0.1",
    description="An MkDocs plugin to a set of pages with tags",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    keywords="mkdocs python markdown tag hierarch tags",
    url="https://github.com/angeloedades/mkdocs-tag-page-builder",
    author="Angelo Edades",
    author_email="angelo@aedad.es",
    license="MIT License",
    python_requires=">=3.10",
    install_requires=[
        "mkdocs>=1.3",
        "jinja2",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(exclude=["*.tests"]),
    package_data={"tagpagebuilder": ["templates/*.md.template"]},
    entry_points={
        "mkdocs.plugins": ["tagpagebuilder = tagpagebuilder.plugin:TagPageBuilderPlugin"]
    },
)
