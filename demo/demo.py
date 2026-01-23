import os
import sys
import json
import random
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

from datetime import datetime 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from run_simulation import PatientAgent

# Get the directory where this script is located
DEMO_DIR = os.path.dirname(os.path.abspath(__file__))

# Custom CSS for modern styling
def inject_custom_css():
    st.markdown("""
    <style>
    /* Main page styling */
    .main {
        padding: 2rem 1rem;
    }
    
    /* Title styling */
    h1 {
        color: #1f4788;
        font-weight: 700;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #4a90e2;
        padding-bottom: 0.5rem;
    }
    
    h3 {
        color: #2c3e50;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Selectbox and radio styling */
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    /* Radio button styling */
    .stRadio > div {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e9ecef;
    }
    
    .stRadio > div > label {
        font-weight: 500;
        color: #495057;
    }
    
    /* Form input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #dee2e6;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Card-like containers */
    .info-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* Error message styling */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #dc3545;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #667eea;
    }
    </style>
    """, unsafe_allow_html=True)



# ======= 插入开始 =======
import os
from openai import OpenAI

# 初始化客户端 (仅在环境变量存在时初始化，避免报错)
gen_client = None
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL")

if openai_api_key:
    gen_client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_base_url
    )
# ======= 插入结束 =======

CEFR_DICT = {
    "A": "Beginner\n\tCan make simple sentences.",
    "B": "Intermediate\n\tCan have daily conversations.",
    "C": "Advanced\n\tCan freely use even advanced medical terms.",
}

PERSONALITY_DICT = {
    "plain": "Neutral\n\tNo strong emotions or noticeable behavior.",
    "verbose": "Talkative\n\tSpeaks a lot, and provides highly detailed responses.",
    "distrust": "Distrustful\n\tQuestions the doctor’s expertise and care.",
    "pleasing": "Pleasing\n\tOverly positive and tend to minimize their problems.",
    "impatient": "Impatient\n\tEasily irritated and lacks patience.",
    "overanxious": "Overanxious\n\tExpresses concern beyond what is typical.",
}

RECALL_DICT = {"low": "\n\tOften forgetting even major medical events.", "high": "\n\tUsually recalls their medical events accurately."}

DAZED_DICT = {
    "normal": "\n\tClear mental status, with naturally reflect their own persona.",
    "high": "\n\tHighly dazed and extremely confused, struggle with conversation.",
}

###########################
# Helper Functions
###########################
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)


@st.cache_data
def load_patient_info(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        patient_info = json.load(f)
    return patient_info


# Styling functions with modern design
def stylize_text(
    text: str,
    font_size: int = 14,
    color: str = "#2c3e50",
    bg_color: str = "#ffffff",
    border_color: str = "#e0e0e0",
    line_height: float = 1.6,
    min_height: str = None,
) -> str:
    text = text.replace("\n", "<br>").replace("\t", "&emsp;")
    style = (
        f"font-size:{font_size}px; color:{color}; background: linear-gradient(135deg, {bg_color} 0%, #f8f9fa 100%); "
        f"border-radius:12px; padding:20px; "
        f"border:2px solid {border_color}; line-height:{line_height}; "
        f"box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"
    )
    if min_height:
        style += f" min-height:{min_height};"
    return f"<div style='{style}'>{text}</div>"


# Function to add a message to chat history
def add_message(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})


# Function to render chat history as HTML with modern styling
def render_chat_html():
    chat_history = st.session_state.get("chat_history", [])
    if not chat_history:
        html_content = """
        <div style="text-align: center; padding: 2rem; color: #6c757d;">
            <h3 style="color: #495057; margin-bottom: 1rem;">💬 Consultation History</h3>
            <p style="font-style: italic;">No messages yet. Start the conversation!</p>
        </div>
        """
    else:
        html_content = """
        <div style="margin-bottom: 1.5rem;">
            <h3 style="color: #1f4788; border-bottom: 2px solid #4a90e2; padding-bottom: 0.5rem; margin-bottom: 1rem;">
                💬 Consultation History
            </h3>
        </div>
        """
        for idx, msg in enumerate(chat_history):
            if msg["role"] == "Doctor":
                html_content += f"""
                <div style="margin-bottom: 1.5rem; padding: 1rem; background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                            border-radius: 12px; border-left: 4px solid #2196f3; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <span style="background: #2196f3; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; 
                                     font-weight: 600; font-size: 12px; margin-right: 0.5rem;">👨‍⚕️ DOCTOR</span>
                    </div>
                    <p style="margin: 0; color: #1565c0; line-height: 1.6;">{msg['content']}</p>
                </div>
                """
            elif msg["role"] == "Patient":
                html_content += f"""
                <div style="margin-bottom: 1.5rem; padding: 1rem; background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                            border-radius: 12px; border-left: 4px solid #ff9800; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <span style="background: #ff9800; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; 
                                     font-weight: 600; font-size: 12px; margin-right: 0.5rem;">👤 PATIENT</span>
                    </div>
                    <p style="margin: 0; color: #e65100; line-height: 1.6;">{msg['content']}</p>
                </div>
                """
            else:
                html_content += f"""
                <div style="margin-bottom: 1rem; padding: 0.75rem; background: #f5f5f5; border-radius: 8px;">
                    <strong style="color: #666;">{msg['role']}:</strong>
                    <span style="color: #333;">{msg['content']}</span>
                </div>
                """
    return html_content


# Reset the session state keys
def reset_to_patient_selection():
    keys_to_keep = {"logged_in", "labeler"}
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            st.session_state.pop(key, None)
    st.rerun()  

###########################
# Page Functions
###########################
# 1. Patient selection page with modern styling
def patient_selection_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                   font-size: 2.5rem; margin-bottom: 0.5rem;">🏥 Patient Profile Configuration</h1>
        <p style="color: #6c757d; font-size: 1.1rem;">Configure patient information and persona for simulation</p>
    </div>
    """, unsafe_allow_html=True)
    
    demo_data_path = os.path.join(DEMO_DIR, "demo_data.json")
    patient_info_list = load_patient_info(demo_data_path)
    patient_info_dict = {str(info["hadm_id"]): info for info in patient_info_list}

    display_options_to_hadm = {}  # mapping: "age:..../gender:.../disease:..." → patient info
    for hadm_id in sorted(patient_info_dict.keys()):
        info = patient_info_dict[hadm_id]
        display_str = f"age: {info['age']} / gender: {info['gender']} / disease: {info.get('diagnosis', 'Unknown')}"
        display_options_to_hadm[display_str] = hadm_id

    # Select box to show results with card styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h3 style="color: #1f4788; margin-top: 0;">👤 Select a Patient</h3>
    </div>
    """, unsafe_allow_html=True)
    
    selected_display = st.selectbox("Select Patient", display_options_to_hadm.keys(), label_visibility="collapsed")
    base_patient = patient_info_dict[display_options_to_hadm[selected_display]]

    st.markdown("""
    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                padding: 1.5rem; border-radius: 12px; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h3 style="color: #1f4788; margin-top: 0;">⚙️ Customize Patient Persona</h3>
    </div>
    """, unsafe_allow_html=True)

    cefr = st.radio(
        "📚 Select CEFR Level", 
        options=list(CEFR_DICT.keys()), 
        format_func=lambda k: f"{k.capitalize()} : {CEFR_DICT[k]}",
        horizontal=False
    )

    personality = st.radio(
        "🎭 Select Personality", 
        options=list(PERSONALITY_DICT.keys()), 
        format_func=lambda k: f"{k.capitalize()}: {PERSONALITY_DICT[k]}",
        horizontal=False
    )

    recall_level = st.radio(
        "🧠 Select Recall Level", 
        options=list(RECALL_DICT.keys()), 
        format_func=lambda k: f"{k.capitalize()}: {RECALL_DICT[k]}",
        horizontal=False
    )

    dazed_level = st.radio(
        "😵 Select Dazed Level", 
        options=list(DAZED_DICT.keys()), 
        format_func=lambda k: f"{k.capitalize()}: {DAZED_DICT[k]}",
        horizontal=False
    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Simulation", use_container_width=True, type="primary"):
            base_patient["cefr"] = cefr
            base_patient["personality"] = personality
            base_patient["recall_level"] = recall_level
            base_patient["dazed_level"] = dazed_level

            st.session_state.selected_patient = base_patient
            st.rerun()


# 2. Demo Page (ED Consultation Simulation) with modern styling
def demo_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                   font-size: 2.5rem; margin-bottom: 0.5rem;">🏥 ED Consultation Simulation</h1>
        <p style="color: #6c757d; font-size: 1.1rem;">Interactive patient-doctor dialogue simulation</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected_patient_profile = st.session_state.get("selected_patient", None)

    if selected_patient_profile is None:
        st.error("No patient selected. Please go back to the patient selection page.")
        if st.button("Go to Patient Selection"):
            reset_to_patient_selection()
        return
    
    # Build a config dictionary based on the selected labeler.
    config_path = os.path.join(DEMO_DIR, "config.json")
    with open(config_path, "r") as f:
        config = json.load(f)

    # Fix prompt_dir path - convert relative path to absolute path
    if config.get("prompt_dir", "").startswith("../"):
        # Relative path from demo/ to src/prompts/simulation
        prompt_dir_relative = config["prompt_dir"]
        # Get project root (parent of demo/)
        project_root = os.path.dirname(DEMO_DIR)
        # Convert to absolute path
        config["prompt_dir"] = os.path.abspath(os.path.join(project_root, prompt_dir_relative.replace("../", "")))
    elif not os.path.isabs(config.get("prompt_dir", "")):
        # If it's a relative path but doesn't start with ../
        config["prompt_dir"] = os.path.abspath(os.path.join(DEMO_DIR, config["prompt_dir"]))

    # Load patient basic information
    set_seed(config["random_seed"])

    # Initialize session state keys if they do not exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


    if "patient_agent" not in st.session_state:
        # Load patient basic info for initialization
        import copy
        selected_patient = copy.deepcopy(selected_patient_profile)
        
        # 使用 patient 配置块
        patient_config = config.get("patient", {})
        patient_model = patient_config.get("model_name", config.get("model", "qwen-max"))
        patient_api_type = patient_config.get("api_type", config.get("backend_api_type", "qwen"))
        patient_temperature = patient_config.get("temperature", 0.7)
        patient_api_base = patient_config.get("api_base", "https://api.siliconflow.cn/v1")
        
        # 获取 API key（从环境变量）
        qwen_api_key = os.getenv("QWEN_API_KEY", "")
        if not qwen_api_key:
            st.error("❌ 错误：未设置 QWEN_API_KEY 环境变量！")
            st.info("💡 请在服务器上运行以下命令设置环境变量：\n```bash\nexport QWEN_API_KEY='你的API密钥'\n```")
            st.stop()
        
        # 构建 client_params，包含 API 配置
        # 注意：函数参数名是 seed，不是 random_seed
        client_params = {
            "temperature": patient_temperature,
            "seed": config["random_seed"],  # 改为 seed，匹配函数参数名
            "api_key": qwen_api_key,
            "base_url": patient_api_base,
        }
        
        # 显示配置信息（调试用）
        with st.expander("🔍 查看患者代理配置（调试）", expanded=False):
            st.json({
                "patient_model": patient_model,
                "patient_api_type": patient_api_type,
                "patient_temperature": patient_temperature,
                "patient_api_base": patient_api_base,
                "api_key_set": bool(qwen_api_key),
                "api_key_prefix": qwen_api_key[:10] + "..." if qwen_api_key else "未设置",
                "client_params": {k: (v[:20] + "..." if isinstance(v, str) and len(v) > 20 else v) for k, v in client_params.items()}
            })
        
        st.session_state.patient_agent = PatientAgent(
            patient_profile=selected_patient,
            backend_str=patient_model,
            backend_api_type=patient_api_type,
            prompt_dir=config["prompt_dir"],
            prompt_file=config["patient_prompt_file"],
            num_word_sample=10,
            cefr_type=selected_patient["cefr"],
            personality_type=selected_patient["personality"],
            recall_level_type=selected_patient["recall_level"],
            dazed_level_type=selected_patient["dazed_level"],
            client_params=client_params,
        )


    top_cols = st.columns([3, 1])
    with top_cols[-1]:
        if st.button("Return to Patient Selection", use_container_width=True):
            reset_to_patient_selection()

    # Layout: Two columns (left for patient info, right for conversation)
    cols = st.columns([2, 3])
    patient_info_height = st.sidebar.slider("Adjust Patient Info Height", min_value=400, max_value=1000, value=650)
    with cols[0]:
        basic_info_html = f"""
        <div style="margin-bottom: 1.5rem; padding: 1rem; background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin-top: 0px; margin-bottom: 1rem; color: #1565c0; border-bottom: 2px solid #2196f3; padding-bottom: 0.5rem;">
                📋 Patient's Basic Information
            </h3>
            <div style="line-height: 2;">
                <div style="margin-bottom: 0.75rem;">
                    <span style="font-weight: 600; color: #1976d2;">👤 Age:</span> 
                    <span style="color: #424242;">{selected_patient_profile.get('age', 'N/A')}</span>
                </div>
                <div style="margin-bottom: 0.75rem;">
                    <span style="font-weight: 600; color: #1976d2;">⚧️ Gender:</span> 
                    <span style="color: #424242;">{selected_patient_profile.get('gender', 'N/A')}</span>
                </div>
                <div style="margin-bottom: 0.75rem;">
                    <span style="font-weight: 600; color: #1976d2;">🚑 Arrival transport:</span> 
                    <span style="color: #424242;">{selected_patient_profile.get('arrival_transport', 'N/A')}</span>
                </div>
            </div>
        </div>
        """
        persona_html = f"""
        <div style="margin-bottom: 0px; margin-top: 1rem; padding: 1rem; background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                    border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); line-height:1.6;">
            <h3 style="margin-top: 0px; margin-bottom: 1rem; color: #e65100; border-bottom: 2px solid #ff9800; padding-bottom: 0.5rem;">
                🎭 Patient's Persona
            </h3>
            <div style="line-height: 2;">
                <div style="margin-bottom: 0.75rem;">
                    <span style="font-weight: 600; color: #f57c00;">📚 Language proficiency:</span> 
                    <span style="color: #424242;">{CEFR_DICT[selected_patient_profile.get('cefr', 'N/A')]}</span>
                </div>
                <div style="margin-bottom: 0.75rem;">
                    <span style="font-weight: 600; color: #f57c00;">🎨 Personality:</span> 
                    <span style="color: #424242;">{PERSONALITY_DICT[selected_patient_profile.get('personality', 'N/A')]}</span>
                </div>
                <div style="margin-bottom: 0.75rem;">
                    <span style="font-weight: 600; color: #f57c00;">🧠 Medical History Recall Level:</span> 
                    <span style="color: #424242;">{RECALL_DICT[selected_patient_profile.get('recall_level', 'N/A')]}</span>
                </div>
                <div style="margin-bottom: 0.75rem;">
                    <span style="font-weight: 600; color: #f57c00;">😵 Dazed Level:</span> 
                    <span style="color: #424242;">{DAZED_DICT[selected_patient_profile.get('dazed_level', 'N/A')]}</span>
                </div>
            </div>
        </div>
        """
        patient_info_html = basic_info_html + persona_html
        patient_info_html = f"""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; min-height: {patient_info_height-45}px; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            {basic_info_html}
            {persona_html}
        </div>
        """
        components.html(patient_info_html, height=patient_info_height, scrolling=True)

        btn_cols = st.columns(2)
        if not st.session_state.get("chat_saved", False):
            if btn_cols[0].button("Reset Conversation", key="reset_demo"):
                st.session_state.chat_history = []
                st.session_state.patient_agent.reset()
                st.rerun()

    with cols[1]:
        # Conversation area with modern styling
        conversation_html = render_chat_html()
        conversation_height = patient_info_height - 110
        conversation_html = f"""
        <div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); 
                    padding: 1.5rem; border-radius: 12px; min-height: {conversation_height-45}px; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 2px solid #e9ecef;">
            {conversation_html}
        </div>
        """
        components.html(conversation_html, height=conversation_height, scrolling=True)

        # Doctor's message input with modern styling
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    padding: 1rem; border-radius: 12px; margin-top: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4 style="color: #1f4788; margin-top: 0; margin-bottom: 0.5rem;">💬 Enter Doctor's Message</h4>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form(key="chat_form", clear_on_submit=True):
            doctor_message = st.text_input("Doctor Message", placeholder="Type your message here...", label_visibility="collapsed")
            submitted = st.form_submit_button("📤 Send Message", use_container_width=True, type="primary")

        if submitted and doctor_message:
            if len(st.session_state.chat_history) == 0:
                st.session_state.conversation_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            add_message("Doctor", doctor_message)
            with st.spinner("🤔 Patient agent is generating a response..."):
                try:
                    # 添加调试输出
                    agent = st.session_state.patient_agent
                    st.write(f"🔍 调试：调用患者代理，模型={agent.model}, API类型={agent.backend_api_type}")
                    st.write(f"🔍 调试：client_params包含: {list(agent.client_params.keys()) if agent.client_params else '无'}")
                    
                    patient_response = st.session_state.patient_agent.inference(doctor_message)
                    
                    if not patient_response or patient_response.strip() == "":
                        patient_response = "抱歉，我没有理解您的问题。请再说一遍。"
                    else:
                        st.success("✅ 成功获取患者回复")
                        
                except Exception as e:
                    error_msg = str(e)
                    st.error(f"❌ 错误：患者代理生成回复时出错")
                    st.error(f"错误详情：{error_msg}")
                    
                    # 显示更详细的调试信息
                    with st.expander("🔍 查看详细错误信息", expanded=True):
                        import traceback
                        st.code(traceback.format_exc())
                        
                        # 显示患者代理的配置
                        st.write("**患者代理配置：**")
                        agent = st.session_state.patient_agent
                        st.json({
                            "backend": agent.backend,
                            "backend_api_type": agent.backend_api_type,
                            "model": agent.model,
                            "client_type": str(type(agent.client)),
                            "client_params": agent.client_params if agent.client_params else {},
                            "messages_count": len(agent.messages) if hasattr(agent, 'messages') else 0,
                        })
                    
                    patient_response = f"❌ 错误：{error_msg}"

            add_message("Patient", patient_response)
            st.rerun()



###########################
# Main App Routing
###########################

def main():
    # Show the patient selection page.
    if "selected_patient" not in st.session_state:
        patient_selection_page()
    else:
        demo_page()

if __name__ == "__main__":
    st.set_page_config(
        page_title="Patient Simulation Demo",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    inject_custom_css()
    main()
