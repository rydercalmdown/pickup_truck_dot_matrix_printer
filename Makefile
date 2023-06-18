IMAGE_NAME=rydercalmdown/road-writer
PI_IP=192.168.0.101

.PHONY: build
build:
	@docker build --platform=linux/amd64 -t $(IMAGE_NAME) .

.PHONY: install
install:
	@make build

.PHONY: run
run:
	@docker run --platform=linux/amd64 -it  -p 8000:8000 -v $(shell pwd)/src/:/code/ $(IMAGE_NAME)

.PHONY: copy
copy:
	@scp -r ./src/ ryder@$(PI_IP):/home/ryder/road_writer

.PHONY: open
open:
	@open http://$(PI_IP):8000/

.PHONY: ssh
ssh:
	@ssh ryder@$(PI_IP)
