import os


def file_name_to_build_name(_, file_name: str):
    return os.path.splitext(os.path.basename(file_name))[0]
