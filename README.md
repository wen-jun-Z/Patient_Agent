# Patient Simulation Agent

医患对话模拟系统，使用 LLM 模拟医生和患者进行急诊科问诊对话。

## 功能特性

- 支持多种 LLM API（DeepSeek、Qwen、OpenAI、Azure OpenAI、Gemini、vLLM）
- 医生 Agent：问诊、收集信息、给出诊断
- 患者 Agent：模拟不同性格、语言水平、记忆能力的患者
- 完整的对话记录和 Token 统计

## 项目结构

```
src/
├── agent/              # Agent 实现
│   ├── doctor_agent.py
│   └── patient_agent.py
├── config/             # 配置文件
│   └── base.yaml
├── data/               # 数据文件
│   └── final_data/
│       └── patient_profile.json
├── prompts/            # Prompt 模板
│   └── simulation/
├── models.py           # LLM API 封装
├── run_simulation.py   # 主程序
└── utils.py            # 工具函数
```

## 快速开始

### 1. 环境变量设置

```bash
export DEEPSEEK_API_KEY="your_deepseek_key"
export QWEN_API_KEY="your_qwen_key"
export QWEN_BASE_URL="https://api.siliconflow.cn/v1"
```

### 2. 运行模拟

```bash
cd src
python run_simulation.py \
  data_dir=./data/final_data \
  prompt_dir=./prompts/simulation \
  patient_agent.api_type=qwen \
  patient_agent.backend="your_model" \
  doctor_agent.api_type=deepseek \
  doctor_agent.backend=deepseek-chat \
  experiment.total_inferences=5
```

## 配置说明

详细配置请参考 `src/config/base.yaml`

