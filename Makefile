
SHELL = /bin/bash
TAG ?= latest

all: build

# base is the published runtime image, workspace adds the test suite and dev dependencies
build:
	docker build --tag seasketch/heatmap:$(TAG) --target base --file Dockerfile .
	docker tag seasketch/heatmap:$(TAG) seasketch/heatmap:latest
	docker build --tag seasketch/heatmap:workspace --target workspace --file Dockerfile .

test: build
	docker run --rm \
		--volume $(shell pwd)/:/work \
		--workdir /work \
		seasketch/heatmap:workspace \
		pytest

shell: build
	docker run --rm -it \
		--volume $(shell pwd)/:/work \
		seasketch/heatmap:workspace \
		/bin/bash
