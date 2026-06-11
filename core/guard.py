class PlanGuard:
    """HITL 人工审批门禁"""
    def __init__(self):
        self.plan = None
        self.locked = False

    def load(self, plan):
        self.plan = plan

    def approve(self):
        print("\n=== PLAN REVIEW ===")
        print(f"项目: {self.plan.get('project', 'unknown')}")
        print(f"论文章节: {self.plan.get('paper', {}).get('chapters', [])}")
        print(f"代码模块: {self.plan.get('code', {}).get('modules', [])}")
        print(f"DAG: {self.plan.get('dag', {})}")
        print("===================")
        ok = input("Approve plan? (yes/no): ")
        if ok.lower() != "yes":
            exit("Plan rejected by user")
        self.locked = True
        print("[GUARD] Plan approved. Executing...\n")

    def validate(self):
        if not self.locked:
            raise Exception("Plan not approved")