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
    나스닥 시가총액 상위 100개 기업 크롤링 후 데이터프레임으로 반환
    """
    data = []
    columns = [
        "Company",
        "Change (%)",
        "Current Price ($)",
        "Market Cap ($)"
    ]  # 컬럼리스트 생성


    url = "https://finance.yahoo.com/markets/stocks/large-cap-stocks/?start=0&count=100"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers= headers)
    soup = BeautifulSoup(res.text, "lxml")
    table = soup.select_one("#main-content-wrapper > section.yf-12mq010 > div > div.tableContainer.yf-2v9ias > div > table.yf-16a0xa2.bd")
    tbody = table.select_one("tbody")
    # print(tbody)

    data = []
    for i in range(100):
        row = tbody.find("tr", attrs = {"data-testid-row": f"{i}"})
    
        name = row.select_one("td:nth-child(2) > div").get_text()
        price = row.select_one("td:nth-child(4) > div > fin-streamer").get_text()
        change_per = row.select_one("td:nth-child(6) > fin-streamer > span").get_text()
        market_cap = row.select_one("td:nth-child(9) > fin-streamer").get_text()
        
        data.append([name, change_per, price, market_cap])
    
    return pd.DataFrame(data, columns = columns)
