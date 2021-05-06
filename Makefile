lint:
	@./scripts/lint.sh

tag:
	@./scripts/tag.sh

pre_commit_install:
	@ pre-commit install && pre-commit install --hook-type commit-msg

test:
	@pytest
