# 输入：短链服务的界面原型

演示 `ui-prototype-skill` 的最小闭环：从上游接口契约出发，产出一个能点、能看的页面。

## 上游（虚构但完整）

`tech-design-skill` 产出的接口契约 `.project/design/tech/interfaces.yaml`：

| ID | 接口 | 承担 |
|---|---|---|
| IF-001 | `POST /api/links` | AC-001 创建成功、AC-002 同 URL 复用 |
| IF-002 | `GET /{code}` | AC-010 302 跳转、AC-011 未知短码 404 |
| IF-003 | `GET /api/links/{code}/stats` | AC-020 点击计数 |

## 本例看点

1. **页面状态对齐接口错误码**：`400_INVALID_URL` 和 `404_NOT_FOUND` 不是画上去的，
   是真的能用输入框触发出来（见 `pages/index.html`）。
2. **没覆盖到的要写进 `gaps`**：IF-003 的失败分支页面没做，这里如实记了一条，
   而不是假装覆盖全了。`validate_bundle.py` 会拦「上游缺失却不记 gap」这种情况。
3. **零外部依赖**：`index.html` 里 `src=`/`href=` 出现 0 次，双击即开，不需要起服务。

## 校验

```bash
cd ui-prototype-skill/scripts
python validate_bundle.py --selftest   # selftest: 5 passed, 0 failed
python validate_bundle.py              # Bundle validation passed
```
