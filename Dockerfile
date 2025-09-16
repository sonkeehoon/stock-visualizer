# 1. 베이스 이미지 설정 (Python 3.12 사용)
FROM python:3.12-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 필요한 파일 복사
COPY requirements.txt .
COPY app.py .
COPY crawler.py .
COPY visualizer.py .
COPY img/ ./img/

# 4. 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. Streamlit 포트 노출
EXPOSE 8501

# 6. 컨테이너 실행 시 Streamlit 앱 실행
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]