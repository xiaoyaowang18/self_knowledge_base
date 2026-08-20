# 写入工作流

仅在收录、编译或生成选题需要写入正式知识文件时读取。

## 收录链接

1. 用 `python3 scripts/kb.py normalize-url "URL"` 规范化地址，再用 `lookup --source-url` 查重。已存在时返回已有笔记，除非用户明确要求刷新，否则不重复抓取。
2. 读取页面实际内容。受限页面读取失败时，说明原因并请用户提供正文或导出文件；不绕过平台限制。
3. 先把抓取到的正文暂存在 `/tmp`，运行 `hash-file` 和 `lookup --content-hash`。内容已存在时停止，不向正式目录写重复文件。
4. 将正文写入 `raw/YYYY/MM/YYYY-MM-DD-slug.md`。原文保持可复核，不加入 AI 判断。
5. 复制 `templates/source-note.md` 的字段和正文结构，创建 `notes/YYYY-MM-DD-slug.md`：
   - `id` 使用 `note-YYYYMMDD-HASH8`，其中 `HASH8` 是内容哈希前 8 位；
   - `source_ref` 使用根目录相对路径；
   - `source_url` 保存规范化 URL；
   - `content_hash` 保存完整 SHA-256；
   - 从实际内容选择 3—5 个已有标签，确无合适标签时才新增；
   - 「核心信息」只写来源支持的事实，「我的判断」写对用户的意义。
6. 运行 `python3 scripts/kb.py sync`。
7. 查看新笔记的 `related`。若命中已有 Wiki，更新该页；若同一主题已有至少两篇有效笔记，创建 Wiki。再次运行 `sync`。

## 收录本地文件

1. 确认文件可读，运行 `hash-file` 和 `lookup --content-hash` 查重。
2. 将原文件复制到 `raw/YYYY/MM/`，保留扩展名和内容，不覆盖同名文件。
3. 读取可提取内容并按「收录链接」第 5—7 步创建笔记。PDF 没有可提取文本时停止；OCR 不在 MVP 范围。

## 记录用户想法

1. 保留用户原话并暂存到 `/tmp`，计算内容哈希后查重。
2. 按 `templates/idea-note.md` 创建笔记：`source_type` 固定为 `user_idea`，`source_ref` 和 `source_url` 留空。
3. 不给用户观点补造外部证据；在「证据与限制」中写出待验证点。
4. 运行 `sync`，再按需要回织 Wiki。

## 编译主题或实体

1. 先用 `search`、`INDEX.md` 和笔记的 `related` 找齐相关笔记。
2. 通常至少需要两条有效笔记；用户明确要求时可以先建单源草稿，`status` 设为 `draft`。
3. 按 `templates/wiki.md` 写入 `wiki/topics/` 或 `wiki/entities/`。`source_notes` 只列实际读取过的笔记 ID。
4. 综合结论要区分共识、分歧和待确认问题。资料冲突时并列保留，不强行统一。
5. 更新已有页时保留仍然有效的矛盾和来源，刷新 `updated_at`，再运行 `sync`。

## 选题落盘

只有选题具备明确读者、核心冲突、至少两条可追溯来源和下一步动作时，才按 `templates/brief.md` 写入 `briefs/`。否则只在对话中说明素材不足，不创建文件。写入后运行 `sync`。
