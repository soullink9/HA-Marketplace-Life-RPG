For anyone changing the code. [CONTRIBUTING.md](../CONTRIBUTING.md) has the rules the code keeps and how to release.

## Testing
Everything runs with plain Python 3.13; nothing needs a real Home Assistant, ComfyUI or LLM.

| Command | What it checks |
|---|---|
| `python3 tests/test_engine.py` | The game's rules, then a three-year simulation of a casual, a steady and a dedicated player (the Pacing table comes from it). |
| `python3 tests/test_engine_soak.py` | A 30-year soak with casual, steady, grinder, shopper and chaotic players (breaks of up to two months, missing and junk sensor data, random and invalid actions, a restart every year). It checks for crashes, broken invariants, save size and update speed. `python3 tests/test_engine_soak.py 3 1 2` is a quicker 3-year run. |
| `python3 tests/test_integration.py` | The whole Home Assistant side (setup, options, sensors, buttons, actions, the panel's websocket API, Assist tools, the painter and the LLM writer) against stand-ins for Home Assistant, a fake ComfyUI that checks every workflow against ComfyUI's real node signatures, and a fake LLM. Needs `pip install -r tests/requirements.txt`. |
| `python3 tests/test_integration_soak.py 3 sdxl` | Three years of the Home Assistant side in fast time, with the fake ComfyUI (`sdxl` or `flux_unet`) and LLM: painting and writing budgets, queues, the art folder. |
| `python3 tests/test_release.py` | The release scripts in `scripts/`: the version check (all four places) and notes, building and checking the zip, and publishing to a fake Gitea server. |

Gitea's runner runs these on every push (shorter soaks), plus `ruff`, the panel check and building the zip; GitHub runs the same plus Home Assistant's `hassfest` and the Marketplace's checks. See [CONTRIBUTING.md](../CONTRIBUTING.md) for where to make changes and how to release.

## Files

| Path | What it holds |
|---|---|
| `custom_components/life_rpg/` | The integration. `__init__.py` sets it up and registers the panel; `config_flow.py` the setup and Configure pages; `coordinator.py` reads the sensors and runs one adventurer's game; `sensor.py`, `event.py`, `button.py` the entities; `services.py` the actions; `websocket.py` the panel's API; `llm_api.py` the Assist tools; `lore.py` the LLM's words; `art.py` the ComfyUI painter. |
| `custom_components/life_rpg/engine/` | The whole game in plain Python, with no Home Assistant imports. `game.py` holds the `Game` class (the day loop, scoring, progression, the labyrinth, choices and emergencies), with its other parts in `shop.py` (the market), `board.py` (the bounty board), `inputs.py` (sensors, corrections and hand logging) and `characters.py` (portrait choices, chats and gifts). `rules.py` has the tuning constants and formulas, `content.py` every name, table and line of text, `loot.py` chests and gear, `market.py` gold, stock and haggling, and `appearance.py` looks and painting prompts. |
| `custom_components/life_rpg/frontend/` | The System panel and cards (`life-rpg.js`), their styles (`styles.js`), the pixel-art engine (`art.js`) and the cast (`cast.js`). Plain ES modules, no build step. |
| `custom_components/life_rpg/translations/`, `services.yaml`, `brand/` | UI text, action descriptions and the integration's icon and logo. |
| `examples/` | A dashboard view and four phone-notification automations to copy from. |
| `tests/` | `test_engine*.py`: the engine (no Home Assistant needed); `test_integration*.py`: the Home Assistant side, with the stand-ins in `stubs.py`; `test_release.py`: the release scripts. `README.md` lists what each checks. |
| `scripts/` | The release helpers both release workflows use (see [Tests and releases: the files](#tests-and-releases-the-files)). |
| `pyproject.toml`, `.gitea/`, `.github/` (repository root) | Lint settings; Gitea's test and release workflows (the main copy, no GitHub needed); GitHub's checks (hassfest, the Marketplace's), its copy of each release and the bug report form. |

## Tests and releases: the files

Gitea is the main copy of this repository; it push-mirrors to GitHub, the public copy people install from.

| File | What it does |
|---|---|
| `.gitea/workflows/test.yml` | Runs every check on each push to Gitea (lint, the tests and building the zip, on Python 3.14, and the panel scripts on Node 20), with no actions downloaded from GitHub |
| `.gitea/workflows/release.yml` | Publishes a release on Gitea (Run workflow button, or a pushed version tag); its tag then reaches GitHub through the push mirror |
| `.github/workflows/release.yml` | Publishes the same release on GitHub when a version tag arrives there (or from its own Run workflow button): the copy the Marketplace installs from |
| `.github/workflows/ci.yml` | GitHub's checks on every push: lint, the tests and Home Assistant's `hassfest` (which comes from GitHub, so it runs only there) |
| `.github/workflows/validate.yml` | The Marketplace's own checks (the HACS action), which its catalog requires; GitHub only, for the same reason |
| `scripts/release_notes.py` | Shared by both release workflows: checks the version, gives the release's title, writes the notes (install steps with the zip's address on GitHub, then the changelog section) |
| `scripts/build_package.py` | Builds `dist/life_rpg.zip`, the same bytes every time, and checks it with `check_package.py` |
| `scripts/check_package.py` | Checks the zip the way it gets installed: one `life_rpg/` folder, a manifest for that domain at the repository's version, the icon, exactly the integration's files |
| `scripts/publish_gitea_release.py` | Creates or updates the Gitea release and uploads its files, through Gitea's API (standard library only) |
| `tests/test_release.py` | Tests all four scripts, publishing against a fake Gitea server |
