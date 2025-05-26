import streamlit as st
import random
from momquiz_record import data as mom_data

# Entry point
def run():
    # Initialize mom-quiz session state
    if 'mom_stage' not in st.session_state:
        st.session_state.mom_stage    = 'select_category'
        st.session_state.mom_playlist = []
        st.session_state.mom_index    = 0

    # Home button
    if st.button('🏠 몸으로말해요 퀴즈 홈', key='mom_home_nav'):
        st.session_state.page = 'home'
        # reset quiz state
        st.session_state.mom_stage    = 'select_category'
        st.session_state.mom_playlist = []
        st.session_state.mom_index    = 0
        return

    # 1) 분야 선택 화면
    if st.session_state.mom_stage == 'select_category':
        st.title('🤸‍♂️ 몸으로말해요 퀴즈')
        category = st.selectbox(
            '퀴즈 분야를 선택하세요:',
            options=list(mom_data.keys()),
            key='mom_category_select'
        )
        if st.button('시작', key='mom_start'):
            items = mom_data[category]
            sample_count = min(10, len(items))
            st.session_state.mom_playlist = random.sample(items, sample_count)
            st.session_state.mom_index    = 0
            st.session_state.mom_stage    = 'quiz'

    # 2) 퀴즈 화면
    elif st.session_state.mom_stage == 'quiz':
        playlist = st.session_state.mom_playlist
        idx = st.session_state.mom_index
        # Show current keyword
        if idx < len(playlist):
            st.markdown(
                f"<h1 style='text-align:center'>{playlist[idx]}</h1>",
                unsafe_allow_html=True
            )
            if st.button('다음', key=f'mom_next_{idx}'):
                st.session_state.mom_index += 1
        else:
            st.success('🎉 퀴즈 완료!')
            if st.button('홈으로', key='mom_finish'):
                st.session_state.page = 'home'
                # reset for next time
                st.session_state.mom_stage    = 'select_category'
                st.session_state.mom_playlist = []
                st.session_state.mom_index    = 0