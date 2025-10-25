import json

from src.pob.client import PathOfBuilding


def list_socket_group(pob: PathOfBuilding):
    result = pob.send_and_wait(json.dumps({"command": "listSocketGroup"}))
    return json.loads(result)


def list_socket_group_gem(
    pob: PathOfBuilding,
    slot_id: str,
):
    result = pob.send_and_wait(
        json.dumps(
            {
                "command": "listSocketGroupGem",
                "slotId": slot_id,
            }
        )
    )
    return json.loads(result)
