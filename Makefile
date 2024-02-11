APP := $(shell basename -s .git $(shell git remote get-url origin))
REGISTRY ?= ghcr.io/yuandrk
VERSION := $(shell git describe --tags --abbrev=0)-$(shell git rev-parse --short HEAD)
ARCH ?= amd64

VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

.DEFAULT_GOAL := run 

### to do : 
### multi os 

pre:
	sudo apt install python3-venv

$(VENV)/bin/activate: requirements.txt
	@python3 -m venv $(VENV)
	@chmod +x $(VENV)/bin/activate
	@. $(VENV)/bin/activate && $(PIP) install -r requirements.txt

venv: $(VENV)/bin/activate
	@. $(VENV)/bin/activate

run: venv
	@. $(VENV)/bin/activate && $(PYTHON) scr/main.py

image: 
	@docker build . -t $(REGISTRY)/$(APP):$(VERSION)-$(ARCH)

arm:
	@docker build --build-arg ARCH=arm64v8 . -t $(REGISTRY)/$(APP):$(VERSION)-arm64

push:
	@docker push $(REGISTRY)/$(APP):$(VERSION)-$(ARCH)

clean:
	@rm -rf __pycache__
	@rm -rf $(VENV)
