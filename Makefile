
SHELL = /bin/bash
TAG ?= latest

all: build

# base is the published runtime image, workspace adds the test suite and dev dependencies
build:
	docker build --tag seasketch/heatmap:$(TAG) --target base --file Dockerfile .
	docker tag seasketch/heatmap:$(TAG) seasketch/heatmap:latest
	docker build --tag seasketch/heatmap:workspace --target workspace --file Dockerfile .

# perrygeo/gdal-base is amd64-only, so arm64 uses Dockerfile.arm64 (Debian GDAL + venv)
build-arm64:
	docker build --platform linux/arm64 --tag seasketch/heatmap:$(TAG)-arm64 --target base --file Dockerfile.arm64 .
	docker tag seasketch/heatmap:$(TAG)-arm64 seasketch/heatmap:arm64
	docker build --platform linux/arm64 --tag seasketch/heatmap:workspace-arm64 --target workspace --file Dockerfile.arm64 .

test: build
	docker run --rm \
		--volume $(shell pwd)/:/work \
		--workdir /work \
		seasketch/heatmap:workspace \
		pytest

test-arm64: build-arm64
	docker run --rm --platform linux/arm64 \
		--volume $(shell pwd)/:/work \
		--workdir /work \
		seasketch/heatmap:workspace-arm64 \
		pytest

shell: build
	docker run --rm -it \
		--volume $(shell pwd)/:/work \
		seasketch/heatmap:workspace \
		/bin/bash

shell-arm64: build-arm64
	docker run --rm -it --platform linux/arm64 \
		--volume $(shell pwd)/:/work \
		seasketch/heatmap:workspace-arm64 \
		/bin/bash
