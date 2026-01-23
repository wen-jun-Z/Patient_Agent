"""
Streamlit Cloud 入口文件
直接运行 demo/demo.py 的代码
"""
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "src"))

# 读取并执行 demo.py（跳过 if __name__ == "__main__" 检查）
demo_path = os.path.join(project_root, "demo", "demo.py")
with open(demo_path, "r", encoding="utf-8") as f:
    code = f.read()
    # 替换 __name__ == "__main__" 为 True，确保页面配置被执行
    code = code.replace('if __name__ == "__main__":', 'if True:  # Streamlit Cloud entry point')
    exec(compile(code, demo_path, "exec"), {"__file__": demo_path, "__name__": "__main__"})
