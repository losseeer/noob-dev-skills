# 输入：短链服务

本例演示 tech-design-skill 的最小闭环：从上游两份产物出发，产出技术方案（选型 + 数据模型 + 接口契约）。

## 上游（虚构但完整）

**定位卡摘要** `.project/positioning/current.yaml`

- `criticality`: low
- `scale`: small
- `budget`: low
- `constraints`: 禁止引入按量付费的托管服务
- `non_functional_priority`: 成本优先，其次开发速度

**需求卡摘要** `.project/requirements/`

| ID | 标题 | 验收标准 |
|---|---|---|
| REQ-001 | 创建短链 | AC-001 提交长 URL 后返回短码；AC-002 同一长 URL 重复提交复用既有短码 |
| REQ-002 | 短码跳转 | AC-010 访问短码 302 跳转；AC-011 未知短码返回 404 |
| REQ-003 | 点击统计 | AC-020 每次跳转计数加一 |

## 本例看点

1. **选型每条都有依据**（`tech/stack.yaml` 的 `basis` 字段）——
   `constraint` / `requirement` / `assumption` / `user_choice` 四种都用到了，
   其中 `SEL-006` 是 `assumption`，因此被迫写出 `why_assumed` 与 `revisit_when`。
2. **预算冲突被显式处置**（`current.yaml` 的 `CONF-001`）——
   最初想用托管 KV 存储，被 `budget: low` 打回，改成 SQLite 并记为 `resolved`。
3. **上游每条 AC 都落到具体产物**（`current.yaml` 的 `coverage`）——
   五条 AC 全部 `covered`，且都有接口或实体认领，跑 bundle 校验能兜住这一点。
4. **界面原型不在本例里**——`ui-prototype-skill` 会读这里的 `tech/interfaces.yaml` 出页面，
   本 Skill 只产出到接口契约为止。

## 校验

```bash
cd tech-design-skill/scripts
python validate_bundle.py
```
