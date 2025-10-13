import hashlib
import subprocess
from pathlib import Path
import time

from src.lua_scripts.apply_patch import apply_patch
from src.utils.constant import (
    FILE_POB_RUNTIME,
    FILE_TEMP_REQUEST,
    FILE_TEMP_RESPONSE,
)


class PathOfBuilding:
    def __init__(
        self,
        exe_path=FILE_POB_RUNTIME,
        force_update: bool = False,
        request_command_file: Path | str = FILE_TEMP_REQUEST,
        response_command_file: Path | str = FILE_TEMP_RESPONSE,
    ):
        self.exe_path = str(exe_path)
        self.process = None
        self._last_response_hash = ""

        apply_patch(force_update)

        Path(request_command_file).touch(exist_ok=True)
        Path(response_command_file).touch(exist_ok=True)

        self.request_command_file = Path(request_command_file)
        self.response_command_file = Path(request_command_file)

    def __enter__(self):
        self.start()
        print(f"Start Path of Building with PID={self.process.pid}")
        return self

    def __exit__(self, *_):
        if self.process and self.process.poll() is None:
            print("Exit Path of Building")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("____ Exit Timeout")
                self.process.kill()
            print("____ done")

    @classmethod
    def get_file_hash(cls, path: Path) -> str:
        if not path.exists():
            return ""
        sha256 = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def is_running(self):
        return self.process and self.process.poll() is None

    def start(self):
        self.process = subprocess.Popen([self.exe_path])

    def send_command(self, command: str):
        if not self.is_running():
            raise RuntimeError("Path of Building is Not Running")

        self.request_command_file.write_text(command, encoding="utf-8")
        self._last_response_hash = self.get_file_hash(
            self.response_command_file,
        )
        print(f"Command sent: {command}")

    def read_response(self) -> str:
        if self.response_command_file.exists():
            return self.response_command_file.read_text(encoding="utf-8")
        return ""

    def wait_for_response(
        self,
        timeout=10.0,
        poll_interval=0.5,
    ) -> str:
        start = time.time()
        while True:
            if time.time() - start > timeout:
                raise TimeoutError("Response timeout")

            current_hash = self.get_file_hash(self.response_command_file)
            if current_hash:
                time.sleep(0.05)  # Buffer
                response = self.read_response()
                self._last_response_hash = current_hash
                return response

            time.sleep(poll_interval)

    def send_and_wait(
        self,
        command: str,
        timeout=10.0,
        poll_interval=0.1,
    ) -> str:
        self.send_command(command)
        return self.wait_for_response(
            timeout=timeout,
            poll_interval=poll_interval,
        )
