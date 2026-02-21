import pytest

from lava_speed.node_manager import LavalinkNode, LavalinkNodeManager


@pytest.mark.asyncio
async def test_get_best_node_skips_disconnected_nodes() -> None:
    manager = LavalinkNodeManager()

    node_a = LavalinkNode(identifier="a", host="127.0.0.1", port=2333)
    node_b = LavalinkNode(identifier="b", host="127.0.0.1", port=2444)

    await manager.add_node(node_a)
    await manager.add_node(node_b)

    await manager.update_node_stats(
        "a",
        '{"stats":{"cpu":{"lavalinkLoad":0.25},"playingPlayers":10,"memory":{"used":1024},"uptime":99}}',
    )
    await manager.update_node_stats("b", {"cpu": {"lavalinkLoad": 0.10}, "playingPlayers": 20})

    best = await manager.get_best_node()
    assert best is not None
    assert best.identifier == "a"
    assert best.stats.memory_used == 1024
    assert best.stats.uptime == 99

    await manager.mark_disconnected("a")
    best_after_disconnect = await manager.get_best_node()

    assert best_after_disconnect is not None
    assert best_after_disconnect.identifier == "b"


@pytest.mark.asyncio
async def test_invalid_stats_marks_node_disconnected() -> None:
    manager = LavalinkNodeManager()
    node = LavalinkNode(identifier="x", host="127.0.0.1", port=2333)

    await manager.add_node(node)
    await manager.update_node_stats("x", '{"stats":{"cpu":"invalid","playingPlayers":3}}')

    best = await manager.get_best_node()
    assert best is None


@pytest.mark.asyncio
async def test_score_uses_double_player_weight() -> None:
    manager = LavalinkNodeManager()

    node_a = LavalinkNode(identifier="a", host="127.0.0.1", port=2333)
    node_b = LavalinkNode(identifier="b", host="127.0.0.1", port=2444)

    await manager.add_node(node_a)
    await manager.add_node(node_b)

    await manager.update_node_stats("a", {"cpu": {"lavalinkLoad": 0.10}, "playingPlayers": 5})
    await manager.update_node_stats("b", {"cpu": {"lavalinkLoad": 0.08}, "playingPlayers": 7})

    best = await manager.get_best_node()
    assert best is not None
    assert best.identifier == "a"
