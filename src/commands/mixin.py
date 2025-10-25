from typing import Optional


class CommandMixin:
    def load_build(
        self,
        file_name: str,
        build_name: Optional[str],
    ) -> dict: ...

    def save_build(
        self,
        file_name: str,
        build_name: Optional[str],
        file_sub_path: Optional[str],
    ) -> dict: ...

    def download_build(
        self,
        link: str,
        build_name: Optional[str],
    ) -> dict: ...

    def upload_build(
        self,
        website_id: int,
        with_code: Optional[bool],
    ) -> dict: ...

    def create_build(
        self,
        build_name: Optional[str],
    ) -> dict: ...

    def get_build_folder(self) -> dict: ...

    def list_build(
        self,
        prefix: Optional[str],
        suffix: Optional[str],
    ) -> dict: ...

    def list_item_base_type(self) -> dict: ...

    def list_item_base(
        self,
        base_type: str,
    ) -> dict: ...

    def list_item_unique_type(self) -> dict: ...

    def list_item_unique(
        self,
        base_type: str,
    ) -> dict: ...

    def list_item(self) -> dict: ...

    def list_item_slot(self) -> dict: ...

    def set_item_slot(
        self,
        slot_name: str,
        item_id: int,
        item_set_id: Optional[int] = 1,
    ) -> dict: ...

    def add_item(
        self,
        raw: str,
    ) -> dict: ...

    def list_socket_group(self) -> dict: ...

    def list_socket_group_gem(
        self,
        slot_id: str,
    ) -> dict: ...
