---
name: ui-prototype-skill
description: Turn an existing interface contract into runnable, clickable pages for human review. Produces a prototype index and interactive HTML/Vue/React pages that actually trigger each error branch, with unaligned parts recorded as explicit gaps. Trigger on 画个原型 / 做个能点的 demo / 交互给我看看 / 页面长什么样 / UI 原型 / 先看一下界面 / 做个页面让我点, or when a design already exists and the user wants to see and feel the UI before implementation. Do NOT use for choosing backend technology, designing data models or interface contracts — that is owned by tech-design-skill. Do NOT use for writing requirement cards or acceptance criteria — that is owned by requirement-analysis-skill. Do NOT use for deciding scope — that is owned by project-positioning-skill. Do NOT use for writing production code or tracking build progress — that is owned by dev-companion-skill.
---

# UI Prototype Skill

把已有的接口契约变成**能点、能看**的页面，用来让人 review 交互。

一句分工：

> 定位决定**做不做**，需求决定**做成什么样**，技术设计决定**怎么解**，
> **本 Skill 决定界面长什么样、点了会怎样**，开发陪伴负责**真的做下去并记得住**。

与其余四个 Skill **只通过文件约定协作，不互相调用**。

## 边界（不可越界）

| 本 Skill 不做 | 归属 |
|---|---|
| 技术选型（前端栈除外）、数据模型、接口契约 | `tech-design-skill` |
| 写需求卡、验收标准 | `requirement-analysis-skill` |
| 判断该不该做、是否超范围 | `project-positioning-skill` |
| 写实现代码、记录开发进度 | `dev-companion-skill` |
| 最终视觉稿定稿（配色、动效、响应式规范） | 用户 review 决定 |

硬性约束：

- 不依赖上游产物，不要求接口契约存在。
- 可选读取 `.project/design/tech/interfaces.yaml`，**只读不修改**。
- 读到契约必须核对 `produced_by` 是 `tech-design-skill`；不是就降回原始输入并在 note 里写明。
- 上游缺失时**不阻塞**，但必须记进 `gaps`——`validate_bundle.py` 会拦「缺失却不记」。
- 页面本身**不进 schema 校验**，只有 `current.yaml` 里的清单受校验。

## 先判定任务类型

按顺序路由：

1. **纯打听类不归本 Skill，本条只作误路由兜底**：用户只是问某个界面该怎么设计、
   某个交互模式叫什么 → 归 `dev-companion-skill`（能力 B）。若已被路由进来 → 只回答，不写文件。
2. 已有原型且用户要求改 → 改页面并重跑校验，更新 `pages` 的 `review_status`。
3. 已有原型且用户要看汇总 → 只输出 `current.yaml` 的摘要。
4. 其余「给我看个界面 / 做个能点的」请求 → 走**完整流程**（步骤 1-4）。

## 三档输入

| 档 | 来源 | 拿到之后 |
|---|---|---|
| 1 | 契约文件 `.project/design/tech/interfaces.yaml` | `upstream.interfaces.status: found`，记 `fields_read` |
| 2 | 用户原始输入——对话描述、截图、贴出的接口片段 | `status: not_found`，**必须记一条 gap** |
| 3 | 提问 | 只问前端技术栈；页面细节不问，先做出来让人看 |

## 核心流程

### 1. 解决上下文

读取 `prompts/01_resolve_context.md`。核对 `produced_by`，抽出成功分支与 `error_case`，
抽不到或覆盖不到的进 `gaps`。

### 2. 选技术栈（每轮必问）

读取 `prompts/02_choose_stack.md`。**必须问且必须给推荐值**：
默认纯 HTML 单文件（零构建、双击即开），项目已有 Vue/React 栈时改推对应项。
用户超时或未授权 → 执行推荐值。

### 3. 做页面

读取 `prompts/03_build_pages.md`。四条硬要求：能直接打开、错误态能触发、
数值会变、留白要写。

### 4. 收尾与 Review

读取 `prompts/04_review.md`。更新 `current.yaml`，然后**必须跑校验**：

```bash
cd <本 skill 目录>/scripts && python validate_bundle.py
```

`review_status`：`pending` → `reviewed` / `needs_change`。
`current.yaml` 的 `status` 仅在所有页面都 `reviewed`、且 `gaps` 都已交代时才能置 `reviewed`。

## 产物约定

```text
.project/prototype/
  current.yaml        原型索引（机器读，进 schema）
  pages/
    index.html        可交互页面，双击即开
```

ID 约定：`REQ-\d{3}` / `AC-\d{3}`（沿用上游）/ `IF-\d{3}`（沿用上游）/ `Q\d+`。
页面文件名与索引里的 `file` 必须一致，改一边就要改另一边——对不上会校验失败，这是刻意的。

## 本 Skill 的四条共享原则形态

1. **问题 ≠ 指令** → 路由第 1 条：只讨论界面怎么设计、没说要做时，只回答，不写文件。
2. **不许把推断写成事实** → 页面状态必须对齐 `error_case`，对不上的记 `gaps`，不假装覆盖。
3. **不许静默降级** → 上游缺失、页面打不开、校验跑不起来，全部显式报告并记 gap。
4. **单一真源** → `current.yaml` 是页面清单唯一真源，页面本身不进校验，不手写第二份清单。

## 资源索引

- 解决上下文：`prompts/01_resolve_context.md`
- 选技术栈：`prompts/02_choose_stack.md`
- 做页面：`prompts/03_build_pages.md`
- 收尾与 Review：`prompts/04_review.md`
- 页面规则与降级：`rules/page_rules.yaml`
- Schema：`schemas/`
- 索引模板：`templates/index.yaml.tpl`
- 完整示例：`examples/shortlink/`
- 校验脚本：`scripts/validate_artifact.py`（单产物）与 `scripts/validate_bundle.py`（页面引用与示例一致性，带 `--selftest`）
- CI 工作流模板：`assets/ui-prototype-check.yml`
