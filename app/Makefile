.PHONY: help \
        train train-leve train-regular train-pesado train-all clean-models \
        serve serve-prod serve-prod-8000 serve-prod-5000 clean-pycache format \
		frontend-install frontend-dev frontend-build frontend-typecheck

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

serve-prod-8000: ## Start the API on production (0.0.0.0:8000, 4 workers)
	@$(MAKE) -C service serve-prod-8000

serve-prod-5000: ## Start the API on production (0.0.0.0:5000, 4 workers)
	@$(MAKE) -C service serve-prod-5000

frontend-install: ## Install frontend dependencies
	@cd frontend && npm install

frontend-dev: ## Start frontend development server
	@cd frontend && npm run dev

frontend-build: ## Build the frontend for production
	@cd frontend && npm run build

frontend-typecheck: ## Run frontend type checking
	@cd frontend && npm run type-check

clean-pycache: ## Remove __pycache__ dirs everywhere
	@$(MAKE) -C training clean-pycache
	@$(MAKE) -C service clean-pycache

format:
	@echo "Formatting code with Black..."
	black service/ training/