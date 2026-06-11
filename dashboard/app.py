"""Agent OS Lite — Streamlit 实时监控 Dashboard"""
import streamlit as st
import json
import time
import os

RUNTIME_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "runtime")

def load(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {} if "dag" in path or "plan" in path else []

st.set_page_config(
    page_title="Agent OS Lite Dashboard",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Agent OS Lite — DeepSeek Dashboard")
st.caption(f"Model: deepseek-v4-pro | Endpoint: api.deepseek.com (direct)")

placeholder = st.empty()

while True:
    plan = load(f"{RUNTIME_PATH}/plan.json")
    dag = load(f"{RUNTIME_PATH}/dag.json")
    queue = load(f"{RUNTIME_PATH}/queue.json")
    logs = load(f"{RUNTIME_PATH}/logs.json")

    with placeholder.container():
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📋 PLAN")
            if plan:
                st.json(plan.get("paper", {}))
            else:
                st.info("等待计划生成...")

        with col2:
            st.subheader("🔗 DAG")
            if dag:
                st.json(dag)
            else:
                st.info("等待DAG...")

        with col3:
            st.subheader("📊 QUEUE")
            if queue:
                for task in queue:
                    icon = "✅" if task["status"] == "DONE" else ("🔄" if task["status"] == "RUNNING" else "⏳")
                    st.write(f"{icon} {task['id']} — {task['status']}")
            else:
                st.info("等待队列...")

        st.subheader("📝 LOGS")
        if logs:
            for log in logs[-20:]:
                st.write(f"[{log.get('task', '?')}] {log.get('status', '?')}")
        else:
            st.info("暂无日志")

    time.sleep(2)
    st.rerun()