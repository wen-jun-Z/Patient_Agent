import os
import time
import json
import datetime
from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAI

# 可选导入 Google GenAI（仅在使用 Gemini API 时需要）
try:
    from google import genai
    from google.genai import types
    from google.genai.types import HttpOptions
    GOOGLE_GENAI_AVAILABLE = True
except ImportError:
    GOOGLE_GENAI_AVAILABLE = False
    genai = None
    types = None
    HttpOptions = None

# load_dotenv(override=True)
GENAI_API_KEY = os.environ.get("GENAI_API_KEY", "")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY", "")
AZURE_ENDPOINT = os.environ.get("AZURE_ENDPOINT", "")
PORT = os.environ.get("VLLM_PORT", "")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "./google_credentials.json")

azure_client = None
if AZURE_OPENAI_KEY != "":
    azure_client = AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version="2024-10-21",
    )

gen_client = None
if GENAI_API_KEY != "" and GOOGLE_GENAI_AVAILABLE:
    gen_client = genai.Client(vertexai=True, api_key=GENAI_API_KEY, http_options=HttpOptions(api_version="v1"))

# ======= 【插入】标准 OpenAI 兼容客户端初始化 (兼容 DeepSeek/Qwen/OpenAI) =======
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
QWEN_API_KEY = os.environ.get("QWEN_API_KEY", "")
QWEN_BASE_URL = os.environ.get("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

standard_client = None
if OPENAI_API_KEY:
    standard_client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
elif DEEPSEEK_API_KEY:
    standard_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
elif QWEN_API_KEY:
    standard_client = OpenAI(api_key=QWEN_API_KEY, base_url=QWEN_BASE_URL)
# ======================================================================
time_gap = {"gpt-4": 3}


def get_answer(response):
    if hasattr(response, "choices"):
        answer = response.choices[0].message.content
    elif hasattr(response, "text"):
        answer = response.text.strip()
    else:
        raise NotImplementedError(f"Fail to extract answer: {answer}")
    if "</think>" in answer:
        answer = answer.split("</think>")[-1].replace("<think>", "").replace("\n", "").strip()
    return answer


def get_token_log(response):
    token_usage = {}
    if hasattr(response, "usage"):
        token_usage["prompt_tokens"] = response.usage.prompt_tokens
        token_usage["completion_tokens"] = response.usage.completion_tokens
        token_usage["total_tokens"] = response.usage.total_tokens
        if hasattr(response.usage, "completion_tokens_details"):  # for gpt-5 series
            if hasattr(response.usage.completion_tokens_details, "reasoning_tokens"):
                token_usage["extra_info"] = {"reasoning_tokens": response.usage.completion_tokens_details.reasoning_tokens}
    elif hasattr(response, "usage_metadata"):
        token_usage["prompt_tokens"] = response.usage_metadata.prompt_token_count
        token_usage["completion_tokens"] = response.usage_metadata.candidates_token_count
        token_usage["total_tokens"] = response.usage_metadata.total_token_count
    else:
        raise NotImplementedError(f"Fail to extract usage data: {response}")
    return token_usage
    

def gpt_azure_response(message: list, model="gpt-4o", temperature=0, seed=42, **kwargs):
    time.sleep(time_gap.get(model, 3))
    try:
        return azure_client.chat.completions.create(model=model, messages=message, temperature=temperature, seed=seed, **kwargs)
    except Exception as e:
        error_msg = str(e).lower()
        if "context" in error_msg or "length" in error_msg:
            if isinstance(message, list) and len(message) > 2:
                message = [message[0]] + message[2:]
        print(e)
        time.sleep(time_gap.get(model, 3) * 2)
        return gpt_azure_response(model=model, messages=message, temperature=temperature, seed=seed, **kwargs)


def gemini_response(message: list, model="gemini-2.0-flash", temperature=0, seed=42, **kwargs):
    if not GOOGLE_GENAI_AVAILABLE or gen_client is None:
        raise ImportError("Google GenAI is not available. Please install google-genai package or use a different API.")
    
    time.sleep(time_gap.get(model, 3))
    system_prompt = message[0]["content"] if message[0]["role"] == "system" else None
    if system_prompt:
        contents = message[1:]
    else:
        contents = message

    try:
        contents = [{"role": item["role"], "parts": [{"text": item["content"]}]} for item in contents]
    except:
        raise NotImplementedError

    try:
        if model == "gemini-2.5-flash":
            return gen_client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=temperature,
                    seed=seed,
                    thinking_config=types.ThinkingConfig(thinking_budget=kwargs.get("thinking_budget", 0))
                ),
            )
        else:
            return gen_client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=temperature,
                    seed=seed,
                ),
            )

    except Exception as e:
        error_msg = str(e).lower()
        if "context" in error_msg or "length" in error_msg or 'maximum context length' in error_msg:
            if isinstance(message, list) and len(message) > 2:
                message = [message[0]] + message[2:]
        print(e)
        time.sleep(time_gap.get(model, 3) * 2)
        return gemini_response(message, model, temperature, seed, **kwargs)


def vllm_model_setup(model):
    if model == "vllm-llama3-70b-instruct":
        model = "meta-llama/Llama-3-70B-Instruct"
    elif model == "vllm-llama3-8b-instruct":
        model = "meta-llama/Llama-3-8B-Instruct"
    elif model == "vllm-llama3.1-8b-instruct":
        model = "meta-llama/Llama-3.1-8B-Instruct"
    elif model == "vllm-llama3.1-70b-instruct":
        model = "meta-llama/Llama-3.1-70B-Instruct"
    elif model == "vllm-llama3.3-70b-instruct":
        model = "meta-llama/Llama-3.3-70B-Instruct"
    elif model == "vllm-qwen2.5-72b-instruct":
        model = "Qwen/Qwen2.5-72B-Instruct"
    elif model == "vllm-qwen2.5-7b-instruct":
        model = "Qwen/Qwen2.5-7B-Instruct"
    elif model == "vllm-deepseek-llama-70b":
        model = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"
    else:
        raise ValueError(f"Invalid model: {model}")
    return model


def vllm_response(message: list, model=None, temperature=0, seed=42, **kwargs):
    VLLM_API_KEY = "EMPTY"
    VLLM_API_BASE = f"http://localhost:{PORT}/v1"
    vllm_client = OpenAI(api_key=VLLM_API_KEY, base_url=VLLM_API_BASE)

    assert model in [
        "meta-llama/Llama-3-70B-Instruct",
        "meta-llama/Llama-3-8B-Instruct",
        "meta-llama/Llama-3.1-8B-Instruct",
        "meta-llama/Llama-3.1-70B-Instruct",
        "meta-llama/Llama-3.3-70B-Instruct",
        "Qwen/Qwen2.5-72B-Instruct",
        "Qwen/Qwen2.5-7B-Instruct",
        "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
    ]
    time.sleep(time_gap.get(model, 3))

    try:
        return vllm_client.chat.completions.create(
            model=model,
            messages=message,
            temperature=temperature,
            seed=seed,
        )
    except Exception as e:
        error_msg = str(e).lower()
        if "context" in error_msg or "length" in error_msg or 'maximum context length' in error_msg:
            if isinstance(message, list) and len(message) > 2:
                message = [message[0]] + message[2:]
        print(e)
        time.sleep(time_gap.get(model, 3) * 2)
        return vllm_response(message, model, temperature, seed)

# ======= 【插入】处理 DeepSeek/OpenAI 请求的函数 =======
def standard_openai_response(message: list, model="gpt-4o", temperature=0, seed=42, api_key=None, base_url=None, **kwargs):
    """
    支持按调用传入 api_key/base_url，避免多 Agent 共享同一客户端时串线。
    同时移除 kwargs 中的 model，防止重复传参报错。
    """
    # 统一获取/覆盖模型名，防止重复传参导致 multiple values
    model = kwargs.pop("model", model)
    # 从 kwargs 中提取 temperature 和 seed（如果存在）
    temperature = kwargs.pop("temperature", temperature)
    seed = kwargs.pop("seed", seed)
    time.sleep(time_gap.get(model, 1))  # 稍微休眠一下防止超频
    
    # 选择客户端：优先使用调用传入的 api_key/base_url，否则用全局 standard_client
    client = standard_client
    if api_key or base_url:
        client = OpenAI(
            api_key=api_key or getattr(standard_client, "api_key", None),
            base_url=base_url or getattr(standard_client, "base_url", None),
        )

    # DeepSeek 兼容：如果 base_url 指向 deepseek 且模型名是 gpt 系列，自动改名
    if client and "deepseek" in str(client.base_url) and "gpt" in model:
        model = "deepseek-chat"
        
    try:
        return client.chat.completions.create(
            model=model, 
            messages=message, 
            temperature=temperature, 
            seed=seed, 
            **kwargs,
        )
    except Exception as e:
        print(f"Standard OpenAI Error: {e}")
        time.sleep(2)
        return standard_openai_response(message, model, temperature, seed, api_key=api_key, base_url=base_url, **kwargs)
# ========================================================
def get_response_method(model):
    response_methods = {
    "gpt_azure": gpt_azure_response,
    "vllm": vllm_response,
    "genai": gemini_response,
    "gpt": standard_openai_response,
        "deepseek": standard_openai_response,
        "qwen": standard_openai_response,
}
    return response_methods.get(model.split("-")[0], lambda _: NotImplementedError())
