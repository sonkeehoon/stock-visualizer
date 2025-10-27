# crawler.py

from bs4 import BeautifulSoup
import requests
import pandas as pd

columns = ["종목별", "현재가", "전일비", "등락률",
        "거래량", "거래대금(백만)", "시가총액(억)"]  # 컬럼리스트 생성


def get_target_df()-> pd.DataFrame:
    '''
    코스피 시가총액 상위 100개 기업 크롤링 후 데이터프레임으로 반환
    '''
    
    data = []  # 데이터를 담을 리스트 생성
    for i in range(10):  # 1~10페이지까지 크롤링 (페이지당 10개, 총 100개 기업)
        
        url = f"https://finance.naver.com/sise/entryJongmok.naver?&page={i+ 1}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        # 테이블 전체 가져오기
        table = soup.select_one("body > div > table.type_1")

        # 테이블 안의 행들 가져오기
        rows = table.select("tr")
        for row in rows[2: -2]:
            cols = row.select("td")
            data.append([c.get_text(strip=True) for c in cols])

    df = pd.DataFrame(data, columns=columns)
    target_df = df[["종목별", "등락률", "현재가", "시가총액(억)"]]
    return target_df
    