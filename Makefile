
SHELL = /bin/bash
TAG ?= latest

all: build

build:
	docker build --tag seasketch/heatmap:$(TAG) --file Dockerfile .
	docker tag seasketch/heatmap:$(TAG) seasketch/heatmap:latest

test:
	docker run --rm \
		--volume $(shell pwd)/:/app \
		seasketch/heatmap:$(TAG) \
		/app/tests/run_tests.sh

shell: build
	docker run --rm -it \
		--volume $(shell pwd)/:/app \
		seasketch/heatmap:$(TAG) \
		/bin/bash
