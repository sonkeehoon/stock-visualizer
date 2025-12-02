# crawler.py

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_kospi_df() -> pd.DataFrame:
    """
    코스피 시가총액 상위 100개 기업 크롤링 후 데이터프레임으로 반환
    """

    data = []  # 데이터를 담을 리스트 생성
    columns = [
        "종목별",
        "현재가",
        "전일비",
        "등락률",
        "거래량",
        "거래대금(백만)",
        "시가총액(억)",
    ]  # 컬럼리스트 생성

    for i in range(10):  # 1~10페이지까지 크롤링 (페이지당 10개, 총 100개 기업)

        url = f"https://finance.naver.com/sise/entryJongmok.naver?&page={i+ 1}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        # 테이블 전체 가져오기
        table = soup.select_one("body > div > table.type_1")

        # 테이블 안의 행들 가져오기
        rows = table.select("tr")
        for row in rows[2:-2]:
            cols = row.select("td")
            data.append([c.get_text(strip=True) for c in cols])

    df = pd.DataFrame(data, columns=columns)
    target_df = df[["종목별", "등락률", "현재가", "시가총액(억)"]]
    return target_df


def get_US_df() -> pd.DataFrame:
    """
    미국 시가총액 상위 100개 기업 크롤링 후 데이터프레임으로 반환
    """
    data = []
    columns = [
        "Company",
        "Change (%)",
        "Current Price ($)",
        "Market Cap ($)",
    ]  # 컬럼리스트 생성

    url = "https://finance.yahoo.com/markets/stocks/large-cap-stocks/?start=0&count=100"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    table = soup.select_one(
        "#main-content-wrapper > section.yf-12mq010 > div > div.tableContainer.yf-2v9ias > div > table"
    )
    tbody = table.select_one("tbody")

    data = []
    for i in range(100):
        row = tbody.find("tr", attrs={"data-testid-row": f"{i}"})

        name = row.select_one("td:nth-child(2) > div").get_text()
        
        price_tag = row.select_one("td:nth-child(4) > div > fin-streamer")
        span = price_tag.find("span")
        price = span.get_text() if span else price_tag.get_text()

        change_per_tag = row.select_one("td:nth-child(6) > fin-streamer")
        span2 = change_per_tag.find("span")
        change_per = span2.get_text() if span2 else change_per_tag.get_text()

        market_cap = row.select_one("td:nth-child(9) > fin-streamer").get_text()

        data.append([name, change_per, price, market_cap])

    return pd.DataFrame(data, columns=columns)


def get_er_df() -> pd.DataFrame:
    """
    주요 4개국 환율 크롤링 후 데이터프레임으로 반환
    """

    nations = ["USD", "EUR", "JPY", "CNY"]

    data = []
    columns = ["label", "price", "change", "chart_url"]  # 컬럼리스트 생성

    for nation in nations:
        url = f"https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_{nation}KRW"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")

        spot = soup.select_one("#content > div.spot")

        # price (class 이름에 의존하지 않고 em 하나만 가져오기)
        price_em = spot.select_one("div.today p.no_today em")
        price = price_em.get_text(strip=True) if price_em else None

        # change (두 번째 em 사용, 클래스 무시)
        change_em_list = spot.select("p.no_exday em")
        if len(change_em_list) >= 2:
            change = change_em_list[1].get_text(strip=True)
        elif change_em_list:
            change = change_em_list[-1].get_text(strip=True)
        else:
            change = ""
        change = change.replace("(", "").replace(")", "").replace("\n", "")

        chart_url = f"https://ssl.pstatic.net/imgfinance/chart/marketindex/area/month3/FX_{nation}KRW.png"
        data.append([nation, price, change, chart_url])

    df = pd.DataFrame(data=data, columns=columns)
    df.set_index("label", inplace=True)

    return df


if __name__ == "__main__":
    US_df = get_US_df()
    # print(er_df)
    # print(er_df.loc["USD"])
