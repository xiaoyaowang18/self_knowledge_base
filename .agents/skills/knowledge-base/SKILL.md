---
name: knowledge-base
description: 管理当前仓库的个人 AI 知识库；当用户要求收录链接、文件或想法，查询库内观点，编译主题，生成写作选题，维护索引或校验知识库时使用。不要用于与本知识库无关的通用搜索或写作。
---

# Personal AI Knowledge Base

把用户输入转成可追溯的本地知识，并从现有知识生成回答和写作行动。

## 先选择工作模式

- 收录链接、文件或想法，或编译主题／实体：读取 [写入工作流](references/write-workflows.md)。
- 查询库内观点或生成选题：读取 [读取工作流](references/read-workflows.md)。生成选题同时遵守写入工作流中的选题落盘规则。
- 维护、检索、查重或校验：直接使用根目录的 `scripts/kb.py`。

## 不可破坏的约束

- 以包含 `AGENTS.md`、`INDEX.md` 和 `scripts/kb.py` 的目录为知识库根目录。
- 原始资料写入 `raw/` 后只读，不覆盖。删除任何资料前必须取得用户确认。
- 先留原文，再做 AI 加工；读取失败时不生成摘要或补造事实。
- 资料事实、用户观点和 AI 推断必须明确区分。
- 正式回答和选题必须给出根目录相对路径形式的来源。
- 不引入数据库、向量库、服务器、UI 或新的第三方依赖。
- 写入正式内容后运行 `python3 scripts/kb.py sync`；命令非零退出时修复问题，不能绕过校验。

## 机械命令

```bash
python3 scripts/kb.py normalize-url "URL"
python3 scripts/kb.py hash-file /path/to/file
python3 scripts/kb.py lookup --source-url "URL"
python3 scripts/kb.py lookup --content-hash "SHA256"
python3 scripts/kb.py search "查询词"
python3 scripts/kb.py sync
python3 scripts/kb.py validate
```

`lookup` 返回 0 表示已存在，返回 1 表示未找到。`sync` 依次更新双向关联、索引并校验全库。

## 交付结果

完成写入后，只汇报新增、更新、跳过和失败的文件，以及最相关的已有知识。查询时先给结论，再列直接支撑结论的来源；库内无依据时明确说没有。
