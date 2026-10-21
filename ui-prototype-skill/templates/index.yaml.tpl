produced_by: ui-prototype-skill
version: 1
as_of: {{date}}
project: ""
upstream:
  interfaces:
    status: found              # found / not_found / skipped
    ref: .project/design/tech/interfaces.yaml
    fields_read: []
    note: ""
  requirements:
    status: not_found
    ref: .project/requirements/
    note: ""
stack: html                    # html / vue / react
stack_rationale: ""
entry: index.html
pages:
  - name: ""
    file: index.html
    covers: []                 # REQ-xxx / AC-xxx，不许留空
    states_shown: []           # 页面上真的能触发出来的状态
    review_status: pending     # pending / reviewed / needs_change
    note: ""
gaps:
  # 上游缺失、或页面没覆盖到的，每条都要有 kind / ref / reason。
  # 上游 status 是 not_found / skipped 时不记 gap，校验会失败。
  - kind: interface            # interface / acceptance / state / requirement
    ref: ""
    reason: ""
    deferred_to: ""
open_questions: []
status: draft                  # draft / reviewed
