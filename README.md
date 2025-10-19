# Path of Building AI

## Installation

Clone this repository with submodules:

```sh
git clone --recursive https://github.com/nakashimas/PathOfBuildingAI.git
cd PathOfBuildingAI
```

If you already cloned without `--recursive`, initialize and update submodules manually:

```sh
git submodule init
git submodule update
```

Install Python dependencies:

```sh
pip install -r requirements.txt
```

Apply the MCP patch and launch AI tool:

```sh
python -m src
```

> This will create `src/Modules/MCP.lua` and modify `src/Modules/Main.lua` to enable the CLI/AI server.
> The patch is applied locally and will not be committed to the repository.

Only Apply patch:

```sh
python -m src patch
```

## Usage

### Introduction

```sh
python -m src <<MODE>> <<OPTIONS>>
```

- Make sure `launch.devMode = true` in Path of Building.
- You can then communicate with PoB via CLI commands or Python scripts.

### CLI

First, start the client and obtain its PID.

```sh
python -m src cli start
# > 8888
```

Next, send a request by specifying the PID.
The response includes a random number used to detect file changes.

```sh
python -m src cli request --body "{}" --pid 8888
# > {"_rand": 0.99999999}
```

### CHAT

TBD.

Planned outline:

```sh
python -m src chat
# Input Chat / Press Ctrl + C to Exit
# I > こんにちは、私が最近作った Righteous Fire のビルドを読み込んでください。
# O >> "My Perfect RF Starter"を表示しました、続いてお手伝いできることはありますか？
```

### CUI

TBD.

Planned outline:

```sh
python -m src cui
# Input Commands / Press Ctrl + C to Exit
# I > load build C:/User/path/to/farmer.xml
# O >> {'status': 200, '_rand': '0.70940703694654'}
# or
# O >> SUCCESS load build
```
