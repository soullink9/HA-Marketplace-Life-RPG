What's on each tab of the System panel, the dashboard card, the example automations, and every entity and event the integration creates.

## Screens
**The System panel** has ten tabs (the tab bar wraps onto two rows on a phone):
- **Status:** your adventurer in their gear, level, rank, HP and MP, job, race, attributes, skills, active bonuses and where they come from, today's episode title and the goddess's line.
- **Quests:** the daily choice, the daily quests, emergency and penalty windows with timers, and the bounty board.
- **Labyrinth:** this week's guardian, floor trait, depth, creature tally and bestiary.
- **Inventory:** paper doll with six slots, chests, items, enhance, sell and salvage.
- **Market:** Marrow Fennick, the current stock, haggling, your bag of consumables and your wardrobe.
- **Class:** all eight jobs with their levels, passives and skills, plus skill proficiency.
- **Records:** badges, and the titles and hidden quests you've earned.
- **Goddess:** her portrait, devotion and blessings, a chat with her, and your racial gift tree.
- **Log:** 30-day chart, the weekly chronicle and the System log.
- **Gallery** (while paintings are on): every painting with its Repaint, and the choices for you, the goddess and Marrow.

If several adventurers exist, switch between them at the top; you can only act for your own (admins can act for anyone).

**Cards:** `type: custom:life-rpg-card` with `view: compact | status | quests | labyrinth` and an optional `adventurer: Name`. Tapping a card opens the panel. [`examples/dashboard.yaml`](../examples/dashboard.yaml) has a ready view.

**Phone notifications:** the [`examples/automations/`](../examples/automations) folder has one automation per file, each pasted straight into the automation editor (nothing goes in the config folder, no packages or `!secret`), for Home Assistant 2026.11 and newer:
- [System notifications](../examples/automations/life_rpg_notifications.yaml): emergencies and their fines, penalty quests, choices, level and rank ups, guardians (including one that survived its week and returns, with the try number and the gold the loss cost), jobs, skills, hidden quests, evolutions, titles and more.
- [Secure your streak](../examples/automations/life_rpg_streak_nudge.yaml): at 8 pm, if today isn't cleared, what's still doable (or how many quests the penalty quest needs).
- [Guardian within reach](../examples/automations/life_rpg_guardian_push.yaml): Sunday at 5 pm, if the guardian has 25% HP or less, the reward for felling it and what losing the week would cost.
- [Goddess good morning](../examples/automations/life_rpg_goddess_morning.yaml): her good-morning message as soon as she writes it (needs written flavour on).
- [Chore waiting for approval](../examples/automations/life_rpg_chore_approval.yaml): kids mode, tells a parent when a child marks a chore done.

To add one: **Settings → Automations & scenes → Create automation → Create new automation → ⋮ → Edit in YAML**, select everything, paste the file's contents over it, change `notify.mobile_app_your_phone` and the `user_` prefix (or switch to the visual editor and pick them), and save. You can rename the achievements entity in its settings and the automation follows if you pick it again; renaming no longer removes and re-adds it. Paintings clean up after themselves (gear, portraits and goddesses unseen for a week of play), so no automation is needed to tidy `/config/life_rpg/art`.

## Entities (adventurer "User")
`sensor.user_level`, `_level_progress`, `_xp`, `_xp_today`, `_streak`, `_rank`, `_job`, `_title`, `_race`, `_labyrinth` (guardian HP left, %), `_daily_choice`, `_gold` (with your bag and the merchant's mood as attributes), `_chests`, `_emergency_quest`, `_devotion`, one attribute sensor per quest (`_stamina` … with its skill as attributes) and one quest sensor per quest (`_stamina_quest` …). `sensor.user_devotion` carries the goddess's `morning_message` once it's written each day, handy for a daily briefing.

`event.user_achievements` fires every event:
- `level_up`, `rank_up`, `attribute_up`, `skill_up`
- `quest_complete`, `day_cleared`, `perfect_day`, `streak_milestone`, `personal_record`, `reading_held`
- `job_change`, `job_level`, `race_evolved`
- `title_earned`, `badge_earned`, `hidden_quest`
- `emergency_quest`, `emergency_cleared`, `emergency_failed`, `emergency_declined` (with `fine`, `excused` and, for failures, `why`: work, late or off)
- `penalty_quest`, `penalty_cleared`, `streak_broken`, `shield_earned`, `shield_used`
- `guardian_appeared`, `guardian_defeated`, `guardian_returned` (a guardian that survived its week holds the floor: with `attempt` and the `fine` paid)
- `choice_offered`, `choice_won`, `choice_lost`
- `bounty_claimed`, `bounty_done`
- `chest_dropped`, `devotion_up`, `bargain_struck`, `market_restocked`, `goddess_gift`

Events that pay gold carry a `gold` attribute.