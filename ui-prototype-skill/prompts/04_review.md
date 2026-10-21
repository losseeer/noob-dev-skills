# 步骤 4：收尾与 Review

## 更新索引

把这一轮的结果写进 `.project/prototype/current.yaml`：

- `pages`：每页的 `file`、`covers`（覆盖哪些 REQ / AC）、`states_shown`（展示了哪些状态）、
  `review_status`
- `gaps`：没覆盖到的，每条必须有 `kind` / `ref` / `reason`
- `open_questions`：等用户答复的

**`covers` 不许留空**——页面覆盖不到任何需求，说明这一页不知道为什么存在。

## 跑校验

```bash
cd <本 skill 目录>/scripts && python validate_bundle.py
```

它检查三件事：登记的页面文件在不在、上游缺失有没有记 gap、每页有没有覆盖需求。

**脚本跑不起来、Python 不可用、依赖没装——全部显式报告，不许当成通过。**

## Review 语义

| review_status | 含义 |
|---|---|
| `pending` | 已生成，等用户看 |
| `reviewed` | 用户看过并认可 |
| `needs_change` | 用户要求改，改完重跑校验 |

`current.yaml` 的 `status` 仅在所有页面都 `reviewed`、且 `gaps` 都已交代时才能置 `reviewed`。
**有 gap 没交代就置 reviewed，等于把未完成说成已完成。**

## 硬性约束

- 用户说「这里不对」时改页面并重跑校验，不要只在对话里解释为什么这样设计。
- 页面文件删除或改名时，索引里的 `file` 必须同步改——对不上会导致校验失败，
  这是刻意的，防止索引与磁盘漂移。
