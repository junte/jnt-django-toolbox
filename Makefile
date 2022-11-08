lint:
	black --check .
	flake8 .
	poetry check
	pip check

pre_commit_install:
	pre-commit install && pre-commit install --hook-type commit-msg

test:
	pytest
