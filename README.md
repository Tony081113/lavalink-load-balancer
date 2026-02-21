# lava-speed

`lava-speed` 是一個以非同步為核心的 Python 函式庫骨架，採用 Poetry 與 `pyproject.toml` 作為封裝標準。

## 專案結構

```text
.
├─ example.py
├─ src/
│  └─ lava_speed/
│     ├─ __init__.py
│     ├─ client.py
│     └─ node_manager.py
├─ tests/
│  ├─ test_client.py
│  └─ test_node_manager.py
├─ pyproject.toml
├─ requirements.txt
└─ .gitignore
```

## 安裝（Poetry）

```bash
poetry install
```

## 安裝（requirements.txt）

```bash
pip install -r requirements.txt
```

## 測試

```bash
poetry run pytest
```

## 範例

最簡單的執行範例在 `example.py`，示範：
- 取得套件版本 `__version__`
- 建立 `LavalinkNodeManager`
- 新增節點與更新節點統計
- 取得最佳節點

你也可以直接從套件根路徑匯入：

```python
from lava_speed import LavaSpeedClient, LavalinkNode, LavalinkNodeManager

client = LavaSpeedClient(base_url="https://example.com")
manager = LavalinkNodeManager()
node = LavalinkNode(identifier="node-1", host="127.0.0.1", port=2333)
```

```bash
poetry run python example.py
```