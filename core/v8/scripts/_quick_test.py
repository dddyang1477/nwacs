import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from self_learning_engine import SelfLearningEngine, SkillLevel

e = SelfLearningEngine()
with open(os.path.join(os.path.dirname(__file__), "_quick_test.txt"), "w", encoding="utf-8") as f:
    f.write(f"Skills: {list(e.skills.keys())}\n")
    for k, s in e.skills.items():
        f.write(f"  {k}: level={s.level.value}, exp={s.experience}/{s.max_experience}\n")
    f.write("DONE\n")
print("DONE")
