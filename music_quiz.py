import streamlit as st
from streamlit_player import st_player
from songs_record import songs_by_period
import pandas as pd
import random


def run():
    # Transform songs_by_period into DataFrame
    records = []
    for period_str, track_list in songs_by_period.items():
        year = int(period_str.split("_")[0])
        for entry in track_list:
            records.append({
                "year": year,
                "artist": entry["artist"],
                "title": entry["title"],
                "link": entry["link"]
            })

    df_songs = pd.DataFrame(records)

    # Session state initialization
    if "stage" not in st.session_state:
        st.session_state.stage    = "select_year"
        st.session_state.year     = None
        st.session_state.playlist = []
        st.session_state.index    = 0

    # Home button (항상 보이도록 키 지정)
    if st.button("🏠 음악퀴즈 홈", key="home_button"):
        st.session_state.stage = "select_year"
        st.session_state.index = 0

    # 1) Year selection screen
    if st.session_state.stage == "select_year":
        st.title("🎶 AI/Data Platform 팀미팅 음악 퀴즈")
        decade = st.selectbox(
            "세대를 선택하세요:",
            options=sorted(df_songs["year"].unique()),
            format_func=lambda y: f"{y}년대",
            key="decade_select"
        )
        if st.button("시작", key="start_quiz"):
            # filter songs by selected decade and take a random sample of 10
            df_filtered = df_songs[df_songs.year == decade]
            n = min(10, len(df_filtered))
            sampled = df_filtered.sample(n).to_dict('records')
            st.session_state.playlist = sampled
            st.session_state.year     = decade
            st.session_state.index    = 0
            st.session_state.stage    = "play_song"

    # 2) Playback screen
    elif st.session_state.stage == "play_song":
        playlist = st.session_state.playlist
        song = playlist[st.session_state.index]

        # Display title and artist
        st.markdown(
            f"<h2 style='text-align:center'>{song['title']} - {song['artist']}</h2>",
            unsafe_allow_html=True
        )

        # Autoplay YouTube video
        st_player(song['link'], playing=True, height=300)

        # Next button
        if st.button("⏭️ 다음", key=f"next_{st.session_state.index}"):
            with st.spinner("다음 곡 불러오는 중..."):
                st.session_state.index += 1
                if st.session_state.index >= len(playlist):
                    st.success("🔔 모든 곡을 재생했습니다. 다시 처음으로 돌아갑니다.")
                    st.session_state.stage = "select_year"
                # else: 그대로 play_song 상태 유지
