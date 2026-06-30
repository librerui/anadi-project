## Service automation — start/stop the API.
## Self-contained: runnable standalone from this directory
## (`cd service && make serve`) or via the root Makefile
## (`make serve` from the repo root) — both resolve the same way.
##
## uvicorn needs `service` importable as a top-level package, so this
## always runs from REPO_ROOT, same pattern as training/Makefile.

.DEFAULT_GOAL := help
PYTHON  ?= python3
HOST    ?= 0.0.0.0
PORT    ?= 8000

THIS_DIR   := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
REPO_ROOT  := $(abspath $(THIS_DIR)/..)

.PHONY: help serve serve-prod clean-pycache

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

serve: ## Start the API with autoreload (dev)
	cd $(REPO_ROOT) && $(PYTHON) -m uvicorn service.main:app --host $(HOST) --port $(PORT) --reload

serve-prod: ## Start the API without autoreload (prod-like)
	cd $(REPO_ROOT) && $(PYTHON) -m uvicorn service.main:app --host $(HOST) --port $(PORT)

clean-pycache: ## Remove __pycache__ dirs under service/
	find $(THIS_DIR) -type d -name '__pycache__' -exec rm -rf {} +