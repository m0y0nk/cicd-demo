#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${ROOT_DIR}/build"

rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}/app"
cp "${ROOT_DIR}/app/"*.py "${BUILD_DIR}/app/"
cp "${ROOT_DIR}/README.md" "${BUILD_DIR}/"

cat > "${BUILD_DIR}/build-info.txt" <<EOF
Application: CI/CD Demo Calculator
Build status: SUCCESS
Build time (UTC): $(date -u +"%Y-%m-%dT%H:%M:%SZ")
Source revision: ${GITHUB_SHA:-local}
EOF

echo "Build created at ${BUILD_DIR}"
find "${BUILD_DIR}" -type f -print
