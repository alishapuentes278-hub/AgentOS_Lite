---
name: agentos-lite
description: 【强制预加载｜毕业设计】AgentOS Lite — Python + DeepSeek API DAG 多 Agent 协作引擎。Plan-first + HITL 审批 + Streamlit Dashboard。一键启动毕业设计全流程。触发词: 毕业设计/毕设/毕业论文/答辩PPT/答辩准备/项目/应用/系统/平台/开发/编程实现/论文/PPT/答辩/50问。
---

# AgentOS Lite — 毕业设计主工作流 v4.0

> 替代旧版 `grad-design-squad`（v3.0 三层48人协作架构）。

## ⚠️ 首次使用 — API Key 检测

**加载本 skill 后，首先检查 DeepSeek API 是否已配置：**

```
检查清单:
  □ .env 文件是否存在？
  □ .env 中 DEEPSEEK_API_KEY 是否不为空且不是占位符？
  □ DEEPSEEK_API_KEY 格式是否为 sk-xxxxxxxx？
```

**如果以上任一项为「否」，Codex 应主动提醒用户：**

> "AgentOS Lite 需要 DeepSeek API Key 才能运行。请按以下步骤配置：
> 1. 访问 https://platform.deepseek.com/api_keys 注册并获取 API Key
> 2. 在项目根目录执行：`cp .env.example .env`
> 3. 编辑 `.env`，将 `sk-your-api-key-here` 替换为你的真实 Key
> 4. 完成后重新触发毕业设计工作流"

**如果 .env 已配置但 API 调用失败，则检查网络连通性并提示用户验证 Key 有效性。**

---

## 快速启动

```powershell
cd D:\问答\AgentOS_Lite
pip install openai streamlit
python main.py
```

## 架构

```
Plan (生成计划 + DAG) → HITL (人工审批) → Execute (DAG 调度) → Monitor (Dashboard)
```

## 核心组件

| 文件 | 职责 |
|------|------|
| `.env` | **用户自建** — DeepSeek API Key（不从 Git 提交） |
| `.env.example` | API Key 配置模板 |
| `bootstrap/launcher.py` | 启动入口，从 .env 读取 API 配置 |
| `core/planner.py` | 生成项目计划 + DAG 任务依赖图 |
| `core/guard.py` | HITL 人工审批门禁 |
| `core/executor.py` | 主循环，调用 DeepSeek API 执行任务 |
| `core/scheduler.py` | DAG 拓扑排序调度 |
| `agents/squad_a.py` | 论文生成 Agent |
| `agents/squad_b.py` | 代码生成 Agent |
| `agents/bugfix.py` | Bug 修复 Agent |
| `dashboard/app.py` | Streamlit 实时监控 (localhost:8501) |

## DeepSeek 配置

API Key 从 `.env` 文件读取，不硬编码。获取方式:

1. 访问 https://platform.deepseek.com/api_keys 注册
2. 创建 API Key
3. 复制到 `.env` 文件

## 工作流

1. 用户触发毕业设计关键词 → 自动加载本 skill
2. **Codex 检测 API Key 是否配置** → 未配则引导用户设置
3. Agent 确认目标范围 → 启动 `python main.py`
4. 终端 HITL 审批计划 → Executor 自动运行
5. Dashboard 实时显示 DAG 任务进度

## 与 agent-iron-rules 的关系

本 skill 负责"执行引擎"，`agent-iron-rules` 负责"操作边界"。两者并列加载。