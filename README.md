# 个人 AI 知识库

这是一个面向个人写作者的本地 AI 知识库。它把链接、文件和想法加工成可追溯的原子笔记，再编译为主题结论，并服务知识问答和写作选题。

## 最快使用方式

在项目目录打开 Codex，直接说：

```text
使用 $knowledge-base 收录这个链接：https://example.com
```

也可以自然表达：

```text
记住这个想法：AI 产品的长期壁垒可能是个人上下文。
我现在对「个人知识库要不要向量库」的判断是什么？
基于最近的素材，给我 3 个可以立刻写的公众号选题。
```

项目级 Skill 位于 `.agents/skills/knowledge-base/`。Codex 会自动发现；若当前会话没有出现，重启 Codex 后再试。

## 数据目录

- `inbox/`：待处理缓冲区，存放尚未进入正式层的链接、文件或想法草稿；处理完成后正式事实进入其他层。
- `raw/`：原始网页正文和附件，只新增、不覆盖。
- `notes/`：单源笔记和用户想法。
- `wiki/topics/`：主题结论。
- `wiki/entities/`：人物、产品、公司等实体档案。
- `briefs/`：带证据的写作选题。
- `INDEX.md`：由脚本生成的导航索引，不手工编辑。

## 机械工具

所有命令只依赖 Python 3 标准库：

```bash
python3 scripts/kb.py sync
python3 scripts/kb.py validate
python3 scripts/kb.py search "知识库"
python3 scripts/kb.py wiki-candidates --note-id "note-YYYYMMDD-HASH8"
python3 scripts/kb.py lookup --source-url "https://example.com"
python3 scripts/kb.py hash-file /path/to/file.pdf
```

`wiki-candidates` 是只读的 Wiki 影响检查，会列出主题／实体页面的直接命中和关联候选，不自动创建或改写页面。`sync` 会依次更新双向关联、重建索引并校验全库，但不替代 AI 的语义 Wiki 编译。命令返回非零退出码表示存在需要处理的问题。

## MVP 边界

当前不包含 UI、数据库、向量检索、云同步、协作、定时任务、音视频识别和专用渠道爬虫。完整范围见 [产品设计文档](docs/PRODUCT-DESIGN.md) 。

## 验证

```bash
python3 -m unittest discover -s tests -v
python3 scripts/kb.py sync
```
