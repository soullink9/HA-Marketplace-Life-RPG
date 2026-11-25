"""Websocket API for the System panel and cards.

life_rpg/players    every adventurer in the house (party view), flagged `mine` for the caller
life_rpg/subscribe  live game view for one adventurer (anyone may watch)
life_rpg/action     open chests, equip gear, pick a title... (own adventurer, or admins)
"""

from typing import Any

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
import probatio

from .const import DOMAIN, VERSION
from .coordinator import LifeRPGCoordinator
from .engine.rules import GameError


@callback
def async_register(hass: HomeAssistant) -> None:
    """Register the commands."""
    websocket_api.async_register_command(hass, ws_players)
    websocket_api.async_register_command(hass, ws_subscribe)
    websocket_api.async_register_command(hass, ws_action)
    websocket_api.async_register_command(hass, ws_chat)


def _coordinators(hass: HomeAssistant) -> list[LifeRPGCoordinator]:
    """Every loaded adventurer's coordinator."""
    return [e.runtime_data for e in hass.config_entries.async_loaded_entries(DOMAIN)]


def _get(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> LifeRPGCoordinator | None:
    """The coordinator the message asks for, or None after sending a not_found error."""
    coordinator = next((c for c in _coordinators(hass) if c.config_entry.entry_id == msg["entry_id"]), None)
    if coordinator is None or coordinator.data is None:
        connection.send_error(msg["id"], "not_found", "No such adventurer.")
        return None
    return coordinator


@websocket_api.websocket_command({probatio.Required("type"): "life_rpg/players"})
@callback
def ws_players(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    """List adventurers for the party screen."""
    players = []
    for c in _coordinators(hass):
        d = c.data or {}
        players.append(
            {
                "entry_id": c.config_entry.entry_id,
                "name": c.config_entry.title,
                "mine": c.user_id == connection.user.id,
                "linked": bool(c.user_id),
                "race": d.get("race", {}).get("name"),
                "level": d.get("level"),
                "rank": d.get("rank"),
                "job": (d.get("job") or {}).get("title"),
                "streak": d.get("streak"),
                "floor": (d.get("labyrinth") or {}).get("floor"),
                "title": (d.get("title") or {}).get("name"),
            }
        )
    connection.send_result(msg["id"], {"players": players, "is_admin": connection.user.is_admin})


@websocket_api.websocket_command({probatio.Required("type"): "life_rpg/subscribe", probatio.Required("entry_id"): str})
@callback
def ws_subscribe(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    """Stream an adventurer's game view; every update carries the events it raised."""
    if (coordinator := _get(hass, connection, msg)) is None:
        return
    can_act = connection.user.is_admin or coordinator.user_id == connection.user.id

    @callback
    def send() -> None:
        """Send the current view (without private chats for people who may only watch)."""
        view = coordinator.data
        if not can_act and view:  # watchers see the game, not private conversations
            view = {**view, "lune_chat": [], "market": {**view["market"], "chat": []} if view.get("market") else None}
        connection.send_event(
            msg["id"],
            {
                "view": view,
                "name": coordinator.config_entry.title,
                "can_act": can_act,
                "parent": bool(connection.user.is_admin),
                "version": VERSION,
            },
        )

    connection.subscriptions[msg["id"]] = coordinator.async_add_listener(send)
    connection.send_result(msg["id"])
    send()


@websocket_api.websocket_command(
    {
        probatio.Required("type"): "life_rpg/action",
        probatio.Required("entry_id"): str,
        probatio.Required("action"): str,
        probatio.Optional("chest_id"): int,
        probatio.Optional("item_id"): int,
        probatio.Optional("slot"): str,
        probatio.Optional("title"): probatio.Any(str, None),
        probatio.Optional("job"): str,
        probatio.Optional("accept"): bool,
        probatio.Optional("stock_id"): int,
        probatio.Optional("offer"): probatio.All(int, probatio.Range(min=0)),
        probatio.Optional("consumable"): str,
        probatio.Optional("category"): str,
        probatio.Optional("cosmetic"): probatio.Any(str, None),
        probatio.Optional("quest"): str,
        probatio.Optional("amount"): probatio.All(probatio.Coerce(float), probatio.Range(min=-5000, max=5000)),
        probatio.Optional("url"): probatio.All(str, probatio.Length(max=300)),
        probatio.Optional("today"): probatio.Any(
            None, probatio.All(probatio.Coerce(float), probatio.Range(min=0, max=100000))
        ),
        probatio.Optional("record"): probatio.Any(
            None, probatio.All(probatio.Coerce(float), probatio.Range(min=0, max=100000))
        ),
        probatio.Optional("bedtime"): probatio.All(str, probatio.Length(max=40)),
        probatio.Optional("wake"): probatio.All(str, probatio.Length(max=40)),
        probatio.Optional("prefs"): probatio.Schema(
            {
                probatio.Optional(k): probatio.Any(None, probatio.All(str, probatio.Length(max=40)))
                for k in (
                    "race",
                    "age",
                    "framing",
                    "hair",
                    "fur",
                    "hairstyle",
                    "eyes",
                    "build",
                    "weapon",
                    "outfit",
                    "accessory",
                    "backdrop",
                )
            }
        ),
        probatio.Optional("bounty_id"): int,
        probatio.Optional("xp"): probatio.All(probatio.Coerce(int), probatio.Range(min=0, max=1000)),
        probatio.Optional("gold"): probatio.All(probatio.Coerce(int), probatio.Range(min=0, max=1000)),
        probatio.Optional("chest"): bool,
        probatio.Optional("repeat"): probatio.In(["once", "daily", "weekly"]),
        probatio.Optional("ok"): bool,
    }
)
@websocket_api.async_response
async def ws_action(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    """Perform an action for an adventurer you own (admins may act for anyone)."""
    if (coordinator := _get(hass, connection, msg)) is None:
        return
    if not (connection.user.is_admin or coordinator.user_id == connection.user.id):
        connection.send_error(msg["id"], "unauthorized", "That isn't your adventurer.")
        return
    args = {
        k: msg[k]
        for k in (
            "chest_id",
            "item_id",
            "slot",
            "title",
            "job",
            "accept",
            "stock_id",
            "offer",
            "consumable",
            "category",
            "cosmetic",
            "quest",
            "amount",
            "bedtime",
            "wake",
            "today",
            "record",
            "url",
            "prefs",
            "bounty_id",
            "xp",
            "gold",
            "chest",
            "repeat",
            "ok",
        )
        if k in msg
    }
    try:
        result = await coordinator.async_action(msg["action"], _admin=connection.user.is_admin, **args)
    except (GameError, KeyError, ValueError) as err:
        connection.send_error(msg["id"], "game_error", str(err))
        return
    connection.send_result(msg["id"], {"result": result})


@websocket_api.websocket_command(
    {
        probatio.Required("type"): "life_rpg/chat",
        probatio.Required("entry_id"): str,
        probatio.Required("who"): probatio.In(["lune", "merchant"]),
        probatio.Required("text"): probatio.All(str, probatio.Length(min=1, max=500)),
        probatio.Optional("stock_id"): probatio.Any(int, None),
    }
)
@websocket_api.async_response
async def ws_chat(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    """Talk to Lune or haggle with the merchant (your own adventurer, or any as an admin)."""
    if (coordinator := _get(hass, connection, msg)) is None:
        return
    if not (connection.user.is_admin or coordinator.user_id == connection.user.id):
        connection.send_error(msg["id"], "unauthorized", "That isn't your adventurer.")
        return
    try:
        result = await coordinator.async_chat(msg["who"], msg["text"], msg.get("stock_id"))
    except (GameError, HomeAssistantError) as err:
        connection.send_error(msg["id"], "chat_error", str(err))
        return
    connection.send_result(msg["id"], result)
