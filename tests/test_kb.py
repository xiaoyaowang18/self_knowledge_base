from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "kb.py"
SPEC = importlib.util.spec_from_file_location("kb", MODULE_PATH)
assert SPEC and SPEC.loader
kb = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = kb
SPEC.loader.exec_module(kb)


NOTE_BODY = """# 示例

## 一句话结论

结论。

## 核心信息

- 信息。

## 我的判断

判断。

## 可用场景

- 场景。

## 证据与限制

- 限制。
"""


class KnowledgeBaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for directory in kb.DOCUMENT_DIRS + ("raw",):
            (self.root / directory).mkdir(parents=True, exist_ok=True)
        (self.root / "raw" / "source-a.md").write_text("source a", encoding="utf-8")
        (self.root / "raw" / "source-b.md").write_text("source b", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_note(
        self,
        name: str,
        note_id: str,
        title: str,
        source_ref: str,
        source_url: str,
        content_hash: str,
        tags: list[str],
        related: list[str] | None = None,
    ) -> Path:
        path = self.root / "notes" / name
        document = kb.Document(
            path,
            {
                "id": note_id,
                "type": "source_note",
                "title": title,
                "created_at": "2026-08-20T12:00:00+08:00",
                "updated_at": "2026-08-20T12:00:00+08:00",
                "source_type": "web",
                "source_ref": source_ref,
                "source_url": source_url,
                "content_hash": content_hash,
                "tags": tags,
                "related": related or [],
                "status": "active",
            },
            NOTE_BODY,
        )
        kb.write_document(document)
        return path

    def test_normalize_url_removes_tracking_and_fragment(self) -> None:
        value = kb.normalize_url("HTTPS://Example.COM:443/path/?utm_source=x&b=2&a=1#part")
        self.assertEqual(value, "https://example.com/path?a=1&b=2")

    def test_normalize_url_does_not_crash_on_invalid_port(self) -> None:
        value = kb.normalize_url("https://example.com:bad/path")
        self.assertEqual(value, "https://example.com:bad/path")

    def test_sync_is_idempotent_and_writes_bidirectional_relations(self) -> None:
        left = self.write_note(
            "2026-08-20-left.md",
            "note-20260820-left",
            "AI 知识库的本地存储",
            "raw/source-a.md",
            "https://example.com/a",
            "a" * 64,
            ["knowledge-base", "local-first", "writing"],
        )
        right = self.write_note(
            "2026-08-20-right.md",
            "note-20260820-right",
            "个人知识库为什么本地优先",
            "raw/source-b.md",
            "https://example.com/b",
            "b" * 64,
            ["knowledge-base", "local-first", "architecture"],
        )

        changed, index_changed, issues = kb.run_sync(self.root)
        self.assertEqual(changed, 2)
        self.assertTrue(index_changed)
        self.assertEqual(issues, [])
        self.assertEqual(kb.read_document(left).meta["related"], ["note-20260820-right"])
        self.assertEqual(kb.read_document(right).meta["related"], ["note-20260820-left"])

        snapshot = {path: path.read_text(encoding="utf-8") for path in (left, right, self.root / "INDEX.md")}
        changed, index_changed, issues = kb.run_sync(self.root)
        self.assertEqual(changed, 0)
        self.assertFalse(index_changed)
        self.assertEqual(issues, [])
        self.assertEqual(snapshot, {path: path.read_text(encoding="utf-8") for path in snapshot})

    def test_validate_detects_duplicate_normalized_url(self) -> None:
        self.write_note(
            "2026-08-20-left.md",
            "note-20260820-left",
            "标题一",
            "raw/source-a.md",
            "https://example.com/post?utm_source=a",
            "a" * 64,
            ["tag-one"],
        )
        self.write_note(
            "2026-08-20-right.md",
            "note-20260820-right",
            "标题二",
            "raw/source-b.md",
            "https://example.com/post",
            "b" * 64,
            ["tag-two"],
        )
        kb.write_index(self.root)
        issues = kb.validate_root(self.root)
        self.assertTrue(any("来源 URL" in issue and "重复" in issue for issue in issues))

    def test_validate_detects_one_way_relation(self) -> None:
        self.write_note(
            "2026-08-20-left.md",
            "note-20260820-left",
            "标题一",
            "raw/source-a.md",
            "https://example.com/a",
            "a" * 64,
            ["tag-one"],
            ["note-20260820-right"],
        )
        self.write_note(
            "2026-08-20-right.md",
            "note-20260820-right",
            "标题二",
            "raw/source-b.md",
            "https://example.com/b",
            "b" * 64,
            ["tag-two"],
        )
        kb.write_index(self.root)
        issues = kb.validate_root(self.root)
        self.assertTrue(any("关联不是双向" in issue for issue in issues))

    def test_search_ranks_title_match(self) -> None:
        self.write_note(
            "2026-08-20-left.md",
            "note-20260820-left",
            "本地知识库架构",
            "raw/source-a.md",
            "https://example.com/a",
            "a" * 64,
            ["local-first"],
        )
        results = kb.search(self.root, "知识库")
        self.assertEqual(results[0][1].meta["id"], "note-20260820-left")

    def test_full_note_wiki_brief_structure_validates(self) -> None:
        first = self.write_note(
            "2026-08-20-left.md",
            "note-20260820-left",
            "本地知识库架构",
            "raw/source-a.md",
            "https://example.com/a",
            "a" * 64,
            ["knowledge-base", "local-first"],
        )
        second = self.write_note(
            "2026-08-20-right.md",
            "note-20260820-right",
            "个人知识库本地优先",
            "raw/source-b.md",
            "https://example.com/b",
            "b" * 64,
            ["knowledge-base", "local-first"],
        )
        topic = kb.Document(
            self.root / "wiki" / "topics" / "personal-knowledge-base.md",
            {
                "id": "topic-personal-knowledge-base",
                "type": "topic",
                "title": "个人知识库",
                "updated_at": "2026-08-20T12:00:00+08:00",
                "source_notes": ["note-20260820-left", "note-20260820-right"],
                "contradictions": [],
                "status": "active",
            },
            """# 个人知识库

## 当前结论
本地优先。
## 支持证据
- 两篇笔记。
## 反例或矛盾
- 暂无。
## 仍待确认的问题
- 规模上限。
## 可用于哪些内容
- 架构文章。
""",
        )
        kb.write_document(topic)
        brief = kb.Document(
            self.root / "briefs" / "2026-08-20-local-first.md",
            {
                "id": "brief-20260820-local-first",
                "type": "brief",
                "title": "个人知识库为什么应当本地优先",
                "created_at": "2026-08-20T12:00:00+08:00",
                "source_pages": ["topic-personal-knowledge-base", "note-20260820-left"],
                "status": "draft",
            },
            """# 选题

## 核心角度
复杂方案未必更好。
## 目标读者
个人写作者。
## 为什么现在写
AI 编程降低了实现门槛。
## 关键证据
- 主题页和笔记。
## 文章结构建议
1. 问题。
## 下一步动作
- 补一个真实案例。
""",
        )
        kb.write_document(brief)

        _, _, issues = kb.run_sync(self.root)
        self.assertEqual(issues, [])
        index = (self.root / "INDEX.md").read_text(encoding="utf-8")
        self.assertIn("个人知识库为什么应当本地优先", index)
        self.assertIn("topic-personal-knowledge-base", topic.meta["id"])
        self.assertTrue(first.exists() and second.exists())


if __name__ == "__main__":
    unittest.main()
