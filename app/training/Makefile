## Training automation for the PTD models.
## Self-contained: runnable standalone from this directory
## (`cd training && make train-leve`) or via the root Makefile
## (`make train-leve` from the repo root) both resolve the same way.
##
## `python -m training` must run with the repo root as cwd (so `training`
## resolves as a top-level package and its relative imports work), so every
## python invocation here `cd`s up to REPO_ROOT first.

.DEFAULT_GOAL := help
PYTHON        ?= python3

THIS_DIR      := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
REPO_ROOT     := $(abspath $(THIS_DIR)/..)

DATA_PATH     ?= ../PROJECT_2/data/PTD_level_dataset.xlsx
RESULTS_DIR   ?= models
VERSION       ?=

VERSION_FLAG  = $(if $(VERSION),--version $(VERSION),)

.PHONY: help train train-leve train-regular train-pesado train-all clean-models clean-pycache

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

train: train-leve ## Alias for the default (leve) profile

train-leve: ## Train using the 'leve' (fast/dev) profile
	cd $(REPO_ROOT) && $(PYTHON) -m training --profile leve --data-path $(DATA_PATH) --results-dir $(RESULTS_DIR) $(VERSION_FLAG)

train-regular: ## Train using the 'regular' profile
	cd $(REPO_ROOT) && $(PYTHON) -m training --profile regular --data-path $(DATA_PATH) --results-dir $(RESULTS_DIR) $(VERSION_FLAG)

train-pesado: ## Train using the 'pesado' (full/final) profile
	cd $(REPO_ROOT) && $(PYTHON) -m training --profile pesado --data-path $(DATA_PATH) --results-dir $(RESULTS_DIR) $(VERSION_FLAG)

train-all: train-leve train-regular train-pesado ## Run all three profiles sequentially

clean-models: ## Remove all generated model artifacts
	rm -rf $(REPO_ROOT)/$(RESULTS_DIR)

clean-pycache: ## Remove __pycache__ dirs under training/
	find $(THIS_DIR) -type d -name '__pycache__' -exec rm -rf {} +