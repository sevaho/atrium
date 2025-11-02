##---------- Preliminaries ----------------------------------------------------
.POSIX:     # Get reliable POSIX behaviour
.SUFFIXES:  # Clear built-in inference rules

##---------- Variables --------------------------------------------------------
PREFIX = /usr/local  # Default installation directory

##---------- Build targets ----------------------------------------------------

help: ## Show this help message (default)
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Up
	envvar application.yaml | kubectl apply -f -
	kubectl -n tooling create configmap theonepager --from-file=index.html=index.html --from-file=nginx.conf=nginx.conf --dry-run=client -o yaml | kubectl replace -f -
	kubectl -n tooling rollout restart deployment theonepager
