.PHONY: setup install-uv install-java infra-init infra-apply infra-destroy metabase-up metabase-down pipeline run

install-uv:
	@which uv > /dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh

install-java:
	sudo apt-get update && sudo apt-get install -y openjdk-21-jdk

setup: install-uv
	uv python install 3.13
	uv venv .venv --python 3.13
	uv sync

infra-init:
	cd terraform && terraform init

infra-apply:
	cd terraform && terraform apply

infra-destroy:
	cd terraform && terraform destroy

metabase-up:
	docker compose up -d

metabase-down:
	docker compose down

pipeline:
	dagster dev

run: infra-apply metabase-up pipeline