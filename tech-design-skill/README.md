# tech-design-skill

把已经确定要做的需求翻译成「可以开工」的技术方案：技术选型、架构、数据模型、接口契约。
**界面原型不归本 Skill**，由 `ui-prototype-skill` 承接——它读本 Skill 产出的接口契约。

一句话：**怎么解**。

- 上游 `project-positioning-skill` 决定**做不做**
- 上游 `requirement-analysis-skill` 决定**做成什么样**
- 本 Skill 决定**怎么解**
- 下游 `dev-companion-skill` 负责**真的做下去并记得住**

四者只通过文件约定协作，不互相调用。上游产物缺失时记 `not_found`，不阻塞。

## 产物布局

```text
.project/design/
  current.yaml               方案索引（机器读，进 schema）
  current.md                 人类读摘要 + 交付清单
  tech/
    stack.yaml               技术选型，每条带 basis
    architecture.md          分层与模块边界
    data-model.yaml          数据模型，每个字段带 basis
    interfaces.yaml          接口契约，每条带 acceptance_refs
    layout.md                目录结构（不进 schema）
  decisions/ADR-001-<slug>.md
  reviews/<date>-<version>.yaml
```

界面原型在 `.project/prototype/`，由 `ui-prototype-skill` 写，本 Skill 不碰那个目录。

## 核心机制：选型依据四分类

这是「不许把推断写成事实」在本 Skill 的落地形态。每条 `SEL-xxx` 必须选一个 `basis`：

| basis | 含义 | 强制要求 |
|---|---|---|
| `constraint` | 来自定位卡约束 | 必须写 `source_ref` |
| `requirement` | 来自验收标准 | 必须写 `source_ref` |
| `assumption` | 推断 | 必须写 `why_assumed` + `revisit_when`（schema 强制） |
| `user_choice` | 用户明确选的 | 写清从哪得知 |

注意：**这不是** 定位/需求两个 Skill 的六状态枚举。两者服务的对象不同，不要互相套用。

## 用法

安装后在适合的话题上自动触发。手工跑校验：

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r scripts/requirements.txt

# 校验脚本本身是否正常
python scripts/validate_bundle.py --selftest
# 输出 selftest: 7 passed, 0 failed

# 校验 schema、交叉引用与内置示例
cd scripts && python validate_bundle.py

# 单个产物
python scripts/validate_artifact.py current    .project/design/current.yaml
python scripts/validate_artifact.py stack      .project/design/tech/stack.yaml
python scripts/validate_artifact.py interfaces .project/design/tech/interfaces.yaml
```

支持的 kind：`current` / `stack` / `data_model` / `interfaces` / `review`。

## bundle 校验做什么

| 检查 | 拦截什么 |
|---|---|
| ADR 引用存在 | `decisions` 写了 `ADR-003` 但 `decisions/` 下没有文件 |
| 接口认领的 AC 已登记 | 接口说它实现了 `AC-099`，但索引里压根没这条 |
| covered 的 AC 有人认领 | AC 标了 `covered` 却没有任何接口/实体/页面承担它 |
| assumption 有出处 | `basis: assumption` 没写 `why_assumed` |
| 假设有缓解措施 | `impact_if_wrong` 写了但没写 `mitigation` |

这套检查自带 `--selftest`（7 个用例，含 6 个反向），所以「检查规则本身对不对」也是可验证的。

## CI

把 `assets/solution-check.yml` 复制到目标仓库的 `.github/workflows/`，
并按实际 Skill 安装路径调整。它会依次跑 selftest、bundle 校验、单产物校验、
以及 assumption 可追溯性检查。

## 与其他 Skill 的边界

| 本 Skill 不做 | 归属 |
|---|---|
| 决定该不该做 | `project-positioning-skill` |
| 写需求卡与验收标准 | `requirement-analysis-skill` |
| 解释概念、记录开发进度 | `dev-companion-skill` |
| **写实现代码** | `dev-companion-skill` |

**不得自行放宽上游 constraints。** 约束不合理只能记 `escalated_to_positioning` 交回上游。
