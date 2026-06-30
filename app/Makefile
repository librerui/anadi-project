## Root Makefile — thin dispatcher only. All real logic lives in the
## Makefile of the folder it belongs to:
##   training/Makefile  -> model training
##   service/Makefile   -> the API
## This file just forwards to them so `make <target>` works from the repo
## root without you needing to remember which subfolder owns what.

.PHONY: help \
        train train-leve train-regular train-pesado train-all clean-models \
        serve serve-prod clean-pycache format

help:
	@$(MAKE) -s -C training help
	@echo ""
	@$(MAKE) -s -C service help

## training/
train:
	@$(MAKE) -C training train

train-leve:
	@$(MAKE) -C training train-leve

train-regular:
	@$(MAKE) -C training train-regular

train-pesado:
	@$(MAKE) -C training train-pesado

train-all:
	@$(MAKE) -C training train-all

clean-models:
	@$(MAKE) -C training clean-models

## service/
serve: ## Start the API with autoreload (dev)
	@$(MAKE) -C service serve

serve-prod: ## Start the API without autoreload (prod-like)
	@$(MAKE) -C service serve-prod

clean-pycache: ## Remove __pycache__ dirs everywhere
	@$(MAKE) -C training clean-pycache
	@$(MAKE) -C service clean-pycache

format:
	@echo "Formatting code with Black..."
	black service/ training/