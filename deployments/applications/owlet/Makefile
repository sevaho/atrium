##---------- Preliminaries ----------------------------------------------------
.POSIX:     # Get reliable POSIX behaviour
.SUFFIXES:  # Clear built-in inference rules

##---------- Build targets ----------------------------------------------------

help: ## Show this help message (default)
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Up
	kubectl apply -f ./application.yaml

panel: ## Open the bridge's control panel on http://localhost:8089
	kubectl -n applications port-forward deploy/owlet 8089:8088
