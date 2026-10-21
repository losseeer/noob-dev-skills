version: 1
protocol_note: ""
interfaces:
  # http 型必须给 method 与 path；cli 型必须给 path；event / internal 两者都不需要
  - id: IF-001
    name: ""
    kind: http                      # http / cli / event / internal / page
    method: POST
    path: /api/<resource>
    request:
      - name: ""
        type: ""
        required: true
        constraint: ""
        source: REQ-xxx
    response:
      - name: ""
        type: ""
    errors:
      - code: 400_<CASE>
        when: ""
        response_note: ""
        acceptance_ref: AC-000      # 呼应上游 exception_flows
    source_refs: []
    acceptance_refs: []             # 至少一条，不能为空
    note: ""
