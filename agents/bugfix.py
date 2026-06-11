"""BugFix Squad — Bug 修复 Agent"""

def run(task, fix):
    task_id = task["id"]
    lines = fix.count("\n") + 1 if fix else 0
    print(f"[BugFix] 修复Agent: 已为 {task_id} 应用修复 ({lines} lines)")
    return {"task_id": task_id, "squad": "bugfix", "fix_lines": lines}