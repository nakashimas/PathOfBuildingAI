import json

from src.pob.client import PathOfBuilding


def list_item_base_type(pob: PathOfBuilding):
    result = pob.send_and_wait(json.dumps({"command": "listItemBaseType"}))
    return json.loads(result)


def list_item_base(pob: PathOfBuilding):
    result = pob.send_and_wait(json.dumps({"command": "listItemBase"}))
    return json.loads(result)


def add_item(
    pob: PathOfBuilding,
    raw: str,
):
    result = pob.send_and_wait(
        json.dumps(
            {
                "command": "addItem",
                "item": {"raw": raw},
            }
        )
    )

    return json.loads(result)
