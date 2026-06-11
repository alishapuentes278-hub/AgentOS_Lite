"""DAG 调度器 — 按依赖拓扑排序执行任务"""

def topological_sort(dag):
    """返回DAG拓扑排序的任务执行顺序"""
    in_degree = {node: 0 for node in dag}
    for node, deps in dag.items():
        for dep in deps:
            in_degree[node] += 1

    queue = [node for node, deg in in_degree.items() if deg == 0]
    result = []

    while queue:
        node = queue.pop(0)
        result.append(node)
        for other, deps in dag.items():
            if node in deps:
                in_degree[other] -= 1
                if in_degree[other] == 0:
                    queue.append(other)

    return result if len(result) == len(dag) else None


def get_ready_tasks(queue, dag):
    """返回当前可执行的任务（依赖已满足且状态为PENDING）"""
    task_status = {t["id"]: t["status"] for t in queue}
    ready = []
    for task in queue:
        if task["status"] != "PENDING":
            continue
        deps = dag.get(task["id"], [])
        if all(task_status.get(d, "DONE") == "DONE" for d in deps):
            ready.append(task)
    return ready