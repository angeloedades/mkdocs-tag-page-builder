import yaml
from pathlib import Path
from .utilities import info

#
# Helpers
#
def get_metadata(name, path):
    # Extract metadata from the yaml at the beginning of the file
    def extract_yaml(f):
        result = []
        c = 0
        for line in f:
            if line.strip() == "---":
                c += 1
                continue
            if c == 2:
                break
            if c == 1:
                result.append(line)
        return "".join(result)

    filename = Path(path) / Path(name)
    with filename.open() as f:
        metadata = extract_yaml(f)
        if metadata:
            meta = yaml.load(metadata, Loader=yaml.FullLoader)
            meta.update(filename=name)
            info(f"META: {meta}")
            return meta
