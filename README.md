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

Run the AI server:

```sh
python -m src
```

- Make sure `launch.devMode = true` in Path of Building.
- You can then communicate with PoB via CLI commands or Python scripts.
