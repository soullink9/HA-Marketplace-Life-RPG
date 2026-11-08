# Contributing to Life RPG

Thanks for helping. This page is for anyone changing the code: where things live, the rules the code keeps,
how to check a change, and how to release one.

## Ground rules

- **Nothing talks to the internet.** The only outside connections are the ComfyUI address the user enters and
  the AI Task entity or conversation agent they pick in Home Assistant. No fonts, scripts, images, analytics or
  update checks from anywhere else, in the integration or in the panel.
- **No new dependencies.** `manifest.json` has no `requirements`, and the panel has no build step. Pillow is used
  when present (it ships with Home Assistant) and everything works without it.
- **The engine stays pure.** `custom_components/life_rpg/engine/` never imports Home Assistant. It takes readings
  and a clock, and returns a view and events. That's what lets the simulations play 30 years in minutes.
- **The game decides every number.** The LLM only writes words, and it's told exactly what each reward is (a
  character's line that oversells a prize is thrown away).
- **Saves must keep loading.** A save is the JSON from `new_ledger()` in `engine/rules.py`. When it loads, any
  key the save doesn't have takes its default (`new_ledger() | saved`), so adding a key is safe. Renaming or
  reshaping a key needs a small conversion in `Game.__init__` so existing players keep their progress.

## Where things live

The [Development](docs/Development.md) page has the full file map. The usual places to make a change:

| To change | Look in |
|---|---|
| Names, flavour text, jobs, titles, badges, hidden quests, choices, side quests | `engine/content.py` |
| XP, levels, ranks, streaks, fines, limits and other tuning numbers | `engine/rules.py` |
| Chests, gear, affixes, enhancing, salvage, bonus caps | `engine/loot.py` |
| Prices, stock, deliveries, haggling | `engine/market.py` (rules) and `engine/shop.py` (the player's actions) |
| How characters look and the painting prompts | `engine/appearance.py` |
| ComfyUI workflows, the painting queue, the art folder | `art.py` |
| What the LLM is asked to write | `lore.py` |
| The panel and cards | `frontend/life-rpg.js`, styles in `frontend/styles.js` |
| The pixel art | `frontend/art.js` (adventurers, items, monsters) and `frontend/cast.js` (everyone else) |

**Adding a player action** (a new button): add the method to the `Game` class (or the mixin it belongs in),
add it to the handler table in `LifeRPGCoordinator.async_action` (`coordinator.py`), add any new argument to the
`life_rpg/action` schema in `websocket.py`, then call it from the panel with `this.action("name", {...})`.
Add an Assist tool in `llm_api.py` if it makes sense by voice.

**Adding an event:** add it to `EVENT_TYPES` in `engine/rules.py`, give it a line in `describe()` in
`frontend/life-rpg.js` (toasts and the log), add it to `translations/en.json` under `entity.event.achievements`, and list it
on the [Screens and Entities](docs/Screens-and-Entities.md) page.

**Adding an option:** the form is in `config_flow.py`, its labels in `translations/en.json`, and the option is
read in `coordinator.py`. Options apply without losing progress (the entry reloads).

## Checking a change

You need Python 3.13 or newer (Home Assistant 2026.9 itself runs on 3.14, which is what the workflows use), and
Node 20 or newer for the panel check. The engine checks need nothing else; for the rest:

```sh
pip install -r tests/requirements.txt
```

| Command | Time | When |
|---|---|---|
| `ruff check custom_components tests` and `ruff format custom_components tests` | seconds | every change |
| `for f in custom_components/life_rpg/frontend/*.js; do node --check "$f"; done` | seconds | any panel change |
| `python3 tests/test_engine.py` | a minute or two | every change |
| `python3 tests/test_integration.py` | seconds | any change outside `engine/` |
| `python3 tests/test_engine_soak.py 30 1 2 3 4 5 6` | long (minutes per player and seed, on all cores) | any change to how the game plays |
| `python3 tests/test_integration_soak.py 3 sdxl` and `python3 tests/test_integration_soak.py 3 flux_unet` | several minutes each | any change to painting, writing or the coordinator |
| `python3 tests/test_release.py` | seconds | any change to `scripts/` or the release workflows |
| `python3 scripts/build_package.py` | seconds | before a release: builds `dist/life_rpg.zip` and checks it installs |

Any change to how the game plays (rules, rewards, content pools, the market) gets the full 30-year run before it
ships: some problems (a list that grows forever, a number that overflows, a pool that runs dry) only show up
after years of play. The run prints `30/30 runs finished cleanly` when all is well.

Gitea's runner runs lint, the panel check, the unit tests, a 3-year soak, the Home Assistant tests (with
half-year soaks), the release tests and the zip build on every push (`.gitea/workflows/test.yml`). On GitHub the same
checks run plus Home Assistant's `hassfest` and the Marketplace's own checks, which come from GitHub and can only run
there. [tests/README.md](tests/README.md) lists what each test checks.

Code style: `ruff` settles formatting and import order (see `pyproject.toml`). Every function and class has a
docstring, and comments say why, not what. In the panel, keep to plain JavaScript modules with no build step.

## Documentation

[README.md](README.md) is the front page, and every other page lives in [`docs/`](docs). When a change alters
something a page describes, update that page in the same commit.

## Standards for every change

- **Readable over clever.** Write code a newcomer can follow on the first read. Prefer a few plain lines with a named
  variable to a dense one-liner, a nested conditional expression, or a trick that needs a comment to decode.
- **Comment the why.** Every function and class has a docstring. Comments explain why the code does something
  non-obvious (a quirk of the device or service, a Home Assistant rule, a deliberate trade-off), not what each line
  does.
- **Keep names consistent.** Follow the names already used in the integration: the same words for
  the same things, Home Assistant's conventions for entities and config entries, `snake_case` for Python names and
  `camelCase` for JavaScript.
- **Keep the docs in step.** When you change a function, class or behaviour, update its docstring, its comments and the
  pages under `docs/` (and the README) that describe it in the same commit.
- **Keep the tests green.** Every change keeps existing behaviour and passes all of the tests. When you
  fix a bug, add the situation that caused it to the tests so it stays fixed.
- **No new dependencies without approval.** Don't add a third-party library (to a `manifest.json`, a
  `requirements.txt` or CI) without asking in an issue first. This page says what it already depends on and why.

### Test layout

The tests use these names:

```
tests/
  stubs.py                stand-ins for Home Assistant and the libraries the integration uses
  test_integration.py     the real integration against the stand-ins and a fake device or service
  test_<subject>.py       any other checks (test_engine.py, test_blueprint.py, test_live_proxy.py)
  test_<subject>_soak.py  a long simulation: it takes a length as an argument, and CI runs a short one
  fake_<service>.py       a fake device or service, when it's too big to live inside the test
  requirements.txt        what the tests need beyond Python, if they need anything
```

Every `test_*.py` is a plain script, not a pytest suite: run it with `python3` from the repository root, and it
exits non-zero if any check fails.

### The Marketplace

`hacs.json` at the root is the Marketplace's file: the name it lists and the oldest Home Assistant version the
integration works with. Keep that version in step with the README's requirements.

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/): a type, an optional scope, then a short summary in
the imperative.

```
feat: add a diagnostics download
fix: keep the last value when the service is briefly unreachable
refactor: split the coordinator's update into steps
docs: explain the safety settings
test: cover a reply with a missing field
chore: update the CI actions
```

## Releasing

Gitea is the main copy of this repository. It push-mirrors to GitHub, which is the public copy: the Marketplace
installs from GitHub's releases, so every link in the docs and release notes points there.

1. Change the version in all four places (the unit tests fail if they disagree, and so does the release):
   - `VERSION` in `custom_components/life_rpg/const.py`
   - `version` in `custom_components/life_rpg/manifest.json`
   - `const VERSION` in `custom_components/life_rpg/frontend/life-rpg.js`
   - the `?v=` on every `import` in `frontend/life-rpg.js` and `frontend/cast.js`

   The version is part of the panel's element name and of every script URL. That is what makes browsers and the
   Home Assistant app load the new panel instead of one they kept in memory.
2. Add the release to the top of [CHANGELOG.md](CHANGELOG.md), under a heading `## X.Y.Z (date)` (move what's under
   `## Unreleased` into it).
3. Run the checks above, including the 30-year run if the game changed.
4. Commit and push to Gitea, then publish with Gitea's **Release** workflow (`.gitea/workflows/release.yml`),
   either way:
   - **Actions → Release → Run workflow**, and enter the version without the `v` (for example `1.2.1`). It
     creates the tag `v1.2.1` on the commit it releases.
   - or push a version tag: `git tag v1.2.1 && git push origin v1.2.1`.

   The workflow checks the version matches all four places and `CHANGELOG.md` (`scripts/release_notes.py`), runs
   every check, builds `life_rpg.zip` and checks it installs as `custom_components/life_rpg/`
   (`scripts/build_package.py`), and publishes the release on Gitea with the zip and notes: install steps, then that
   version's changelog section (`scripts/publish_gitea_release.py`). A version with a suffix (`-beta`) is published
   as a pre-release. If any check fails, nothing is published. Running it again for the same version updates the
   release and replaces its zip.

5. Gitea's push mirror then sends the commits and the new tag to GitHub, where the tag starts GitHub's own
   **Release** workflow (`.github/workflows/release.yml`), which runs the same checks and publishes the same
   release there. The Marketplace picks it up from GitHub. If GitHub is down, the mirror catches up later; the Gitea
   release is already done.

The Gitea workflows use no actions (`actions/checkout` and the like download from GitHub): each job runs in a plain
image from Docker Hub (`python:3.14-bookworm`, and `node:20-bookworm` for the panel scripts) and fetches the code
from Gitea with git, so testing and releasing keep working when GitHub can't be reached. Only the tests' packages
(`tests/requirements.txt`) come from PyPI. When the runner's jobs can't reach Gitea at its public address (a runner
on the same Docker network as Gitea, say), set an Actions variable `GITEA_INTERNAL_URL` to the address they can
reach (`http://gitea-server:3000`); both workflows and the publish script use it.

Keep every tag on Gitea: the push mirror makes GitHub's tags match Gitea's, so a tag missing from Gitea is deleted on
GitHub, and the GitHub release on it turns into a draft.

## Reporting bugs

Open an issue with your Home Assistant version, the Life RPG version, what you did and what you expected.
The log helps: **Settings → System → Logs**, search for `life_rpg`. For painting problems, say which model type and
image-edit model you use; for LLM problems, which integration provides your AI Task entity.

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).
