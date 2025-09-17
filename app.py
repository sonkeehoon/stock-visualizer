# app.py

import logging
import uuid
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import rc
import importlib
import time
from datetime import datetime
import pytz
import base64


from visualizer import make_treemap
import crawler  # crawler.py 전체 불러오기


# 접속 로그 출력 설정

# 로거 설정
logging.basicConfig(level=logging.INFO)

# 세션 ID 생성
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

logging.info(f" | 접속자가 앱을 열었습니다 | 세션ID={st.session_state.session_id}")  # docker logs에서 확인 가능

# 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False
rc('font', family='NanumGothic')

st.set_page_config(page_title="코스피 Top100", layout="wide")

# === 가운데 정렬 제목 ===
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.title("코스피 시총 Top100 히트맵")
    
# session_state 초기화
if "refresh" not in st.session_state:
    st.session_state.refresh = False

# === 새로고침 버튼 가운데 배치 ===
col1, col2, col3 = st.columns([1,2,1])
with col2:
    # 현재 시각 구하기
    kst = pytz.timezone('Asia/Seoul')
    now_live = datetime.now(kst).strftime(" %Y년 %m월 %d일 %H:%M:%S")
    
    if st.button("새로고침"):
        with st.spinner("데이터를 새로고침하는 중... ⏳"):
            df = crawler.target_df.copy()
            importlib.reload(crawler)  # crawler.py 다시 불러오기
            time.sleep(2)
            st.success("데이터 갱신 완료 ✅")
    
    st.write(f"마지막 갱신 시각 : {now_live}")
    
# 새로고침 플래그 체크
if st.session_state.refresh:
    st.session_state.refresh = False
    # st.experimental_rerun()  # 최신 버전이면 여전히 필요

# 데이터 로드
df = crawler.target_df.copy()

# 전처리
df["등락률"] = df["등락률"].str.replace("%","").astype(float)
df["시가총액(억)"] = df["시가총액(억)"].str.replace(",","").astype(int)

# 트리맵 배치하기
fig = make_treemap(df)

# Streamlit에 출력
st.pyplot(fig)

# === 크롤링한 원본 데이터 표 출력 ===

st.markdown(
    """
    <h2 style='text-align: center;'>📊 코스피 Top 100 </h2>
    """,
    unsafe_allow_html=True
)

df_display = df.copy()

# 등락률 뒤에 % 붙이기
df_display["등락률"] = df_display["등락률"].map("{:+.2f}%".format)

# 시가총액(억) 천 단위 콤마 추가
df_display["시가총액(억)"] = df_display["시가총액(억)"].map("{:,}".format)

df_display.index = df_display.index + 1  # 인덱스 1부터 시작

col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.dataframe(
        df_display, 
        # width="content", 
        width = 800,
        height = 400
    )

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
    unsafe_allow_html=True
)
