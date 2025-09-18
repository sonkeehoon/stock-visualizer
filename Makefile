# Makefile

# 변수 설정
IMAGE_NAME = kospi100_image
CONTAINER_NAME = kospi100
PORT = 80

# ==============================
# 1️⃣ 현재 실행 중인 컨테이너/이미지 정리
clean:
	-docker stop $(CONTAINER_NAME)
	-docker rm $(CONTAINER_NAME)
	docker system prune -af

# ==============================
# 2️⃣ Dockerfile로 이미지 빌드
build:
	docker build -t $(IMAGE_NAME) .

# ==============================
# 3️⃣ 빌드한 이미지로 컨테이너 실행
run:
	docker run -d -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)
	docker logs -f $(CONTAINER_NAME)
# ==============================
# 4️⃣ 전체 작업: 정리 → 빌드 → 실행

restart: clean build run