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

    def list_item_base(self) -> dict: ...

    def add_item(
        self,
        raw: str,
    ) -> dict: ...
