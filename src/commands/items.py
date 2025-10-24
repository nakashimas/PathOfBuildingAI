import json

from src.pob.client import PathOfBuilding


def list_item_base_type(pob: PathOfBuilding):
    result = pob.send_and_wait(json.dumps({"command": "listItemBaseType"}))
    return json.loads(result)


def list_item_base(
    pob: PathOfBuilding,
    base_type: str,
):
    result = pob.send_and_wait(
        json.dumps(
            {
                "command": "listItemBase",
                "type": base_type,
            }
        )
    )
    return json.loads(result)


def list_item_unique_type(pob: PathOfBuilding):
    result = pob.send_and_wait(json.dumps({"command": "listItemUniqueType"}))
    return json.loads(result)


def list_item_unique(
    pob: PathOfBuilding,
    base_type: str,
):
    result = pob.send_and_wait(
        json.dumps(
            {
                "command": "listItemUnique",
                "type": base_type,
            }
        )
    )
    return json.loads(result)


def list_item(pob: PathOfBuilding):
    result = pob.send_and_wait(json.dumps({"command": "listItem"}))
    return json.loads(result)


def list_item_slot(pob: PathOfBuilding):
    result = pob.send_and_wait(json.dumps({"command": "listItemSlot"}))
    return json.loads(result)


def set_item_slot(
    pob: PathOfBuilding,
    slot_name: str,
    item_id: int,
    item_set_id: int = 1,
):
    result = pob.send_and_wait(
        json.dumps(
            {
                "command": "setItemSlot",
                "slotName": slot_name,
                "itemId": item_id,
                "itemSetId": item_set_id,
            }
        )
    )

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
