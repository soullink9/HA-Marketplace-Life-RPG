# Tests

Run everything from the repository root. Each test is a plain Python script, not a pytest suite: it prints what it
checks and exits non-zero if anything failed. These are the commands the Test workflow runs:

```sh
pip install -r tests/requirements.txt
python3 tests/test_engine.py
python3 tests/test_engine_soak.py 3 1 2
python3 tests/test_integration.py
python3 tests/test_integration_soak.py 0.5 sdxl
python3 tests/test_integration_soak.py 0.5 flux_unet
python3 tests/test_release.py
```

| Script | What it checks |
|---|---|
| `test_engine.py` | Engine rule checks and a multi-year simulation (plain python, no Home Assistant) |
| `test_engine_soak.py` | 30-year soak test: play the engine for decades with normal and hostile players and check nothing breaks |
| `test_integration.py` | Integration test: the whole Home Assistant side (setup, config and options flows, coordinator, sensors, buttons, services, websocket API, Assist tools, the art studio and the LLM writer) against Home Assistant stand-ins (stubs.py), a fake ComfyUI that checks every workflow against ComfyUI's real node signatures, and a fake AI Task LLM |
| `test_integration_soak.py` | Multi-year soak of the Home Assistant side: coordinator + art studio (fake ComfyUI) + LLM writer (fake AI Task) |
| `test_release.py` | The release scripts in `scripts/`: the version check and notes, building and checking the zip, publishing to a fake Gitea server, and working out which releases GitHub still needs |

[CONTRIBUTING.md](../CONTRIBUTING.md#checking-a-change) says which to run for which change, and how long each takes.
The tests stand in for Home Assistant (`stubs.py`), so they can't prove the integration works on a real Home
Assistant: try changes on a real installation too.
