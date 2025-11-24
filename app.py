# app.py

import base64
import logging
import time
import uuid
from datetime import datetime

import matplotlib.pyplot as plt
import pytz
import streamlit as st
from matplotlib import rc

import crawler  # crawler.py 전체 불러오기
from visualizer import make_treemap

# 접속 로그 출력 설정

# 로거 설정
logging.basicConfig(level=logging.INFO)

# 세션 ID 생성

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

logging.info(
    f" | 접속자가 앱을 열었습니다 | 세션ID={st.session_state.session_id}"
)  # docker logs에서 확인 가능

# 한글 폰트 설정
plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False
rc("font", family="NanumGothic")

st.set_page_config(page_title="Live Stock Info", layout="wide")

kospi_tab, US_tab, er_tab = st.tabs(["Kospi Top100", "U.S. Top100", "Exchange Rate"])

with kospi_tab:
    # === 가운데 정렬 제목 ===
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title(f"코스피 Top100 히트맵")

    # session_state 초기화
    if "refresh_kospi" not in st.session_state:
        st.session_state.refresh_kospi = False

    # === 새로고침 버튼 가운데 배치 ===
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # 현재 시각 구하기
        kst = pytz.timezone("Asia/Seoul")
        cur_time = datetime.now(kst).strftime(
            "%b %d, %Y %I:%M:%S %p"
        )  # e.g. Oct 28, 2025 04:31:33 PM

        if st.button("새로고침", key="kospi_refresh_button"):
            with st.spinner("데이터를 새로고침하는 중... ⏳"):
                df = crawler.get_kospi_df()  # 최신 데이터 크롤링
                time.sleep(2)
                st.session_state.refresh_kospi = True
                st.success("데이터 갱신 완료 ✅")

        st.write(f"마지막 갱신 시각: {cur_time}")

    # 새로고침 플래그 체크
    if st.session_state.refresh_kospi:
        st.session_state.refresh_kospi = False

    # 데이터 로드
    df = crawler.get_kospi_df()

    # 전처리
    df["등락률"] = df["등락률"].str.replace("%", "").astype(float)
    df["시가총액(억)"] = df["시가총액(억)"].str.replace(",", "").astype(int)

    # 트리맵 배치하기
    fig = make_treemap(df, market="KOSPI")

    # Streamlit에 출력
    st.pyplot(fig)

    # === 크롤링한 원본 데이터 표 출력 ===

    st.markdown(
        """
        <h2 style='text-align: center;'>📊 코스피 Top 100 </h2>
        """,
        unsafe_allow_html=True,
    )

    df_display = df.copy()

    # 등락률 뒤에 % 붙이기
    df_display["등락률"] = df_display["등락률"].map("{:+.2f}%".format)

    # 시가총액(억) 천 단위 콤마 추가
    df_display["시가총액(억)"] = df_display["시가총액(억)"].map("{:,}".format)

    df_display.index = df_display.index + 1  # 인덱스 1부터 시작

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.dataframe(
            df_display,
            # width="content",
            width=800,
            height=400,
        )

with US_tab:
    # === 가운데 정렬 제목 ===
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("U.S. Top 100 Heatmap")

    # session_state 초기화
    if "refresh_US" not in st.session_state:
        st.session_state.refresh_US = False

    # === 새로고침 버튼 가운데 배치 ===
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # 현재 시각 구하기
        kst = pytz.timezone("Asia/Seoul")
        cur_time = datetime.now(kst).strftime(
            "%b %d, %Y %I:%M:%S %p"
        )  # e.g. Oct 28, 2025 04:31:33 PM

        if st.button("Refresh", key="US_refresh_button"):
            with st.spinner("Refreshing data... ⏳"):
                df = crawler.get_US_df()  # 최신 데이터 크롤링
                time.sleep(2)
                st.session_state.refresh_US = True
                st.success("Data refreshed successfully ✅")

        st.write(f"Last updated: {cur_time}")

    # 새로고침 플래그 체크
    if st.session_state.refresh_US:
        st.session_state.refresh_US = False

    # 데이터 로드
    df = crawler.get_US_df()

    # 전처리
    df["Change (%)"] = df["Change (%)"].str.replace("%", "").astype(float)

    # 트리맵 배치하기
    fig = make_treemap(df, market="U.S.")

    # Streamlit에 출력
    st.pyplot(fig)

    # === 크롤링한 원본 데이터 표 출력 ===

    st.markdown(
        """
        <h2 style='text-align: center;'>📊 U.S. Top 100 </h2>
        """,
        unsafe_allow_html=True,
    )

    df_display = df.iloc[:, :-1].copy()

    # 등락률 뒤에 % 붙이기
    df_display["Change (%)"] = df_display["Change (%)"].map("{:+.2f}%".format)

    df_display.index = df_display.index + 1  # 인덱스 1부터 시작

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.dataframe(
            df_display,
            # width="content",
            width=800,
            height=400,
        )

with er_tab:
    nations = ["USD", "EUR", "JPY", "CNY"]

    # === 왼쪽 정렬 제목 ===
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown("## 💱 주요 4개국 환율")

    # session_state 초기화
    if "refresh_US" not in st.session_state:
        st.session_state.refresh_US = False

    # === 새로고침 버튼 가운데 배치 ===
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        # 현재 시각 구하기
        kst = pytz.timezone("Asia/Seoul")
        cur_time = datetime.now(kst).strftime(
            "%b %d, %Y %I:%M:%S %p"
        )  # e.g. Oct 28, 2025 04:31:33 PM

        if st.button("새로고침", key="er_refresh_button"):
            with st.spinner("데이터를 새로고침하는 중... ⏳"):
                er_df = crawler.get_er_df()  # 최신 데이터 크롤링
                time.sleep(2)
                st.session_state.refresh_kospi = True
                st.success("데이터 갱신 완료 ✅")

        st.write(f"마지막 갱신 시각: {cur_time}")

    # 새로고침 플래그 체크
    if st.session_state.refresh_US:
        st.session_state.refresh_US = False

    # 데이터 로드
    er_df = crawler.get_er_df()

    # =========================
    # 1행: 미국 달러(왼쪽 큰 영역) / 유로(오른쪽)
    # =========================
    # col_left_top, col_right_top = st.columns([2, 1])

    # --- 미국 달러 ---
    for nation in nations:
        info = er_df.loc[nation]
        box = st.container(border=True)

        label = ""
        if nation == "USD":
            label = "미국 달러"
        elif nation == "EUR":
            label = "유로"
        elif nation == "JPY":
            label = "일본 엔화"
        elif nation == "CNY":
            label = "중국 위안화"

        with box:
            st.markdown(
                f"""
            <h3>
                {label}({nation}) &nbsp; {info['price']}<span style="font-size:14px; ">&nbsp;원&nbsp;</span>
                <span style="font-size:14px; color:#777;"> 전일대비 </span> {info['change']} 
            </h3>
            """,
                unsafe_allow_html=True,
            )

            # TODO: 3개월 환율 차트 데이터로 교체
            # usd_df = crawler.get_usd_history("3개월")
            img_url = f"https://ssl.pstatic.net/imgfinance/chart/marketindex/area/month3/FX_{nation}KRW.png"
            st.image(img_url, width=750)


github_url = "https://github.com/sonkeehoon/stock-visualizer"
naver_blog_url = "https://blog.naver.com/djfkfk12345"

# 이미지 파일을 Base64로 읽기
with open("img/octocat.png", "rb") as f:
    data = f.read()
    github_logo = base64.b64encode(data).decode()

with open("img/naver_blog.png", "rb") as f:
    data = f.read()
    naver_blog_logo = base64.b64encode(data).decode()

st.markdown(
    f"""
    <hr style="margin-top:50px; margin-bottom:10px;"> 
    <div style='text-align: center; font-size: 15px; color: #555;'>
        Stock Visualizer: <a href="{github_url}" target="_blank">
            <img src="data:image/png;base64,{github_logo}" width="35" style="vertical-align:middle;">
                </a></div>
                
    <div style='text-align: center; font-size: 15px; color: #555;'> 
        개발자 블로그: <a href="{naver_blog_url}" target="_blank">
            <img src="data:image/png;base64,{naver_blog_logo}" width="35" style="vertical-align:middle;">
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
