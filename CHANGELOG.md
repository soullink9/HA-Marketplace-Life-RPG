# Changelog

## Unreleased

### Repository

- Gitea is the main copy: its runner checks every push and publishes releases (`.gitea/workflows/`), with nothing
  downloaded from GitHub, so it keeps working when GitHub can't be reached. Gitea push-mirrors to GitHub, and every
  push from it publishes on GitHub the releases GitHub doesn't have yet, with the same files and notes, where the
  Marketplace installs from.
- The release helpers live in `scripts/` and are used by both: the version check and notes, building the zip, and
  publishing on Gitea. Every release's notes now start with how to install it.
- The release's zip is now always `life_rpg.zip` (it had the version in its name), so
  `.../releases/latest/download/life_rpg.zip` always gets the newest. Each zip is checked before it's published.

## 1.2.0 (2026-11-04)

- Moved to its own repository, [HA-Marketplace-Life-RPG](https://github.com/soullink9/HA-Marketplace-Life-RPG), so it can be installed and updated
  from the Home Assistant Marketplace (Home Assistant 2026.11 and newer). Installing by hand works as before.
- Lists its categories, so it shows up in the right place when browsing the Marketplace. No other changes to how
  the integration works.

## 1.1.1 (2026-11-02)

- No changes to the integration.

## 1.1.0 (2026-11-01)

- No changes to the integration.

## 1.0.2 (2026-11-01)

- No changes to the integration.

## 1.0.0 (2026-11-01)

Initial release.

- Daily quests from your phone's health sensors (steps, floors, sleep, water, bedtime), or logged by hand.
- Endless levels and ranks, eight jobs, skill proficiency, racial gifts that evolve, a weekly labyrinth guardian,
  daily choices, emergency, penalty and hidden quests, a bounty board with a kids mode for chores, chests and gear,
  titles, badges and devotion to a goddess.
- Gold and Marrow Fennick's market: three deliveries a day, consumables and cosmetics, and haggling that remembers you.
- Pixel art for everything, and optional paintings from your own ComfyUI (SDXL, Flux or a custom workflow), with an
  optional image-edit model (Flux Kontext or Qwen Image Edit) that keeps characters consistent.
- Optional words from your own LLM through Home Assistant's AI Task: talk to the goddess, haggle in your own words,
  written mornings, side quests, item lore and a weekly chronicle; and a Life RPG toolset for Assist.
- The System panel, dashboard cards, sensors, an achievements event entity, one-tap logging buttons and actions.
