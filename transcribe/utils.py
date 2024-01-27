import os
import re


def slugify(value):
    """
    Normalizes a string: converts to lowercase, removes non-alpha characters,
    and converts dashes and spaces to underscores.

    """
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    value = re.sub(r"[-\s]+", "_", value)
    return re.sub(r"[^\x00-\x7f]", "", value)


def get_filename(file_path):
    """
    Returns the filename without the filetype extension.

    """
    return os.path.splitext(os.path.basename(file_path))[0]
