from __future__ import annotations

import asyncio

from lava_speed import __version__, LavalinkNode, LavalinkNodeManager


async def main() -> None:
    manager = LavalinkNodeManager()

    await manager.add_node(LavalinkNode(identifier="node-a", host="127.0.0.1", port=2333))
    await manager.add_node(LavalinkNode(identifier="node-b", host="127.0.0.1", port=2444))

    await manager.update_node_stats(
        "node-a",
        {
            "stats": {
                "cpu": {"lavalinkLoad": 0.25},
                "playingPlayers": 5,
                "memory": {"used": 120_000_000},
                "uptime": 1_800_000,
            }
        },
    )
    await manager.update_node_stats(
        "node-b",
        {
            "stats": {
                "cpu": {"lavalinkLoad": 0.10},
                "playingPlayers": 2,
                "memory": {"used": 90_000_000},
                "uptime": 3_600_000,
            }
        },
    )

    best = await manager.get_best_node()

    print(f"lava-speed version: {__version__}")
    if best is None:
        print("No available nodes")
        return

    print(f"Best node: {best.identifier} ({best.host}:{best.port})")


if __name__ == "__main__":
    asyncio.run(main())