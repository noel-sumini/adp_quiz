import streamlit as st

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Home navigation button always visible
def go_home():
    st.session_state.page = "home"

st.button("🏠 Main 홈", on_click=go_home, key="home_nav")

# Page routing
if st.session_state.page == "home":
    st.title("AI/Data Platform팀 팀미팅")
    st.write("원하는 게임을 선택하세요.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎶 음악 퀴즈", key="to_music"):  # Navigate to music quiz
            st.session_state.page = "music"
    with col2:
        if st.button("🤸‍♂️ 몸으로말해요", key="to_mom"):  # Navigate to body quiz
            st.session_state.page = "mom"

elif st.session_state.page == "music":
    # Import and run music quiz page
    import music_quiz
    music_quiz.run()

elif st.session_state.page == "mom":
    # Import and run mom quiz page
    import mom_quiz
    mom_quiz.run()