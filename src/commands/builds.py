import json
from src.pob.client import PathOfBuilding
from src.commands.common import file_name_to_build_name
from src.utils.upload_build_code import upload_build_code, WEBSITE_LIST


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


def download_build(
    pob: PathOfBuilding,
    link: str,
    build_name: str = None,
):
    result = pob.send_and_wait(
        json.dumps(
            {
                "command": "downloadBuild",
                "link": link,
                "buildName": build_name,
            }
        ),
    )

    return json.loads(result)


def upload_build(
    pob: PathOfBuilding,
    website_id: int,
    with_code: bool = False,
):
    result = pob.send_and_wait(
        json.dumps(
            {
                "command": "uploadBuild",
                "websiteId": website_id,
            }
        ),
    )

    result = json.loads(result)

    website_info = WEBSITE_LIST[website_id - 1]
    response, error = upload_build_code(result.get("code"), website_info)

    if not with_code:
        result["code"] = "<<code>>"

    if error:
        result["error"] = str(error)
        return result

    result["url"] = website_info["linkURL"].format(response)

    return result
