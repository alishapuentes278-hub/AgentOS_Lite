"""Squad B — 代码生成 Agent"""

def run(task, code):
    task_id = task["id"]
    lines = code.count("\n") + 1 if code else 0
    print(f"[Squad B] 代码Agent: 已为 {task_id} 生成代码 ({lines} lines)")
    return {"task_id": task_id, "squad": "B", "code_lines": lines}