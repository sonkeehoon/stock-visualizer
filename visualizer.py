# visualizer.py

from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
import squarify

plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False

# data = {
#     "종목": ["삼성전자", "SK하이닉스", "현대차", "LG화학", "카카오", "네이버", "POSCO홀딩스", "셀트리온", "한화솔루션", "현대모비스"],
#     "등락률": [1.5, -2.3, 0.8, -1.1, 3.2, -0.5, 2.0, -1.8, 0.3, -0.7],
#     "시가총액": [450, 120, 60, 55, 40, 70, 35, 25, 20, 30]  # 단위: 조원 (임의값)
# }


def make_treemap(df: pd.DataFrame) -> plt.Figure:
    """전처리된 df로 트리맵 생성, fig 반환"""

    kst = pytz.timezone("Asia/Seoul")
    now = datetime.now(kst).strftime(" %Y년 %m월 %d일 %H:%M:%S")
    # 색상 매핑 (등락률 기준)
    colors = df["등락률"].apply(lambda x: plt.cm.RdYlGn((x + 5) / 10))

    # 제곱근 변환 + 최소값 보정
    sizes = np.sqrt(df["시가총액(억)"].values)
    sizes = np.clip(sizes, a_min=50, a_max=None)  # 최소 크기 50

    # 트리맵 그리기
    fig, ax = plt.subplots(figsize=(16, 7))

    squarify.plot(
        sizes=sizes,
        label=[f"{row.종목별}\n{row.등락률:+.2f}%" for row in df.itertuples()],
        color=colors,
        alpha=0.8,
        text_kwargs={"color": "black", "fontsize": 10},
        ax=ax,
    )

    ax.set_title(f"코스피 Top 100 ({now})", fontsize=12)
    ax.axis("off")
    return fig


if __name__ == "__main__":

    import crawler

    df = crawler.get_target_df().copy()
    # 전처리
    df["등락률"] = df["등락률"].str.replace("%", "").astype(float)
    df["시가총액(억)"] = df["시가총액(억)"].str.replace(",", "").astype(int)
    make_treemap(df)
