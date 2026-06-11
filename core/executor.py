import time
import json
from agents import squad_a, squad_b, bugfix

RUNTIME_PATH = "runtime"
DEEPSEEK_MODEL = "deepseek-v4-pro"

def load(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def call_deepseek(ds_client, prompt, max_tokens=2000):
    """调用 DeepSeek API（通过本地代理）"""
    response = ds_client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content

def call_deepseek_code(ds_client, prompt):
    """调用 DeepSeek 生成代码"""
    return call_deepseek(ds_client, f"请生成以下任务的Python代码:\n{prompt}", max_tokens=3000)

def run_task(task, ds_client):
    task_id = task["id"]
    task_type = task["type"]
    prompt = task["prompt"]

    print(f"[EXECUTOR] Running {task_id} ({task_type})...")

    if task_type == "paper":
        content = call_deepseek(ds_client, prompt, max_tokens=2000)
        save(f"{RUNTIME_PATH}/paper_{task_id}.txt", content)
        squad_a.run(task, content)

    elif task_type == "code":
        code = call_deepseek_code(ds_client, prompt)
        save(f"{RUNTIME_PATH}/code_{task_id}.py", code)
        squad_b.run(task, code)

    elif task_type == "bug":
        fix = call_deepseek_code(ds_client, f"修复以下bug: {prompt}")
        save(f"{RUNTIME_PATH}/fix_{task_id}.py", fix)
        bugfix.run(task, fix)

def main_loop(ds_client):
    print("[EXECUTOR] Agent OS core loop running...")
    while True:
        queue = load(f"{RUNTIME_PATH}/queue.json")
        logs = load(f"{RUNTIME_PATH}/logs.json")

        pending_count = 0
        for task in queue:
            if task["status"] == "PENDING" and task.get("approved", False):
                pending_count += 1
                task["status"] = "RUNNING"
                save(f"{RUNTIME_PATH}/queue.json", queue)

                try:
                    run_task(task, ds_client)
                    task["status"] = "DONE"
                    logs.append({"task": task["id"], "status": "DONE", "type": task["type"]})
                except Exception as e:
                    task["status"] = "FAILED"
                    logs.append({"task": task["id"], "status": "FAILED", "error": str(e)})

                save(f"{RUNTIME_PATH}/queue.json", queue)
                save(f"{RUNTIME_PATH}/logs.json", logs)

        if pending_count == 0:
            all_done = all(t["status"] == "DONE" for t in queue)
            if all_done:
                print("[EXECUTOR] All tasks complete. Idling...")

        time.sleep(2)