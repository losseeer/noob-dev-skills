# 步骤 1：解决上下文（三档输入）

## 目的

确定这一轮页面要对齐什么。按顺序取，**上一档拿到就不再往下走**。

| 档 | 来源 | 拿到之后 |
|---|---|---|
| 1 | 契约文件 `.project/design/tech/interfaces.yaml` | `upstream.interfaces.status: found`，记 `fields_read` |
| 2 | 用户原始输入——对话描述、截图、贴出的接口片段 | `status: not_found`，**必须记一条 gap** 说明没对齐什么 |
| 3 | 提问 | 只问前端技术栈（步骤 2）；页面细节不问，先做出来让人看 |

## 第 1 档必须核对来源

读到 `interfaces.yaml` 后先看 `produced_by` 是不是 `tech-design-skill`。

| 情况 | 处置 |
|---|---|
| 是 | 按契约走 |
| 字段缺失或值不是本包 skill 名 | **降回第 2 档**，`status: skipped`，note 写「路径相同但来源未确认」 |

不要把撞巧同名的文件当成契约——那是把未确认当成已确认。

## 提取接口里的可演示状态

从 `interfaces.yaml` 里抽出两类东西，它们是页面的骨架：

1. **成功分支**：`request` / `response` 里的主要字段 → 页面上要能看到结果
2. **错误分支**：每条 `error_case` → 页面上要有一条能走到它的输入路径

抽不到的、或做了但没覆盖到的，全部进 `gaps`。**`validate_bundle.py` 会拦「上游缺失却没有 gap」的情况**，
所以这一步偷懒会被校验挡住。

## 硬性约束

- 上游文件一律**只读**，不修改接口契约，也不改需求卡。
- 不调用 `tech-design-skill`，也不读它的 `SKILL.md`。
- 不因为上游缺失就阻塞——记 gap 后继续做。
