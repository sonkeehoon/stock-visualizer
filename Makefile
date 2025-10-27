# Makefile
IMAGE_NAME = stock-visualizer_img
CONTAINER_NAME = stock-visualizer
PORT = 80


clean:
	-docker stop $(CONTAINER_NAME)
	-docker rm $(CONTAINER_NAME)
	docker system prune -af

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)
	docker logs -f $(CONTAINER_NAME)

restart: clean build run
