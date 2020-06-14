#!/usr/bin/env bash

set -o errexit
set -o nounset

version=$(poetry version | cut -f 2 -d ' ')

echo "Version for deploy: ${version}"

poetry build
poetry publish
git tag -a v${version} -m "v${version}"
