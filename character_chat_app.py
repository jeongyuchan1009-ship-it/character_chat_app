import streamlit as st
import json
import os
from datetime import datetime
from ai_helper import chat_with_character, search_character, search_character_image

st.set_page_config(
    page_title="캐릭터 대화",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

custom_css = """
    <style>
        * {
            box-sizing: border-box;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: #f8f9fa;
            min-height: 100vh;
        }

        [data-testid="stMainBlockContainer"] {
            background: transparent;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        h1 {
            color: #2d3748 !important;
            font-size: 3rem !important;
            font-weight: 800 !important;
            margin-bottom: 1.5rem !important;
            text-align: center;
        }

        h2, h3 {
            color: #2d3748 !important;
            font-weight: 700 !important;
        }

        .stButton>button {
            background: #6366f1 !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.85rem 1.8rem !important;
            font-weight: 700 !important;
            font-size: 0.98rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        }

        .stButton>button:hover {
            background: #4f46e5 !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
        }

        .stButton>button:active {
            transform: translateY(-1px) !important;
        }

        .stTextInput>div>div>input {
            border-radius: 10px !important;
            border: 2px solid #e0e7ff !important;
            padding: 0.9rem 1.2rem !important;
            font-size: 1rem !important;
            background-color: white !important;
            color: #1f2937 !important;
            transition: all 0.3s ease !important;
        }

        .stTextInput>div>div>input:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        }

        .stInfo, .stSuccess, .stError, .stWarning {
            border-radius: 12px !important;
            padding: 1.2rem !important;
            border-left: 5px solid !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
        }

        .stInfo {
            background-color: #eef2ff !important;
            border-left-color: #6366f1 !important;
            color: #1f2937 !important;
        }

        .stSuccess {
            background-color: #f0fdf4 !important;
            border-left-color: #10b981 !important;
            color: #1f2937 !important;
        }

        .stError {
            background-color: #fef2f2 !important;
            border-left-color: #ef4444 !important;
            color: #1f2937 !important;
        }

        .card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            border: 1px solid #f0f0f0;
        }

        .card:hover {
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
            transform: translateY(-3px);
        }

        .profile-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
            border-radius: 16px;
            padding: 2rem;
            border: 2px solid #e0e7ff;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.1);
        }

        .stChatMessage {
            background: white !important;
            border-radius: 12px !important;
            padding: 1.2rem !important;
            border-left: 5px solid #6366f1;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
            margin-bottom: 1rem;
        }

        [data-testid="stChatMessageContent"] {
            font-size: 1rem;
            line-height: 1.6;
            color: #1f2937 !important;
        }

        .stExpander {
            border-radius: 12px !important;
            border: 2px solid #e0e7ff !important;
            background-color: #f8f9ff !important;
        }

        .stExpander>div>button {
            color: #6366f1 !important;
            font-weight: 600 !important;
        }

        .stDivider {
            margin: 2rem 0 !important;
            border-top: 2px solid rgba(99, 102, 241, 0.15) !important;
        }

        .stImage {
            border-radius: 12px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
            overflow: hidden;
        }

        .search-section {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            margin-bottom: 1.5rem;
            border: 1px solid #f0f0f0;
        }

        .stChatInput>div>div>input {
            border-radius: 10px !important;
            border: 2px solid #e0e7ff !important;
            background: white !important;
            color: #1f2937 !important;
        }

        .stChatInput>div>div>input:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        }

        p, span, div, label {
            color: #2d3748 !important;
        }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.title("💬 캐릭터 대화 앱")

if "character" not in st.session_state:
    st.session_state.character = None
if "character_info" not in st.session_state:
    st.session_state.character_info = None
if "character_image" not in st.session_state:
    st.session_state.character_image = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None

st.markdown('<div class="search-section">', unsafe_allow_html=True)
st.markdown("### 🎬 캐릭터 선택")

col1, col2, col3 = st.columns([1.8, 1.8, 1])

with col1:
    user_name = st.text_input(
        "👤 사용자 이름",
        placeholder="예: 철수, 영희",
        value=st.session_state.user_name or "",
        label_visibility="collapsed"
    )
    if user_name:
        st.session_state.user_name = user_name

with col2:
    character_input = st.text_input(
        "💭 캐릭터 이름",
        placeholder="예: 셜록",
        label_visibility="collapsed"
    )

with col3:
    st.write("")
    search_btn = st.button("🔍 검색", use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)

if search_btn:
    if not user_name:
        st.error("👤 사용자 이름을 먼저 입력해주세요!")
    elif not character_input:
        st.error("💭 캐릭터 이름을 입력해주세요!")
    elif st.session_state.character != character_input:
        with st.spinner(f"🔍 '{character_input}' 정보와 사진을 검색 중입니다..."):
            character_info = search_character(character_input)
            character_image = search_character_image(character_input)
            st.session_state.character = character_input
            st.session_state.character_info = character_info
            st.session_state.character_image = character_image
            st.session_state.messages = []
        st.success(f"✨ '{character_input}'을(를) 불러왔습니다!")

st.divider()

if st.session_state.character:
    col_profile_img, col_profile_info = st.columns([1.2, 1.8])

    with col_profile_img:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if st.session_state.character_image:
            st.image(st.session_state.character_image, use_container_width=True)
        else:
            st.info("📸 사진을 찾을 수 없습니다.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_profile_info:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.markdown(f"### 🎭 {st.session_state.character}")
        with st.expander("📖 캐릭터 정보", expanded=False):
            st.markdown(st.session_state.character_info)
        st.markdown('</div>', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown("---")
        col_start1, col_start2 = st.columns(2)
        with col_start1:
            if st.button("💬 먼저 말걸기", use_container_width=True, type="primary"):
                st.session_state.messages = []
                st.info("메시지를 입력해서 대화를 시작해주세요!")

        with col_start2:
            if st.button("👋 먼저 말 받기", use_container_width=True, type="primary"):
                with st.spinner("캐릭터가 인사 중입니다..."):
                    greeting_prompt = f"""당신은 '{st.session_state.character}'이고, 처음으로 누군가를 만났습니다.
먼저 인사하고 자신을 소개하는 짧은 인사말을 해주세요. (2-3문장)
자연스럽고 친근하게 말해주세요."""

                    greeting = chat_with_character(
                        st.session_state.character,
                        st.session_state.character_info,
                        [{"role": "user", "content": "먼저 인사해줄래?"}]
                    )
                    st.session_state.messages = [
                        {"role": "assistant", "content": greeting}
                    ]
                st.rerun()
        st.divider()

    st.markdown("### 💬 대화")

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    user_input = st.chat_input("메시지를 입력하세요...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("생각 중입니다..."):
            response = chat_with_character(
                st.session_state.character,
                st.session_state.character_info,
                st.session_state.messages
            )

        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)

    st.divider()

    if st.session_state.messages:
        col_save, col_clear = st.columns(2)

        with col_save:
            if st.button("💾 대화 저장", use_container_width=True):
                user_folder = f"conversations/{st.session_state.user_name}"
                os.makedirs(user_folder, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{user_folder}/{st.session_state.character}_{timestamp}.json"

                save_data = {
                    "user": st.session_state.user_name,
                    "character": st.session_state.character,
                    "character_info": st.session_state.character_info,
                    "messages": st.session_state.messages,
                    "saved_at": datetime.now().isoformat()
                }

                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(save_data, f, ensure_ascii=False, indent=2)

                st.success(f"✅ '{filename}'으로 저장되었습니다!")

        with col_clear:
            if st.button("🔄 대화 초기화", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

else:
    st.info("💡 사용자 이름과 캐릭터를 입력한 후 검색 버튼을 눌러주세요!")
