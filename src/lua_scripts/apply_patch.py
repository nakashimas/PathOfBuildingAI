import shutil
from src.utils.constant import (
    FILE_MAIN_LUA,
    FILE_MCP_LUA_SOURCE,
    FILE_MCP_LUA,
)

MAIN_INIT_INSERT_BLOCK = [
    "",
    "\tif launch.devMode then",
    "\t\tMCP.startServer()",
    "\tend",
]


def patch_loadmodule_block(src: str) -> str:
    if 'LoadModule("Modules/MCP")' in src:
        print("[✓] LoadModule('Modules/MCP') already present.")
        return src

    lines = src.splitlines()
    new_lines = []
    inside_block = False

    for i, line in enumerate(lines):
        if line.startswith("LoadModule("):
            if not inside_block:
                inside_block = True
        elif inside_block:
            new_lines.append('LoadModule("Modules/MCP")')
            print(f"[+] Inserted LoadModule('Modules/MCP') Line {i + 1}")
            inside_block = False

        new_lines.append(line)

    return "\n".join(new_lines)


def patch_main_init(src: str) -> str:
    if "MCP.startServer" in src:
        print("[✓] MCP.startServer() already hooked.")
        return src

    lines = src.splitlines()
    new_lines = []
    inside_init = False
    func_start_idx = None
    insert_idx = None

    # First, locate the start line of function Main:Init()
    # and the line just before its corresponding end
    for i, line in enumerate(lines):
        if not inside_init and line.startswith("function main:Init"):
            inside_init = True
            func_start_idx = i
        elif inside_init and line.startswith("end"):
            insert_idx = i
            break

    if func_start_idx is None or insert_idx is None:
        raise RuntimeError(
            "Failed to locate 'function Main:Init() ... end' block",
        )

    # Skip if startServer is already inside the function body
    func_body = "\n".join(lines[func_start_idx:insert_idx])
    if "MCP.startServer" in func_body:
        print("[✓] MCP.startServer() already present inside Main:Init()")
        return src

    # Construct the new line list
    new_lines = []
    for i, line in enumerate(lines):
        new_lines.append(line)
        if i == insert_idx - 1:
            # Insert just before the 'end' line
            new_lines.extend(MAIN_INIT_INSERT_BLOCK)

    print("[+] Hooked MCP.startServer() into Main:Init() ")
    print(f"    before line {insert_idx + 1}")
    return "\n".join(new_lines)


def patch_main_lua():
    if not FILE_MAIN_LUA.exists():
        raise FileNotFoundError(f"{FILE_MAIN_LUA} not found")

    src = FILE_MAIN_LUA.read_text(encoding="utf-8")

    src = patch_loadmodule_block(src)
    src = patch_main_init(src)

    FILE_MAIN_LUA.write_text(src, encoding="utf-8")
    print("[✓] Main.lua patch complete.")


def patch_mcp_lua(force: bool = False):
    if FILE_MCP_LUA.exists() and not force:
        print("[✓] MCP.lua already exists.")
    else:
        shutil.copy(FILE_MCP_LUA_SOURCE, FILE_MCP_LUA)
        print("[✓] Create MCP.lua file.")

    print("[✓] MCP.lua patch complete.")


def apply_patch(force: bool = False):
    patch_main_lua()
    patch_mcp_lua(force)
