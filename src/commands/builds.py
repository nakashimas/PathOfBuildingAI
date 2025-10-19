import json
from src.pob.client import PathOfBuilding
from src.commands.common import file_name_to_build_name


def load_build(
    pob: PathOfBuilding,
    file_name: str,
    build_name: str = None,
):
    if build_name is None:
        build_name = file_name_to_build_name(None, file_name)

    result = pob.send_and_wait(
        json.dumps(
            {
                "command": "loadBuild",
                "fileName": file_name,
                "buildName": build_name,
            }
        )
    )

    return json.loads(result)


def save_build(
    pob: PathOfBuilding,
    file_name: str,
    build_name: str = None,
    file_sub_path: str = None,
):
    if build_name is None:
        build_name = file_name_to_build_name(None, file_name)

    result = pob.send_and_wait(
        json.dumps(
            {
                "command": "saveBuild",
                "fileName": file_name,
                "buildName": build_name,
                "fileSubPath": file_sub_path,
            }
        )
    )

    return json.loads(result)
