import hashlib
import subprocess
import time
import importlib
import inspect
import pkgutil
from pathlib import Path

import psutil

from src.commands.mixin import CommandMixin
from src.lua_scripts.apply_patch import apply_patch
from src.utils.constant import (
    FILE_POB_RUNTIME,
    FILE_TEMP_REQUEST,
    FILE_TEMP_RESPONSE,
    ROOT,
)


class PathOfBuilding:
    def __init__(
        self,
        exe_path=FILE_POB_RUNTIME,
        force_update: bool = False,
        request_command_file: Path | str = FILE_TEMP_REQUEST,
        response_command_file: Path | str = FILE_TEMP_RESPONSE,
        pid: int | None = None,  # ← 外部プロセス用
    ):
        self.exe_path = str(exe_path)
        self.pid = pid
        self.process = None
        self._last_response_hash = ""

        apply_patch(force_update)
        Path(request_command_file).touch(exist_ok=True)
        Path(response_command_file).touch(exist_ok=True)

        self.request_command_file = Path(request_command_file)
        self.response_command_file = Path(response_command_file)

    def __enter__(self):
        if self.pid is None:
            self.start()
            print(f"Start Path of Building with PID={self.process.pid}")
        else:
            print(f"Attach to existing Path of Building PID={self.pid}")
        return self

    def __exit__(self, *_):
        if self.pid is not None:
            print("Detach from external process (not terminating).")
            return

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

    @classmethod
    def _check_alive(cls, pid: int) -> bool:
        try:
            proc = psutil.Process(pid)
            return proc.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def is_running(self) -> bool:
        if self.pid is not None:
            return self._check_alive(self.pid)
        if self.process:
            return self.process.poll() is None
        return False

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
            if current_hash and current_hash != self._last_response_hash:
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


class PathOfBuildingCli(CommandMixin, PathOfBuilding):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_commands()

    def _load_commands(self):
        package_path = ROOT / "src" / "commands"

        for _, module_name, _ in pkgutil.iter_modules([str(package_path)]):
            module = importlib.import_module(f"src.commands.{module_name}")

            for name, func in inspect.getmembers(module, inspect.isfunction):
                bound_method = func.__get__(self, self.__class__)
                setattr(self, name, bound_method)
