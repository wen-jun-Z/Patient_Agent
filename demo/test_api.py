#!/usr/bin/env python3
"""测试 API 调用是否正常"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from openai import OpenAI

# 设置 API 密钥
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "sk-fclzckobrlffwetgkylgbbrnmlmvmdlvwtnbszleujiyuzkx")
QWEN_BASE_URL = "https://api.siliconflow.cn/v1"
MODEL = "Pro/zai-org/GLM-4.7"

print("=" * 50)
print("测试硅基流动 API 调用")
print("=" * 50)
print(f"API Key: {QWEN_API_KEY[:10]}...")
print(f"Base URL: {QWEN_BASE_URL}")
print(f"Model: {MODEL}")
print("=" * 50)

try:
    client = OpenAI(api_key=QWEN_API_KEY, base_url=QWEN_BASE_URL)
    
    print("\n正在发送测试请求...")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "你是一个有用的助手"},
            {"role": "user", "content": "你好，请简单介绍一下你自己"}
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    answer = response.choices[0].message.content
    print(f"\n✅ 成功！")
    print(f"回复: {answer}")
    print(f"\nToken 使用: {response.usage}")
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 50)
print("测试完成！")
print("=" * 50)
