import logging
import mkdocs
from packaging.version import Version

#
# Logging
#
log = logging.getLogger("mkdocs.plugins." + __name__)

MKDOCS_LOG_VERSION = "1.2"
if Version(mkdocs.__version__) < Version(MKDOCS_LOG_VERSION):
    # filter doesn't do anything since that version
    from mkdocs.utils import warning_filter
    log.addFilter(warning_filter)

TAGPAGEBUILDER_LABEL = "TAG-PAGE-BUILDER: "  # plugin's signature label


def info(*args) -> str:
    "Write information on the console, preceded by the signature label"
    args = [TAGPAGEBUILDER_LABEL] + [str(arg) for arg in args]
    msg = " ".join(args)
    log.info(msg)
