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
        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }

        @keyframes glow {
            0%, 100% { box-shadow: 0 0 20px rgba(255, 0, 255, 0.5), 0 0 40px rgba(0, 255, 255, 0.3); }
            50% { box-shadow: 0 0 30px rgba(255, 0, 255, 0.8), 0 0 60px rgba(0, 255, 255, 0.5); }
        }

        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 5px rgba(255, 100, 200, 0.5); }
            50% { box-shadow: 0 0 30px rgba(255, 100, 200, 1), 0 0 60px rgba(100, 200, 255, 0.6); }
        }

        * {
            box-sizing: border-box;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(-45deg, #ff006e, #8338ec, #3a86ff, #06ffa5, #ffbe0b);
            background-size: 400% 400%;
            animation: gradient-shift 15s ease infinite;
            min-height: 100vh;
        }

        [data-testid="stMainBlockContainer"] {
            background: transparent;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1 {
            background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff, #06ffa5, #ff006e);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3.5rem !important;
            font-weight: 900 !important;
            margin-bottom: 2rem !important;
            text-align: center;
            letter-spacing: -1px;
            animation: gradient-shift 4s ease infinite;
            text-shadow: 0 0 30px rgba(255, 100, 200, 0.3);
        }

        h2, h3 {
            background: linear-gradient(90deg, #ff006e, #8338ec, #3a86ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
            animation: gradient-shift 6s ease infinite;
        }

        .stButton>button {
            background: linear-gradient(135deg, #ff006e 0%, #8338ec 25%, #3a86ff 50%, #06ffa5 75%, #ffbe0b 100%) !important;
            background-size: 300% 300%;
            animation: gradient-shift 3s ease infinite;
            color: white !important;
            border: 3px solid rgba(255, 255, 255, 0.5) !important;
            border-radius: 20px !important;
            padding: 1rem 2.5rem !important;
            font-weight: 800 !important;
            font-size: 1.05rem !important;
            transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1) !important;
            box-shadow: 0 0 30px rgba(255, 0, 200, 0.6),
                        0 0 60px rgba(51, 56, 236, 0.4),
                        inset 0 0 20px rgba(255, 255, 255, 0.2) !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        }

        .stButton>button:hover {
            transform: translateY(-6px) scale(1.05) !important;
            box-shadow: 0 0 50px rgba(255, 0, 200, 0.8),
                        0 0 80px rgba(51, 56, 236, 0.6),
                        inset 0 0 30px rgba(255, 255, 255, 0.3) !important;
            animation: pulse-glow 0.5s ease-in-out infinite !important;
        }

        .stButton>button:active {
            transform: translateY(-3px) scale(0.98) !important;
        }

        .stTextInput>div>div>input {
            border-radius: 15px !important;
            border: 3px solid rgba(255, 100, 200, 0.6) !important;
            padding: 1rem 1.5rem !important;
            font-size: 1rem !important;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85)) !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 20px rgba(255, 100, 200, 0.3) !important;
        }

        .stTextInput>div>div>input:focus {
            border-color: #06ffa5 !important;
            box-shadow: 0 0 30px rgba(6, 255, 165, 0.6),
                        0 0 60px rgba(255, 0, 200, 0.4) !important;
            background: white !important;
        }

        .stInfo, .stSuccess, .stError, .stWarning {
            border-radius: 20px !important;
            padding: 1.5rem !important;
            border-left: 6px solid !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
            backdrop-filter: blur(10px);
        }

        .stInfo {
            background: linear-gradient(135deg, rgba(58, 134, 255, 0.2), rgba(6, 255, 165, 0.1)) !important;
            border-left-color: #3a86ff !important;
        }

        .stSuccess {
            background: linear-gradient(135deg, rgba(6, 255, 165, 0.2), rgba(255, 190, 11, 0.1)) !important;
            border-left-color: #06ffa5 !important;
        }

        .stError {
            background: linear-gradient(135deg, rgba(255, 0, 110, 0.2), rgba(255, 100, 200, 0.1)) !important;
            border-left-color: #ff006e !important;
        }

        .card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
            border-radius: 25px;
            padding: 2.5rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2),
                        0 0 40px rgba(255, 0, 200, 0.3),
                        inset 0 0 30px rgba(255, 255, 255, 0.5);
            transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
            border: 2px solid rgba(255, 100, 200, 0.3);
            backdrop-filter: blur(20px);
        }

        .card:hover {
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3),
                        0 0 60px rgba(255, 0, 200, 0.5),
                        inset 0 0 30px rgba(255, 255, 255, 0.6);
            transform: translateY(-8px) scale(1.02);
            animation: glow 1.5s ease-in-out infinite;
        }

        .profile-card {
            background: linear-gradient(135deg,
                rgba(255, 0, 110, 0.15),
                rgba(131, 56, 236, 0.15),
                rgba(58, 134, 255, 0.15),
                rgba(6, 255, 165, 0.15));
            border-radius: 25px;
            padding: 2.5rem;
            border: 3px dashed rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(20px);
            box-shadow: 0 0 40px rgba(255, 0, 200, 0.3),
                        0 0 80px rgba(51, 56, 236, 0.2),
                        inset 0 0 30px rgba(255, 255, 255, 0.2);
        }

        .stChatMessage {
            background: white !important;
            border-radius: 18px !important;
            padding: 1.5rem !important;
            border-left: 6px solid;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12),
                        0 0 30px rgba(255, 100, 200, 0.2) !important;
            border: 2px solid rgba(255, 100, 200, 0.2) !important;
            margin-bottom: 1.5rem;
            animation: float 3s ease-in-out infinite;
        }

        [data-testid="stChatMessageContent"] {
            font-size: 1.05rem;
            line-height: 1.7;
            color: #1a1a1a;
        }

        .stExpander {
            border-radius: 18px !important;
            border: 3px solid rgba(255, 100, 200, 0.4) !important;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 250, 200, 0.9)) !important;
            box-shadow: 0 0 20px rgba(255, 100, 200, 0.2) !important;
        }

        .stExpander>div>button {
            color: #ff006e !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }

        .stDivider {
            margin: 2.5rem 0 !important;
            border-top: 3px dashed rgba(255, 255, 255, 0.4) !important;
        }

        .stImage {
            border-radius: 20px !important;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2),
                        0 0 40px rgba(255, 0, 200, 0.4) !important;
            overflow: hidden;
            border: 3px solid rgba(255, 255, 255, 0.5) !important;
        }

        .search-section {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 250, 240, 0.95));
            border-radius: 25px;
            padding: 2rem;
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2),
                        0 0 40px rgba(255, 0, 200, 0.25);
            margin-bottom: 2rem;
            border: 3px solid rgba(255, 100, 200, 0.3);
            backdrop-filter: blur(15px);
        }

        [data-testid="stSpinner"] {
            color: #ff006e !important;
        }

        .stChatInput>div>div>input {
            border-radius: 15px !important;
            border: 3px solid rgba(255, 100, 200, 0.6) !important;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(255, 250, 240, 0.98)) !important;
            box-shadow: 0 0 20px rgba(255, 100, 200, 0.2) !important;
        }

        .stChatInput>div>div>input:focus {
            border-color: #06ffa5 !important;
            box-shadow: 0 0 40px rgba(6, 255, 165, 0.5),
                        0 0 80px rgba(255, 0, 200, 0.3) !important;
        }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.title("💬 🌈 캐릭터 대화 앱 ✨")

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
st.markdown("### 🎬 🌟 캐릭터 선택 ⭐")

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
    search_btn = st.button("🔍 ✨ 검색", use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)

if search_btn:
    if not user_name:
        st.error("👤 사용자 이름을 먼저 입력해주세요!")
    elif not character_input:
        st.error("💭 캐릭터 이름을 입력해주세요!")
    elif st.session_state.character != character_input:
        with st.spinner(f"✨ 🔮 '{character_input}' 정보와 사진을 검색 중입니다..."):
            character_info = search_character(character_input)
            character_image = search_character_image(character_input)
            st.session_state.character = character_input
            st.session_state.character_info = character_info
            st.session_state.character_image = character_image
            st.session_state.messages = []
        st.success(f"🎉 🌈 '{character_input}'을(를) 불러왔습니다! ✨")

st.divider()

if st.session_state.character:
    col_profile_img, col_profile_info = st.columns([1.2, 1.8])

    with col_profile_img:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if st.session_state.character_image:
            st.image(st.session_state.character_image, use_container_width=True)
        else:
            st.info("📸 ✨ 사진을 찾을 수 없습니다.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_profile_info:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.markdown(f"### 🎭 ⭐ {st.session_state.character} ⭐")
        with st.expander("📖 🌟 캐릭터 정보", expanded=False):
            st.markdown(st.session_state.character_info)
        st.markdown('</div>', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown("---")
        col_start1, col_start2 = st.columns(2)
        with col_start1:
            if st.button("💬 🚀 먼저 말걸기 ✨", use_container_width=True, type="primary"):
                st.session_state.messages = []
                st.info("💡 🎯 메시지를 입력해서 대화를 시작해주세요! ⭐")

        with col_start2:
            if st.button("👋 🌟 먼저 말 받기 💫", use_container_width=True, type="primary"):
                with st.spinner("✨ 🎭 캐릭터가 인사 중입니다..."):
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

    st.markdown("### 💬 🌈 대화 ✨")

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    user_input = st.chat_input("💬 ✨ 메시지를 입력하세요...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("🤔 💭 생각 중입니다..."):
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
            if st.button("💾 ✨ 대화 저장 🌟", use_container_width=True):
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

                st.success(f"✅ 🎉 '{filename}'으로 저장되었습니다! ⭐")

        with col_clear:
            if st.button("🔄 💫 대화 초기화 ✨", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

else:
    st.info("💡 ✨ 사용자 이름과 캐릭터를 입력한 후 검색 버튼을 눌러주세요! 🌟")
