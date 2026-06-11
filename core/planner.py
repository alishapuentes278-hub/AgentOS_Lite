def generate_plan(topic):
    """生成项目计划 + DAG 任务依赖图"""
    return {
        "project": topic,
        "paper": {
            "chapters": ["引言", "相关工作", "系统设计", "实现", "实验", "总结"]
        },
        "code": {
            "modules": ["core", "agents", "runtime"]
        },
        "dag": {
            "T1": [],
            "T2": ["T1"],
            "T3": ["T2"],
            "T4": ["T3"]
        }
    }