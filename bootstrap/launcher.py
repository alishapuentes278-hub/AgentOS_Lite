import subprocess
import threading
import time
import sys
import json
import os
from openai import OpenAI

from core.executor import main_loop
from bootstrap.web_open import open_browser
from core.planner import generate_plan
from core.guard import PlanGuard

# ============================================================
# DeepSeek API 配置
# 优先从 .env 文件读取，未找到则使用默认值
# 获取 API Key: https://platform.deepseek.com/api_keys
# ============================================================

def _load_env():
    """从 .env 文件加载环境变量（简单实现，无外部依赖）"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ[key.strip()] = value.strip()

_load_env()

DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# 验证 API Key
if not DEEPSEEK_API_KEY:
    print("[ERROR] DEEPSEEK_API_KEY 未设置!")
    print("        方式1: cp .env.example .env  然后编辑 .env 填入你的 key")
    print("        方式2: 设置环境变量 DEEPSEEK_API_KEY=sk-xxx")
    print("        获取 Key: https://platform.deepseek.com/api_keys")
    sys.exit(1)

# OpenAI 兼容客户端（对接 DeepSeek 直连 API）
ds_client = OpenAI(
    base_url=DEEPSEEK_BASE_URL,
    api_key=DEEPSEEK_API_KEY,
)

RUNTIME_PATH = "runtime"

def init_runtime(topic="毕业设计项目"):
    os.makedirs(RUNTIME_PATH, exist_ok=True)
    plan = generate_plan(topic)
    with open(f"{RUNTIME_PATH}/plan.json", "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    with open(f"{RUNTIME_PATH}/dag.json", "w", encoding="utf-8") as f:
        json.dump(plan["dag"], f, indent=2, ensure_ascii=False)
    # 初始化队列
    queue = []
    for i, t in enumerate(plan["dag"].keys()):
        queue.append({
            "id": t,
            "type": "paper" if "T1" in t else "code",
            "status": "PENDING",
            "prompt": f"执行任务 {t}",
            "approved": False
        })
    with open(f"{RUNTIME_PATH}/queue.json", "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
    # 初始化日志
    with open(f"{RUNTIME_PATH}/logs.json", "w", encoding="utf-8") as f:
        json.dump([], f, indent=2, ensure_ascii=False)
    return plan

def approve_plan(plan):
    guard = PlanGuard()
    guard.load(plan)
    guard.approve()
    # 审批完成后把任务标记为 approved
    with open(f"{RUNTIME_PATH}/queue.json", "r", encoding="utf-8") as f:
        queue = json.load(f)
    for task in queue:
        task["approved"] = True
    with open(f"{RUNTIME_PATH}/queue.json", "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)

def start_executor():
    main_loop(ds_client)

def start_dashboard():
    subprocess.Popen([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "dashboard/app.py"
    ])

def start_system():
    print("[BOOT] Agent OS Lite starting...")
    print(f"       DeepSeek Model: {DEEPSEEK_MODEL}")
    print(f"       Endpoint: {DEEPSEEK_BASE_URL} (direct)")

    # 初始化计划
    plan = init_runtime()
    print("[PLAN] 计划已生成")

    # HITL审批
    approve_plan(plan)
    print("[HITL] 计划已审批")

    # 启动Executor
    t = threading.Thread(target=start_executor, daemon=True)
    t.start()

    time.sleep(1)

    # 启动Dashboard
    start_dashboard()
    time.sleep(2)
    open_browser()

    print("[OK] System running. Dashboard at http://localhost:8501")
    t.join()