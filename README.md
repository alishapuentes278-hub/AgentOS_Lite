# 🔧 AgentOS Lite

<div align="center">

**Python + DeepSeek API 驱动的 DAG 多 Agent 协作引擎**

一键启动毕业设计全流程：Plan → HITL 审批 → DAG 执行 → Dashboard 监控

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek%20v4-green.svg)](https://www.deepseek.com/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📖 目录

- [项目概述](#项目概述)
- [设计哲学](#设计哲学)
- [架构概览](#架构概览)
- [快速开始](#快速开始)
- [安装指南](#安装指南)
- [配置 DeepSeek API](#配置-deepseek-api)
- [完整使用流程](#完整使用流程)
- [项目结构](#项目结构)
- [核心模块详解](#核心模块详解)
  - [Planner — 计划生成器](#1-planner--计划生成器)
  - [Guard — HITL 审批门禁](#2-guard--hitl-审批门禁)
  - [Executor — 核心执行循环](#3-executor--核心执行循环)
  - [Scheduler — DAG 拓扑调度](#4-scheduler--dag-拓扑调度)
- [Agent 系统](#agent-系统)
- [Dashboard 实时监控](#dashboard-实时监控)
- [运行时状态文件](#运行时状态文件)
- [自定义与扩展](#自定义与扩展)
- [架构演进历史](#架构演进历史)
- [FAQ](#faq)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 项目概述

**AgentOS Lite** 是一个轻量级的 Python Agent 协作引擎。它用 DAG（有向无环图）管理多 Agent 任务依赖，通过 Plan-first + HITL（Human-in-the-Loop）审批确保执行质量，并提供 Streamlit Dashboard 实时监控任务进度。

核心场景：**自动化完成毕业设计的完整工作流**——论文写作、代码开发、Bug 修复三位一体，由 DeepSeek v4 AI 驱动所有内容生成。

### 核心能力

| 能力 | 说明 |
|------|------|
| 🤖 **多 Agent 协作** | Squad A (论文) + Squad B (代码) + BugFix (修复) |
| 📊 **DAG 任务调度** | 拓扑排序 + 依赖感知，自动按序执行 |
| 👤 **HITL 审批** | 执行前人工审核计划，Gate 不通过则阻断 |
| 📡 **DeepSeek API** | 直连 DeepSeek API，OpenAI 兼容协议 |
| 📈 **Streamlit Dashboard** | localhost:8501 实时监控任务状态 |
| 🔌 **一键启动** | python main.py 全自动运行 |

---

## 设计哲学

> "协议文档架构在读的场景下完美，但在跑的场景下死重。用可执行代码替代协议文档。"

AgentOS Lite v4.0 是其前身 grad-design-squad v3.0 的彻底重写：

| 维度 | v3.0 (旧) | v4.0 (新) |
|------|----------|----------|
| Agent 数量 | 48 个人物角色卡 | 3 个 Squad Agent |
| 编排方式 | TL→Squad Lead→Sub-Agent 三级 | Plan→HITL→Executor 主循环 |
| 门禁 | 17 道 Gate 检查点 | 1 道 HITL 审批 |
| 代码量 | ~32KB Markdown 协议 | ~14KB Python 可执行 |
| LLM | 无内置集成 | DeepSeek v4-pro |
| 启动 | 手动编排 | 一键 python main.py |

核心原则：**够用不复杂，可跑不纸上。**

---

## 架构概览

`mermaid
flowchart TD
    A["🚀 python main.py"] --> B["📋 Planner<br/>生成计划 + DAG"]
    B --> C{"👤 Guard<br/>HITL 审批"}
    C -->|"yes"| D["⚙️ Executor<br/>主循环运行"]
    C -->|"no"| X["❌ 终止"]
    D --> E["🤖 DeepSeek API<br/>生成内容"]
    E --> F["📝 Squad A<br/>论文 Agent"]
    E --> G["💻 Squad B<br/>代码 Agent"]
    E --> H["🔧 BugFix<br/>修复 Agent"]
    F --> I["📊 Dashboard<br/>Streamlit :8501"]
    G --> I
    H --> I
    I --> J{"任务全部完成?"}
    J -->|"否"| D
    J -->|"是"| K["✅ 完成"]
`

### 数据流

`
runtime/plan.json ──→ Executor ──→ runtime/queue.json
                         │
                    DeepSeek API
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         paper_T*.txt  code_T*.py  fix_T*.py
              │          │          │
              ▼          ▼          ▼
         runtime/logs.json ←───────┘
              │
              ▼
         Dashboard (实时读取)
`

---

## 快速开始

`ash
# 1. 克隆项目
git clone https://github.com/your-username/AgentOS-Lite.git
cd AgentOS-Lite

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 API Key
cp .env.example .env
# 编辑 .env 填入你的 DeepSeek API Key

# 4. 启动
python main.py
`

启动后：
- **终端**显示 HITL 审批提示，输入 yes 确认计划
- **浏览器**自动打开 http://localhost:8501 Dashboard
- Executor 开始按 DAG 顺序执行任务

---

## 安装指南

### 系统要求

- Python 3.10+
- pip
- 网络连接（访问 DeepSeek API）

### 依赖

`	xt
openai>=1.0.0      # DeepSeek API (OpenAI 兼容协议)
streamlit>=1.28.0  # 实时监控 Dashboard
`

### 安装步骤

```bash
# 创建虚拟环境 (推荐)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 安装
pip install -r requirements.txt
```

> ⚠️ **下一步必须配置 DeepSeek API Key，否则 AgentOS Lite 无法启动。**
> 见下方 [配置 DeepSeek API](#配置-deepseek-api)。

---

## 🔐 配置 DeepSeek API（首次使用必读）

> **本项目不含任何 API Key。** 你需要自己注册 DeepSeek 账号并获取 Key。代码中所有 API 调用均从 `.env` 文件读取，不会上传到 GitHub。

### 如果你在 Codex 中使用

AgentOS Lite 作为 Codex 强制性预加载 skill 时，**会自动检测 API Key 是否配置**。如果未配置，Codex 会直接提醒你：

> "AgentOS Lite 需要 DeepSeek API Key 才能运行。请按以下步骤配置：  
> 1. 访问 https://platform.deepseek.com/api_keys 注册并获取 API Key  
> 2. 在项目根目录执行：`cp .env.example .env`  
> 3. 编辑 `.env`，替换为你的真实 Key  
> 4. 完成后重新触发毕业设计工作流"

### 如果你在命令行中使用

```bash
# 1. 注册 DeepSeek 账号并获取 API Key
#    访问: https://platform.deepseek.com/api_keys

# 2. 创建 .env 文件
cp .env.example .env

# 3. 编辑 .env，填入你的 Key
#    DEEPSEEK_API_KEY=sk-你的真实Key

# 4. 启动
python main.py
```

### .env 文件格式

```env
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_API_KEY=sk-你的真实Key
```

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DEEPSEEK_MODEL` | 模型名称 | `deepseek-chat` |
| `DEEPSEEK_BASE_URL` | API 端点 | `https://api.deepseek.com` |
| `DEEPSEEK_API_KEY` | **必须填写** — 你的 API Key | (无) |

### 安装步骤

`ash
# 创建虚拟环境 (推荐)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 安装
pip install -r requirements.txt
`

---

## 完整使用流程

### Step 1: 启动

`ash
python main.py
`

`
[BOOT] Agent OS Lite starting...
       DeepSeek Model: deepseek-chat
       Endpoint: https://api.deepseek.com (direct)
[PLAN] 计划已生成
`

### Step 2: HITL 审批

`
=== PLAN REVIEW ===
项目: 毕业设计项目
论文章节: ['引言', '相关工作', '系统设计', '实现', '实验', '总结']
代码模块: ['core', 'agents', 'runtime']
DAG: {'T1': [], 'T2': ['T1'], 'T3': ['T2'], 'T4': ['T3']}
===================
Approve plan? (yes/no): yes
`

输入 yes → 开始执行。
o → 终止。

### Step 3: 自动执行

`
[GUARD] Plan approved. Executing...
[EXECUTOR] Agent OS core loop running...
[EXECUTOR] Running T1 (paper)...
[Squad A] 论文Agent: 已为 T1 生成内容 (1847 chars)
[EXECUTOR] Running T2 (code)...
[Squad B] 代码Agent: 已为 T2 生成代码 (156 lines)
[EXECUTOR] Running T3 (code)...
[Squad B] 代码Agent: 已为 T3 生成代码 (203 lines)
[EXECUTOR] Running T4 (paper)...
[Squad A] 论文Agent: 已为 T4 生成内容 (2103 chars)
[EXECUTOR] All tasks complete. Idling...
`

### Step 4: Dashboard 实时监控

浏览器访问 http://localhost:8501：

- 📋 **PLAN** — 论文结构 + 代码模块清单
- 🔗 **DAG** — 任务依赖关系图
- 📊 **QUEUE** — 每个任务的实时状态 (⏳ PENDING / 🔄 RUNNING / ✅ DONE)
- 📝 **LOGS** — 最近 20 条执行日志

### Step 5: 查看输出

`ash
# 生成的论文内容
cat runtime/paper_T1.txt

# 生成的代码
cat runtime/code_T2.py

# 执行日志
cat runtime/logs.json
`

---

## 项目结构

`
AgentOS_Lite/
├── main.py                    # 🚀 一键启动入口
├── requirements.txt           # 📦 Python 依赖
├── .env.example               # 🔐 API Key 配置模板
├── .gitignore                 # 🚫 Git 忽略规则
├── README.md                  # 📖 本文档
│
├── bootstrap/                 # 🏗️ 启动层
│   ├── __init__.py
│   ├── launcher.py            # 系统启动 + DeepSeek API 配置
│   └── web_open.py            # 自动打开浏览器
│
├── core/                      # ⚙️ 核心引擎
│   ├── __init__.py
│   ├── planner.py             # 生成项目计划 + DAG
│   ├── guard.py               # HITL 人工审批门禁
│   ├── executor.py            # Agent OS 主循环 + DeepSeek 调用
│   └── scheduler.py           # DAG 拓扑排序调度
│
├── agents/                    # 🤖 Agent 层
│   ├── __init__.py
│   ├── squad_a.py             # 论文生成 Agent
│   ├── squad_b.py             # 代码生成 Agent
│   └── bugfix.py              # Bug 修复 Agent
│
├── dashboard/                 # 📊 可视化层
│   └── app.py                 # Streamlit 实时监控 Dashboard
│
└── runtime/                   # 💾 运行时状态 (gitignored)
    ├── plan.json              # 当前项目计划
    ├── dag.json               # 任务依赖图
    ├── queue.json             # 任务队列 + 状态
    └── logs.json              # 执行日志
`

---

## 核心模块详解

### 1. Planner — 计划生成器

core/planner.py — 定义项目的任务结构和 DAG 依赖。

`python
def generate_plan(topic):
    return {
        "project": topic,
        "paper": {
            "chapters": ["引言", "相关工作", "系统设计", "实现", "实验", "总结"]
        },
        "code": {
            "modules": ["core", "agents", "runtime"]
        },
        "dag": {
            "T1": [],        # 无依赖，最先执行
            "T2": ["T1"],    # 依赖 T1
            "T3": ["T2"],    # 依赖 T2
            "T4": ["T3"]     # 依赖 T3
        }
    }
`

**扩展方式**: 修改 generate_plan() 返回结构即可自定义任务。

---

### 2. Guard — HITL 审批门禁

core/guard.py — 人工审批关卡，阻止错误计划进入执行。

`
流程图:
  Plan 生成 → 终端展示计划摘要 → 用户输入 yes/no
    ├─ yes → locked=True → Executor 启动
    └─ no  → exit("Plan rejected")
`

PlanGuard.validate() 在执行前检查 locked 状态，未审批则抛异常。

---

### 3. Executor — 核心执行循环

core/executor.py — AgentOS 的心脏。

**主循环**:
`
while True:
    queue = load("runtime/queue.json")
    for task in queue:
        if task["status"] == "PENDING" and task["approved"]:
            task["status"] = "RUNNING"
            run_task(task, ds_client)  # 调用 DeepSeek API
            task["status"] = "DONE"
    time.sleep(2)
`

**任务路由**:
| task["type"] | 调用的 API | 输出文件 | Agent |
|---|---|---|---|
| "paper" | call_deepseek(prompt, max_tokens=2000) | paper_{id}.txt | squad_a |
| "code" | call_deepseek_code(prompt) | code_{id}.py | squad_b |
| "bug" | call_deepseek_code(fix_prompt) | ix_{id}.py | bugfix |

**DeepSeek API 调用**:
`python
def call_deepseek(ds_client, prompt, max_tokens=2000):
    response = ds_client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content
`

---

### 4. Scheduler — DAG 拓扑调度

core/scheduler.py — 两个核心功能:

**	opological_sort(dag)**: Kahn 算法返回 DAG 合法执行顺序。
`
{"T1": [], "T2": ["T1"], "T3": ["T2"], "T4": ["T3"]}
→ ["T1", "T2", "T3", "T4"]
`

**get_ready_tasks(queue, dag)**: 返回"依赖已满足 + 状态为 PENDING"的待执行任务。

---

## Agent 系统

### Squad A — 论文 Agent
- 负责论文各章节的内容生成
- 输出: untime/paper_{task_id}.txt

### Squad B — 代码 Agent
- 负责系统代码的生成
- 输出: untime/code_{task_id}.py

### BugFix Squad — Bug 修复 Agent
- 专门处理 Bug 修复请求
- 输出: untime/fix_{task_id}.py

### 扩展 Agent

每个 Agent 按统一契约实现，添加新 Agent 只需三步:

`python
# agents/squad_c.py
def run(task, content):
    task_id = task["id"]
    # 你的处理逻辑
    return {"task_id": task_id, "squad": "C", "result": "..."}

# 然后在 executor.py 中添加路由:
elif task["type"] == "my_type":
    from agents import squad_c
    squad_c.run(task, content)
`

---

## Dashboard 实时监控

基于 **Streamlit**，零前端代码，纯 Python 实现。

`
http://localhost:8501
`

### 监控面板布局

`
┌──────────────────────────────────────────────────────┐
│  🔧 AgentOS Lite — DeepSeek Dashboard                │
│  Model: deepseek-chat | Endpoint: api.deepseek.com   │
├──────────────────┬──────────────────┬────────────────┤
│  📋 PLAN         │  🔗 DAG          │  📊 QUEUE      │
│  论文章节清单     │  任务依赖关系     │  ⏳ T1 PENDING │
│  代码模块清单     │  T1→T2→T3→T4    │  ⏳ T2 PENDING │
│                  │                  │  ⏳ T3 PENDING │
│                  │                  │  ⏳ T4 PENDING │
├──────────────────┴──────────────────┴────────────────┤
│  📝 LOGS (最近 20 条)                                │
│  [T1] DONE  [T2] RUNNING  [T3] PENDING  ...        │
└──────────────────────────────────────────────────────┘
`

### 实现要点

- st.rerun() 每 2 秒自动刷新
- 直接读取 untime/*.json 获取最新状态
- 三栏布局 st.columns(3) 展示 Plan/DAG/Queue
- 任务状态用 emoji 可视化: ⏳ / 🔄 / ✅ / ❌

---

## 运行时状态文件

untime/ 目录下的 JSON 文件是 AgentOS 的状态总线：

### plan.json
`json
{
  "project": "毕业设计项目",
  "paper": {"chapters": ["引言", "..."] },
  "code": {"modules": ["core", "..."] },
  "dag": {"T1": [], "T2": ["T1"], "T3": ["T2"], "T4": ["T3"]}
}
`

### queue.json
`json
[
  {"id": "T1", "type": "paper", "status": "DONE", "prompt": "...", "approved": true},
  {"id": "T2", "type": "code", "status": "RUNNING", "prompt": "...", "approved": true}
]
`

### logs.json
`json
[
  {"task": "T1", "status": "DONE", "type": "paper"},
  {"task": "T2", "status": "FAILED", "error": "Connection timeout"}
]
`

> ⚠️ untime/ 已被 .gitignore 排除，不会提交到 Git。

---

## 自定义与扩展

### 修改项目结构

编辑 core/planner.py 的 generate_plan():

`python
def generate_plan(topic):
    return {
        "project": topic,
        "paper": {"chapters": ["第1章", "第2章", ...]},
        "code": {"modules": ["module1", ...]},
        "dag": {"T1": [], "T2": ["T1"], ...}  # 定义依赖
    }
`

### 添加新任务类型

1. 在 core/executor.py 的 un_task() 中添加:
`python
elif task["type"] == "my_type":
    result = call_deepseek(ds_client, prompt, max_tokens=4000)
    save(f"{RUNTIME_PATH}/my_{task_id}.json", result)
`

2. 在 ootstrap/launcher.py 的 init_runtime() 中注册任务:
`python
queue.append({
    "id": "T5", "type": "my_type",
    "status": "PENDING", "prompt": "...", "approved": False
})
`

### 切换 LLM 提供商

任何 OpenAI 兼容的 API 都可以用——只需修改 ootstrap/launcher.py:

`python
# Claude (via Anthropic)
DEEPSEEK_BASE_URL = "https://api.anthropic.com/v1"  # 需要兼容网关

# 本地模型 (Ollama)
DEEPSEEK_BASE_URL = "http://localhost:11434/v1"
DEEPSEEK_MODEL = "llama3"

# 其他国产模型
DEEPSEEK_BASE_URL = "https://api.moonshot.cn/v1"
DEEPSEEK_MODEL = "moonshot-v1-8k"
`

---

## 架构演进历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v3.0 | 2026-06-08 | grad-design-squad: 48 Agent 三层协作架构，纯协议文档 |
| v4.0 | 2026-06-11 | AgentOS Lite: DAG + DeepSeek API + Streamlit，可执行 Python |

---

## FAQ

### Q: 如何修改论文的默认章节？
编辑 core/planner.py 中 generate_plan() 的 chapters 列表。

### Q: 运行时状态保存在哪里？
untime/ 目录下的 JSON 文件。所有 Agent 通过共享这些文件通信。

### Q: 如何重置所有任务？
删除 untime/queue.json 和 untime/logs.json，重新运行 python main.py。

### Q: 任务执行失败怎么办？
Executor 捕获异常后标记任务为 FAILED，日志写入 logs.json，然后继续处理下一个任务。

### Q: 可以在无网络环境下运行吗？
可以。将 DEEPSEEK_BASE_URL 指向本地模型（如 Ollama http://localhost:11434/v1）。

### Q: 如何处理大型项目 (>20 个任务)？
修改 core/planner.py 增加更多 DAG 节点 + 在 init_runtime() 中注册对应任务即可。

### Q: 为什么叫 "AgentOS Lite"？
"AgentOS" = Agent Operating System，"Lite" = 轻量。相比前身 v3.0 的 48 角色协议文档（只读不跑），v4.0 是真正可执行的轻量引擎。

---

## 贡献指南

欢迎提交 Issue 和 Pull Request。

### 开发环境搭建

`ash
git clone https://github.com/your-username/AgentOS-Lite.git
cd AgentOS-Lite
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
`

### 代码风格

- 遵循 PEP 8
- 函数/类添加 docstring
- 提交前确保 python main.py 可正常运行

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE) 文件。

---

<div align="center">

**Made with ❤️ for graduation design automation**

</div>