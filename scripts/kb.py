#!/usr/bin/env python3
"""Deterministic maintenance commands for the local Markdown knowledge base."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCUMENT_DIRS = ("notes", "wiki/topics", "wiki/entities", "briefs")
NOTE_TYPES = {"source_note", "idea_note"}
WIKI_TYPES = {"topic", "entity"}
TRACKING_PARAMS = {"fbclid", "gclid", "mc_cid", "mc_eid"}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
LATIN_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9-]{1,}")
CJK_RUN_RE = re.compile(r"[\u3400-\u9fff]+")
TITLE_STOPWORDS = {
    "一个",
    "个人",
    "为什么",
    "什么",
    "如何",
    "怎么",
    "这个",
    "知识",
    "系统",
    "工具",
    "产品",
}

REQUIRED_FIELDS = {
    "source_note": {
        "id",
        "type",
        "title",
        "created_at",
        "updated_at",
        "source_type",
        "source_ref",
        "source_url",
        "content_hash",
        "tags",
        "related",
        "status",
    },
    "idea_note": {
        "id",
        "type",
        "title",
        "created_at",
        "updated_at",
        "source_type",
        "source_ref",
        "source_url",
        "content_hash",
        "tags",
        "related",
        "status",
    },
    "topic": {"id", "type", "title", "updated_at", "source_notes", "contradictions", "status"},
    "entity": {"id", "type", "title", "updated_at", "source_notes", "contradictions", "status"},
    "brief": {"id", "type", "title", "created_at", "source_pages", "status"},
}

REQUIRED_HEADINGS = {
    "source_note": ("一句话结论", "核心信息", "我的判断", "可用场景", "证据与限制"),
    "idea_note": ("一句话结论", "核心信息", "我的判断", "可用场景", "证据与限制"),
    "topic": ("当前结论", "支持证据", "反例或矛盾", "仍待确认的问题", "可用于哪些内容"),
    "entity": ("当前结论", "支持证据", "反例或矛盾", "仍待确认的问题", "可用于哪些内容"),
    "brief": ("核心角度", "目标读者", "为什么现在写", "关键证据", "文章结构建议", "下一步动作"),
}


@dataclass
class Document:
    path: Path
    meta: dict[str, Any]
    body: str


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value == "[]":
        return []
    if value in {"true", "false"}:
        return value == "true"
    if value == "null":
        return None
    if value.startswith('"') and value.endswith('"'):
        return json.loads(value)
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def parse_frontmatter(text: str, path: Path) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: 缺少 YAML frontmatter")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError(f"{path}: frontmatter 未闭合") from exc

    meta: dict[str, Any] = {}
    current_list: str | None = None
    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - "):
            if current_list is None:
                raise ValueError(f"{path}:{line_number}: 列表项没有对应字段")
            meta[current_list].append(parse_scalar(line[4:]))
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            raise ValueError(f"{path}:{line_number}: 只支持简单键值和列表")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        if key in meta:
            raise ValueError(f"{path}:{line_number}: 字段 {key} 重复")
        if raw_value.strip() == "":
            meta[key] = []
            current_list = key
        else:
            meta[key] = parse_scalar(raw_value)
            current_list = None

    body = "\n".join(lines[end + 1 :]).lstrip("\n")
    return meta, body


def dump_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    return json.dumps(str(value), ensure_ascii=False)


def render_document(meta: dict[str, Any], body: str) -> str:
    lines = ["---"]
    for key, value in meta.items():
        if isinstance(value, list):
            if value:
                lines.append(f"{key}:")
                lines.extend(f"  - {dump_scalar(item)}" for item in value)
            else:
                lines.append(f"{key}: []")
        else:
            lines.append(f"{key}: {dump_scalar(value)}")
    lines.extend(("---", "", body.rstrip(), ""))
    return "\n".join(lines)


def read_document(path: Path) -> Document:
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"), path)
    return Document(path=path, meta=meta, body=body)


def write_document(document: Document) -> bool:
    content = render_document(document.meta, document.body)
    old = document.path.read_text(encoding="utf-8") if document.path.exists() else None
    if old == content:
        return False
    document.path.parent.mkdir(parents=True, exist_ok=True)
    document.path.write_text(content, encoding="utf-8")
    return True


def iter_document_paths(root: Path) -> Iterable[Path]:
    for directory in DOCUMENT_DIRS:
        base = root / directory
        if base.exists():
            yield from sorted(base.rglob("*.md"))


def load_documents(root: Path) -> tuple[list[Document], list[str]]:
    documents: list[Document] = []
    errors: list[str] = []
    for path in iter_document_paths(root):
        try:
            documents.append(read_document(path))
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
    return documents, errors


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return ""
    parts = urlsplit(url)
    if not parts.scheme or not parts.netloc:
        return url
    scheme = parts.scheme.lower()
    host = (parts.hostname or "").lower()
    try:
        port = parts.port
    except ValueError:
        return url
    if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
        host = f"{host}:{port}"
    path = parts.path or "/"
    if path != "/":
        path = path.rstrip("/")
    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in TRACKING_PARAMS
    ]
    return urlunsplit((scheme, host, path, urlencode(sorted(query)), ""))


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def title_tokens(title: str) -> set[str]:
    lowered = title.lower()
    tokens = set(LATIN_TOKEN_RE.findall(lowered))
    for run in CJK_RUN_RE.findall(lowered):
        if len(run) == 2:
            tokens.add(run)
        elif len(run) > 2:
            tokens.update(run[index : index + 2] for index in range(len(run) - 1))
    return {token for token in tokens if token not in TITLE_STOPWORDS}


def relation_score(left: Document, right: Document) -> tuple[int, list[str], list[str]]:
    left_tags = {str(tag).strip().lower() for tag in left.meta.get("tags", []) if str(tag).strip()}
    right_tags = {str(tag).strip().lower() for tag in right.meta.get("tags", []) if str(tag).strip()}
    shared_tags = sorted(left_tags & right_tags)
    shared_title = sorted(title_tokens(str(left.meta.get("title", ""))) & title_tokens(str(right.meta.get("title", ""))))
    score = len(shared_tags) * 2 + min(2, len(shared_title))
    return score, shared_tags, shared_title


def update_relations(root: Path, threshold: int = 4, dry_run: bool = False) -> tuple[int, list[tuple[str, str, int, list[str], list[str]]]]:
    documents, errors = load_documents(root)
    if errors:
        raise ValueError("\n".join(errors))
    notes = [doc for doc in documents if doc.meta.get("type") in NOTE_TYPES and doc.meta.get("status") == "active"]
    expected: dict[str, set[str]] = {str(doc.meta.get("id", "")): set() for doc in notes}
    candidates: list[tuple[str, str, int, list[str], list[str]]] = []

    for index, left in enumerate(notes):
        left_id = str(left.meta.get("id", ""))
        if not left_id:
            continue
        for right in notes[index + 1 :]:
            right_id = str(right.meta.get("id", ""))
            if not right_id:
                continue
            score, shared_tags, shared_title = relation_score(left, right)
            if score >= threshold:
                expected[left_id].add(right_id)
                expected[right_id].add(left_id)
                candidates.append((left_id, right_id, score, shared_tags, shared_title))

    changed = 0
    for note in notes:
        note_id = str(note.meta.get("id", ""))
        wanted = sorted(expected.get(note_id, set()))
        current = sorted(str(value) for value in note.meta.get("related", []))
        if current != wanted:
            changed += 1
            if not dry_run:
                note.meta["related"] = wanted
                write_document(note)
    return changed, candidates


def markdown_link(root: Path, document: Document) -> str:
    relative = document.path.relative_to(root).as_posix()
    title = str(document.meta.get("title", document.path.stem)).replace("[", "\\[").replace("]", "\\]")
    return f"[{title}]({relative})"


def build_index(root: Path, documents: list[Document] | None = None) -> str:
    if documents is None:
        documents, _ = load_documents(root)
    active = [doc for doc in documents if doc.meta.get("status") != "archived"]

    def sort_key(document: Document) -> tuple[str, str]:
        updated = str(document.meta.get("updated_at") or document.meta.get("created_at") or "")
        return updated, str(document.meta.get("title", ""))

    groups = {
        "主题": sorted((doc for doc in active if doc.meta.get("type") == "topic"), key=sort_key, reverse=True),
        "实体": sorted((doc for doc in active if doc.meta.get("type") == "entity"), key=sort_key, reverse=True),
        "笔记": sorted((doc for doc in active if doc.meta.get("type") in NOTE_TYPES), key=sort_key, reverse=True),
        "选题": sorted((doc for doc in active if doc.meta.get("type") == "brief"), key=sort_key, reverse=True),
    }

    lines = ["# 知识库索引", "", "> 此文件由 `python3 scripts/kb.py index` 生成，请勿手工编辑。", ""]
    for heading, items in groups.items():
        lines.extend((f"## {heading}", ""))
        if items:
            for document in items:
                date = str(document.meta.get("updated_at") or document.meta.get("created_at") or "")[:10]
                suffix = f"（{date}）" if date else ""
                lines.append(f"- {markdown_link(root, document)}{suffix}")
        else:
            lines.append("- 暂无。")
        lines.append("")

    tags: dict[str, list[Document]] = defaultdict(list)
    for document in groups["笔记"]:
        for tag in document.meta.get("tags", []):
            value = str(tag).strip()
            if value:
                tags[value].append(document)
    lines.extend(("## 标签", ""))
    if tags:
        for tag in sorted(tags):
            lines.extend((f"### {tag}", ""))
            lines.extend(f"- {markdown_link(root, document)}" for document in tags[tag])
            lines.append("")
    else:
        lines.extend(("- 暂无。", ""))
    return "\n".join(lines)


def write_index(root: Path, check_only: bool = False) -> bool:
    expected = build_index(root)
    path = root / "INDEX.md"
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    changed = current != expected
    if changed and not check_only:
        path.write_text(expected, encoding="utf-8")
    return changed


def valid_iso_datetime(value: Any) -> bool:
    try:
        datetime.fromisoformat(str(value))
        return True
    except ValueError:
        return False


def inside_root(root: Path, relative: str) -> Path | None:
    if not relative or Path(relative).is_absolute():
        return None
    target = (root / relative).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return None
    return target


def validate_root(root: Path, check_index: bool = True) -> list[str]:
    documents, errors = load_documents(root)
    issues = list(errors)
    ids: dict[str, Document] = {}
    normalized_urls: dict[str, Document] = {}
    content_hashes: dict[str, Document] = {}

    for document in documents:
        relative = document.path.relative_to(root).as_posix()
        doc_type = str(document.meta.get("type", ""))
        required = REQUIRED_FIELDS.get(doc_type)
        if required is None:
            issues.append(f"{relative}: 未知 type：{doc_type or '空'}")
            continue
        missing = sorted(key for key in required if key not in document.meta)
        if missing:
            issues.append(f"{relative}: 缺少字段：{', '.join(missing)}")

        document_id = str(document.meta.get("id", ""))
        if not ID_RE.fullmatch(document_id):
            issues.append(f"{relative}: id 只能包含小写字母、数字和连字符")
        elif document_id in ids:
            other = ids[document_id].path.relative_to(root).as_posix()
            issues.append(f"{relative}: id 与 {other} 重复：{document_id}")
        else:
            ids[document_id] = document

        expected_prefix = {
            "source_note": "notes/",
            "idea_note": "notes/",
            "topic": "wiki/topics/",
            "entity": "wiki/entities/",
            "brief": "briefs/",
        }[doc_type]
        if not relative.startswith(expected_prefix):
            issues.append(f"{relative}: type={doc_type} 应位于 {expected_prefix}")

        for field in ("created_at", "updated_at"):
            if field in document.meta and not valid_iso_datetime(document.meta[field]):
                issues.append(f"{relative}: {field} 不是 ISO 8601 时间")

        if not str(document.meta.get("title", "")).strip():
            issues.append(f"{relative}: title 不能为空")
        if document.meta.get("status") not in {"active", "draft", "archived"}:
            issues.append(f"{relative}: status 只能是 active、draft 或 archived")

        for heading in REQUIRED_HEADINGS[doc_type]:
            if not re.search(rf"^##\s+{re.escape(heading)}\s*$", document.body, flags=re.MULTILINE):
                issues.append(f"{relative}: 缺少正文标题「{heading}」")

        if doc_type in NOTE_TYPES:
            for list_field in ("tags", "related"):
                if not isinstance(document.meta.get(list_field), list):
                    issues.append(f"{relative}: {list_field} 必须是列表")
            content_hash = str(document.meta.get("content_hash", "")).lower()
            if not HASH_RE.fullmatch(content_hash):
                issues.append(f"{relative}: content_hash 必须是 SHA-256")
            elif content_hash in content_hashes:
                other = content_hashes[content_hash].path.relative_to(root).as_posix()
                issues.append(f"{relative}: 内容与 {other} 重复")
            else:
                content_hashes[content_hash] = document

            source_url = normalize_url(str(document.meta.get("source_url", "")))
            if source_url:
                if source_url in normalized_urls:
                    other = normalized_urls[source_url].path.relative_to(root).as_posix()
                    issues.append(f"{relative}: 来源 URL 与 {other} 重复")
                else:
                    normalized_urls[source_url] = document

            source_ref = str(document.meta.get("source_ref", ""))
            if doc_type == "source_note":
                target = inside_root(root, source_ref)
                if target is None or not target.is_file():
                    issues.append(f"{relative}: source_ref 不存在或越出项目：{source_ref}")
            else:
                if document.meta.get("source_type") != "user_idea":
                    issues.append(f"{relative}: idea_note 的 source_type 必须是 user_idea")
                if source_ref or document.meta.get("source_url"):
                    issues.append(f"{relative}: idea_note 不应伪造 source_ref 或 source_url")

        if doc_type in WIKI_TYPES:
            if not isinstance(document.meta.get("source_notes"), list):
                issues.append(f"{relative}: source_notes 必须是列表")
            if not isinstance(document.meta.get("contradictions"), list):
                issues.append(f"{relative}: contradictions 必须是列表")

        if doc_type == "brief":
            source_pages = document.meta.get("source_pages")
            if not isinstance(source_pages, list) or len(source_pages) < 2:
                issues.append(f"{relative}: source_pages 至少包含两条来源")

    note_ids = {doc_id for doc_id, doc in ids.items() if doc.meta.get("type") in NOTE_TYPES}
    page_ids = set(ids)
    for document in documents:
        relative = document.path.relative_to(root).as_posix()
        document_id = str(document.meta.get("id", ""))
        doc_type = document.meta.get("type")
        if doc_type in NOTE_TYPES:
            for related_id in document.meta.get("related", []):
                related_id = str(related_id)
                if related_id not in note_ids:
                    issues.append(f"{relative}: related 指向不存在的笔记：{related_id}")
                    continue
                other = ids[related_id]
                if document_id not in [str(value) for value in other.meta.get("related", [])]:
                    issues.append(f"{relative}: 与 {related_id} 的关联不是双向")
        elif doc_type in WIKI_TYPES:
            for source_id in document.meta.get("source_notes", []):
                if str(source_id) not in note_ids:
                    issues.append(f"{relative}: source_notes 指向不存在的笔记：{source_id}")
        elif doc_type == "brief":
            for source_id in document.meta.get("source_pages", []):
                if str(source_id) not in page_ids:
                    issues.append(f"{relative}: source_pages 指向不存在的页面：{source_id}")

    if check_index:
        index_path = root / "INDEX.md"
        current = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
        if current != build_index(root, documents):
            issues.append("INDEX.md 缺失或已过期，请运行 python3 scripts/kb.py index")
    return sorted(set(issues))


def find_existing(root: Path, source_url: str = "", content_hash: str = "") -> list[Document]:
    documents, _ = load_documents(root)
    wanted_url = normalize_url(source_url)
    wanted_hash = content_hash.lower().strip()
    matches = []
    for document in documents:
        if document.meta.get("type") not in NOTE_TYPES:
            continue
        same_url = bool(wanted_url) and normalize_url(str(document.meta.get("source_url", ""))) == wanted_url
        same_hash = bool(wanted_hash) and str(document.meta.get("content_hash", "")).lower() == wanted_hash
        if same_url or same_hash:
            matches.append(document)
    return matches


def search(root: Path, query: str, limit: int = 20) -> list[tuple[int, Document]]:
    documents, _ = load_documents(root)
    terms = [term.lower() for term in query.split() if term.strip()] or [query.lower()]
    results: list[tuple[int, Document]] = []
    for document in documents:
        title = str(document.meta.get("title", "")).lower()
        tags = " ".join(str(tag).lower() for tag in document.meta.get("tags", []))
        body = document.body.lower()
        score = 0
        for term in terms:
            score += title.count(term) * 5
            score += tags.count(term) * 3
            score += min(5, body.count(term))
        if score:
            results.append((score, document))
    return sorted(results, key=lambda item: (item[0], str(item[1].meta.get("updated_at", ""))), reverse=True)[:limit]


def run_sync(root: Path, threshold: int = 4) -> tuple[int, bool, list[str]]:
    changed_relations, _ = update_relations(root, threshold=threshold)
    changed_index = write_index(root)
    issues = validate_root(root)
    return changed_relations, changed_index, issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="维护本地 Markdown 知识库")
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT, help="知识库根目录")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate", help="校验数据结构、引用和索引")

    index_parser = subparsers.add_parser("index", help="重建 INDEX.md")
    index_parser.add_argument("--check", action="store_true", help="只检查，不写入")

    relate_parser = subparsers.add_parser("relate", help="计算并写入双向关联")
    relate_parser.add_argument("--threshold", type=int, default=4)
    relate_parser.add_argument("--dry-run", action="store_true")

    sync_parser = subparsers.add_parser("sync", help="更新关联、索引并校验")
    sync_parser.add_argument("--threshold", type=int, default=4)

    search_parser = subparsers.add_parser("search", help="搜索 Wiki、笔记和选题")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=20)

    lookup_parser = subparsers.add_parser("lookup", help="按来源 URL 或内容哈希查重")
    lookup_group = lookup_parser.add_mutually_exclusive_group(required=True)
    lookup_group.add_argument("--source-url")
    lookup_group.add_argument("--content-hash")

    hash_parser = subparsers.add_parser("hash-file", help="计算文件 SHA-256")
    hash_parser.add_argument("path", type=Path)

    normalize_parser = subparsers.add_parser("normalize-url", help="规范化 URL")
    normalize_parser.add_argument("url")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()

    if args.command == "hash-file":
        if not args.path.is_file():
            print(f"文件不存在：{args.path}", file=sys.stderr)
            return 2
        print(hash_file(args.path))
        return 0

    if args.command == "normalize-url":
        print(normalize_url(args.url))
        return 0

    if args.command == "lookup":
        matches = find_existing(root, args.source_url or "", args.content_hash or "")
        for document in matches:
            print(f"{document.meta.get('id')}\t{document.path.relative_to(root)}\t{document.meta.get('title')}")
        return 0 if matches else 1

    if args.command == "search":
        results = search(root, args.query, args.limit)
        for score, document in results:
            print(f"{score}\t{document.path.relative_to(root)}\t{document.meta.get('title')}")
        return 0 if results else 1

    if args.command == "index":
        changed = write_index(root, check_only=args.check)
        if args.check and changed:
            print("INDEX.md 已过期", file=sys.stderr)
            return 1
        print("INDEX.md 已更新" if changed else "INDEX.md 无变化")
        return 0

    if args.command == "relate":
        try:
            changed, candidates = update_relations(root, args.threshold, args.dry_run)
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 1
        for left, right, score, tags, title_terms in candidates:
            print(f"{score}\t{left}\t{right}\ttags={','.join(tags)}\ttitle={','.join(title_terms)}")
        action = "将更新" if args.dry_run else "已更新"
        print(f"{action} {changed} 篇笔记")
        return 0

    if args.command == "validate":
        issues = validate_root(root)
        if issues:
            for issue in issues:
                print(f"ERROR\t{issue}")
            return 1
        print("知识库校验通过")
        return 0

    if args.command == "sync":
        try:
            changed_relations, changed_index, issues = run_sync(root, args.threshold)
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 1
        print(f"关联更新：{changed_relations} 篇笔记")
        print(f"索引更新：{'是' if changed_index else '否'}")
        if issues:
            for issue in issues:
                print(f"ERROR\t{issue}")
            return 1
        print("知识库同步完成，校验通过")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
