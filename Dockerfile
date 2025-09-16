# Dockerfile
# 1. 베이스 이미지
FROM python:3.12-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. OS 패키지 업데이트 및 한글 폰트 설치
RUN apt-get update && apt-get install -y \
    fonts-nanum \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# 4. 필요한 파일 복사
COPY requirements.txt .
COPY app.py .
COPY crawler.py .
COPY visualizer.py .
COPY img/ ./img/

# 5. Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 6. Streamlit 포트 노출
EXPOSE 8501

# 7. 컨테이너 시작 시 Streamlit 앱 실행
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]