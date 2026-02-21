from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

import ujson


@dataclass(slots=True)
class NodeCPUStats:
    lavalink_load: float = 1.0


@dataclass(slots=True)
class NodeStats:
    cpu: NodeCPUStats = field(default_factory=NodeCPUStats)
    playing_players: int = 0
    memory_used: int = 0
    uptime: int = 0


@dataclass(slots=True)
class LavalinkNode:
    identifier: str
    host: str
    port: int
    connected: bool = True
    stats: NodeStats = field(default_factory=NodeStats)


class LavalinkNodeManager:
    def __init__(self) -> None:
        self._nodes: dict[str, LavalinkNode] = {}
        self._lock = asyncio.Lock()

    async def add_node(self, node: LavalinkNode) -> None:
        async with self._lock:
            self._nodes[node.identifier] = node

    async def remove_node(self, identifier: str) -> None:
        async with self._lock:
            self._nodes.pop(identifier, None)

    async def mark_disconnected(self, identifier: str) -> None:
        async with self._lock:
            node = self._nodes.get(identifier)
            if node is not None:
                node.connected = False

    async def update_node_stats(self, identifier: str, payload: dict[str, Any] | str) -> None:
        async with self._lock:
            node = self._nodes.get(identifier)
            if node is None:
                return

            try:
                normalized_stats = self._normalize_stats_payload(payload)
                cpu_stats = normalized_stats.get("cpu", {})
                memory_stats = normalized_stats.get("memory", {})

                if not isinstance(cpu_stats, dict) or not isinstance(memory_stats, dict):
                    raise TypeError("Nested stats fields must be dictionaries")

                load = float(cpu_stats.get("lavalinkLoad", 0.0))
                players = int(normalized_stats.get("playingPlayers", 0))
                memory_used = int(memory_stats.get("used", 0))
                uptime = int(normalized_stats.get("uptime", 0))

                node.stats.cpu.lavalink_load = max(load, 0.0)
                node.stats.playing_players = max(players, 0)
                node.stats.memory_used = max(memory_used, 0)
                node.stats.uptime = max(uptime, 0)
                node.connected = True
            except (KeyError, TypeError, ValueError):
                node.connected = False

    async def get_best_node(self) -> LavalinkNode | None:
        async with self._lock:
            best_node: LavalinkNode | None = None
            best_score = float("inf")

            for node in self._nodes.values():
                if not node.connected:
                    continue

                try:
                    score = self._score(node)
                except (TypeError, ValueError):
                    node.connected = False
                    continue

                if score < best_score:
                    best_score = score
                    best_node = node

            return best_node

    @staticmethod
    def _score(node: LavalinkNode) -> float:
        load = float(node.stats.cpu.lavalink_load)
        players = int(node.stats.playing_players)

        if load < 0 or players < 0:
            raise ValueError("Node stats must be non-negative")

        return (load * 100.0) + (players * 2.0)

    @staticmethod
    def _normalize_stats_payload(payload: dict[str, Any] | str) -> dict[str, Any]:
        if isinstance(payload, str):
            decoded = ujson.loads(payload)
            if not isinstance(decoded, dict):
                raise TypeError("Decoded stats payload must be a dictionary")
            return decoded.get("stats", {})

        if not isinstance(payload, dict):
            raise TypeError("Stats payload must be a dictionary or JSON string")

        stats = payload.get("stats")
        if isinstance(stats, dict):
            return stats

        return payload