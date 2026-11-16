# Changelog

## 1.5.2 (2026-11-16)

### Paintings

- Removing an adventurer now cleans up its paintings too. Its portraits and base paintings, and the goddess and
  merchant as that adventurer had chosen them, used to stay in `/config/life_rpg/art` for good, because only a newer
  painting for the same adventurer replaced them; a new adventurer starts with new ones. Adding and removing
  adventurers while trying the game left a folder of portraits and goddesses nobody would see again.
- The rule from 1.5.1 now covers them: a portrait, goddess or merchant painting that hasn't been shown for a week of
  play is deleted, like gear you no longer have. Everything in use is shown on every refresh, and a goddess shared
  by two adventurers stays while either still shows her. Guardians (the bestiary keeps them) and the daily visitors
  (who take turns) are kept as before.

## 1.5.1 (2026-11-16)

### Paintings

- Paintings of gear you no longer have are now deleted. Every item that drops, and every item the market brings,
  gets its own painting, and before, those stayed in `/config/life_rpg/art` after the item was sold or the delivery
  left, until the folder reached its 1,500-picture cap. After a few months most of the Gallery's count was gear
  nobody would see again. Now an item painting that hasn't been shown for a week of play is deleted; your gear, the
  market's current stock and everything else on screen are shown on every refresh, so they're never touched.
- The week is counted from the newest painting shown, not the clock, so a Home Assistant that was off for a while
  keeps its paintings.
- Expect the count to drop the first time 1.5.1 starts; the space it frees is small (paintings are WebP).

## 1.5.0 (2026-11-16)

### The labyrinth

- You only go deeper by winning. A guardian still standing when the week ends now holds its floor: the next week
  you face the same guardian again (same name, trait and painting) instead of a fresh one, and the floor below stays
  shut until it falls. Before, the floor number stayed put but a brand-new guardian took over as if a new floor had
  opened, and losing cost nothing.
- Losing a week costs a small fine, the same size as a failed emergency: 30 + 2 gold per level, at most 200 and
  never more than 10% of your gold. No XP is taken, so levels and ranks never go backwards.
- The guardian comes back wounded, as before: its HP is set from your pace again and cut by 15% for each week in a
  row it has survived (up to four weeks).
- A new `guardian_returned` event (with the floor, the `attempt` number and the `fine` paid) replaces
  `guardian_appeared` for a repeated floor, with its own toast, phone notification in the example automation, and
  goddess lines. The Labyrinth tab shows which try you're on and what losing this week would cost.

## 1.4.0 (2026-11-15)

**Needs Home Assistant 2026.11 or newer.** The Marketplace only offers this version on 2026.11 and later; older
Home Assistant keeps 1.3.0.

- Built for Home Assistant 2026.11 alone: the code that kept older versions working is gone, and it runs on
  Python 3.14 like Home Assistant does.
- Assist tools follow Home Assistant's new tool format: each has a title, says which integration it comes from, and
  says what it does (looking things up, changing the game, or selling items for good), so conversation agents and
  tool approvals can tell them apart. A tool that fails now says so plainly instead of answering as if it worked.
- Renaming the achievements entity keeps it in place instead of removing it and adding it again.

## 1.3.0 (2026-11-15)

### The goddess

- She knows what time it is, and how long it's been since you last talked. Each message tells her the date and the
  time of day, and when your last conversation was: a moment ago she carries on where you left off; after hours,
  days or weeks she notices the gap and greets you like someone she hasn't seen for that long. The conversation she
  remembers is marked where time passed between talks. This works the same with your own conversation agent, the AI
  Task entity and through Assist. Lines said before this version have no time, so the first chat after updating
  starts without one.

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
