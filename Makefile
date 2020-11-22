quality_check:
	@./scripts/quality.sh

tag:
	@./scripts/tag.sh

pre_commit_install:
	@ pre-commit install && pre-commit install --hook-type commit-msg
