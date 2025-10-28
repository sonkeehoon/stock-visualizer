# visualizer.py

import re
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
import squarify

plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False


def make_treemap(df: pd.DataFrame, market: str) -> plt.Figure:
    """전처리된 df로 트리맵 생성, fig 반환"""

    # --- 단위 문자열 -> 숫자 변환 함수 ---
    def convert_market_cap(val):

        if isinstance(val, (int, float)):
            return val

        if isinstance(val, str):
            val = val.strip().upper()

            try:
                if val.endswith("T"):
                    return float(val[:-1]) * 1_000_000_000_000
                elif val.endswith("B"):
                    return float(val[:-1]) * 1_000_000_000
                elif val.endswith("M"):
                    return float(val[:-1]) * 1_000_000
                elif val.endswith("K"):
                    return float(val[:-1]) * 1_000
                else:
                    return float(val)

            except ValueError:
                return np.nan

        return np.nan

    def clean_company_name(name: str) -> str:
        """
        불필요한 접미사(Inc, Corp, Ltd 등)를 제거해 트리맵 라벨을 간결하게 만드는 함수
        """
        if not isinstance(name, str):
            return name
        if "Taiwan" in name:
            return "TSMC"
        if "International Business Machines" in name:
            return "IBM"
        if "Mitsubishi" in name:
            return "Mitsubishi"
        if "JPMorgan" in name:
            return "JPMorgan"

        # 제거할 단어 목록
        patterns = [
            r"\bInc\b\.?",
            r"\bIncorporated\b",
            r"\bCorporation\b",
            r"\bCorp\b\.?",
            r"\bLtd\b\.?",
            r"\bLimited\b",
            r"\bPLC\b",
            r"\bHoldings\b",
            r"\bGroup\b",
            r"\bCompany\b",
            r"\bLLC\b",
            r"\bN\.V\.\b",
            r"\bS\.A\.\b",
        ]
        for p in patterns:
            name = re.sub(p, "", name, flags=re.IGNORECASE)
        # 불필요한 공백 정리
        return re.sub(r"\s+", " ", name).strip()

    kst = pytz.timezone("Asia/Seoul")

    if market.upper() == "KOSPI":
        cur_time = datetime.now(kst).strftime(" %Y년 %m월 %d일 %H:%M:%S")
        label_col = "종목별"
        change_col = "등락률"
        cap_col = "시가총액(억)"
        title = f"코스피 Top 100 ({cur_time})"

        sizes = np.sqrt(df[cap_col].values)
        fontsize = 10

    elif market.upper() == "U.S.":
        cur_time = datetime.now(kst).strftime(
            "%b %d, %Y %I:%M:%S %p"
        )  # e.g. Oct 28, 2025 04:31:33 PM
        label_col = "Company"
        change_col = "Change (%)"
        cap_col = "Market Cap ($)"
        title = f"U.S. Large Cap Top 100 ({cur_time})"

        df["converted_cap_col"] = df[cap_col].apply(convert_market_cap)
        sizes = np.sqrt(df["converted_cap_col"].values)
        fontsize = 8

    else:
        raise ValueError("market must be 'KOSPI' or 'NASDAQ' or 'EXCHANGE RATE'")

    # 색상 매핑 (등락률 기준)
    colors = df[change_col].apply(lambda x: plt.cm.RdYlGn((x + 5) / 10))

    # 최소값 보정
    sizes = np.clip(sizes, a_min=50, a_max=None)  # 최소 크기 50

    # 트리맵 그리기
    fig, ax = plt.subplots(figsize=(16, 7))

    squarify.plot(
        sizes=sizes,
        label=[
            f"{clean_company_name(row[0])}\n{row[1]:+.2f}%"
            for row in df.itertuples(index=False, name=None)
        ],
        color=colors,
        alpha=0.8,
        text_kwargs={"color": "black", "wrap": True, "fontsize": fontsize},
        ax=ax,
    )

    ax.set_title(f"{title}", fontsize=12)
    ax.axis("off")
    return fig


if __name__ == "__main__":

    import crawler

    df = crawler.get_kospi_df().copy()
    # 전처리
    df["등락률"] = df["등락률"].str.replace("%", "").astype(float)
    df["시가총액(억)"] = df["시가총액(억)"].str.replace(",", "").astype(int)
    make_treemap(df, market="KOSPI")
