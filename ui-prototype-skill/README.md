# ui-prototype-skill

把已有的接口契约变成**能点、能看**的页面，用来让人 review 交互。

一句话：**长什么样、点了会怎样**。

- `project-positioning-skill` 决定**做不做**
- `requirement-analysis-skill` 决定**做成什么样**
- `tech-design-skill` 决定**怎么解**（技术选型、数据模型、接口）
- 本 Skill 决定**界面长什么样、点了会怎样**
- `dev-companion-skill` 负责**真的做下去并记得住**

## 产物布局

```text
.project/prototype/
  current.yaml        原型索引（机器读，进 schema）
  pages/
    index.html        可交互页面，双击即开
```

**页面本身不进 schema 校验**，只有 `current.yaml` 里的清单受校验。

## 三档输入

| 档 | 来源 |
|---|---|
| 1 | 契约文件 `.project/design/tech/interfaces.yaml`（核对 `produced_by`） |
| 2 | 用户原始输入——对话描述、截图、贴出的接口片段 |
| 3 | 提问（只有前端技术栈这一项必问） |

上游缺失**不阻塞**，但必须记进 `gaps` 说明没对齐什么——`validate_bundle.py` 会拦
「上游缺失却没有 gap」的情况。这是本 Skill 对「不许静默降级」的落地方式。

## 必问清单

只有一项：**原型用什么形态产出**（纯 HTML 单文件 / Vue / React）。
默认推荐纯 HTML 单文件，零构建、双击即开。项目已有 Vue/React 栈时改推对应项。

其余一律不问——原型是用来让人 review 的，不是用来收集信息的。

## 用法

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r scripts/requirements.txt

cd scripts
python validate_bundle.py --selftest   # selftest: 5 passed, 0 failed
python validate_bundle.py              # Bundle validation passed

cd ..
python scripts/validate_artifact.py current .project/prototype/current.yaml
```

## 校验做什么

| 检查 | 拦截什么 |
|---|---|
| 页面文件存在 | 索引登记了 `index.html`，磁盘上却没有 |
| 上游缺失必须有 gap | 接口契约没读到却没记录，等于把降级藏起来 |
| 每页覆盖需求 | 页面 `covers` 为空，说明不知道为什么存在 |

这套检查自带 `--selftest`（5 个用例，含 3 个反向），所以「检查规则本身对不对」也是可验证的。

## 与其它 Skill 的边界

| 本 Skill 不做 | 归属 |
|---|---|
| 技术选型（除前端栈）、数据模型、接口设计 | `tech-design-skill` |
| 写需求卡与验收标准 | `requirement-analysis-skill` |
| 判断该不该做 | `project-positioning-skill` |
| 写实现代码、记录开发进度 | `dev-companion-skill` |
| 最终视觉稿定稿 | 用户 review |
