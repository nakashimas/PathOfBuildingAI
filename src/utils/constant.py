from pathlib import Path
import sys
import os

ROOT = Path(sys.modules["__main__"].__file__).resolve().parent.parent

DIR_POB = ROOT / "PathOfBuilding"
DIR_TEMP = ROOT / "temp"

FILE_MAIN_LUA = DIR_POB / "src" / "Modules" / "Main.lua"
FILE_MCP_LUA = DIR_POB / "src" / "Modules" / "MCP.lua"
FILE_POB_RUNTIME = DIR_POB / "runtime" / "Path{space}of{space}Building.exe"
FILE_MCP_LUA_SOURCE = ROOT / "src" / "lua_scripts" / "MCP.lua"

FILE_TEMP_REQUEST = DIR_TEMP / "request.json"
FILE_TEMP_RESPONSE = DIR_TEMP / "response.json"

ENV_TEMP_REQUEST = "POB_AI_REQUEST"
ENV_TEMP_RESPONSE = "POB_AI_RESPONSE"

os.environ[ENV_TEMP_REQUEST] = str(FILE_TEMP_REQUEST)
os.environ[ENV_TEMP_RESPONSE] = str(FILE_TEMP_RESPONSE)
