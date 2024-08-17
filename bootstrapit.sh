#!/bin/bash
# Bootstrapit Project Configuration
#
# Variables that are commented out can left as is
# if you are satisfied with the automatically
# derived default. For example, if you specify,
# LICENSE_ID="MIT" then the value for LICENSE_NAME
# will be "MIT License".

# Author info is used to populate
#  - License Info
#  - setup.py fields
#  - README.md contributor info
# This can also be a company or organization name and email
AUTHOR_NAME="Manuel Barkhau"
AUTHOR_EMAIL="mbarkhau@gmail.com"

KEYWORDS="traceback stacktrace pretty"
DESCRIPTION="Human readable stacktraces."


GIT_REPO_DOMAIN="github.com"
GIT_REPO_NAMESPACE="mbarkhau"
PACKAGE_NAME="pretty-traceback"
MODULE_NAME="pretty_traceback"

# PACKAGE_VERSION="2024.1021"
# PACKAGE_VERSION="v0.1.0"
PACKAGE_VERSION="$(date +'%Y.1001')"

# These must be valid (space separated) conda package names.
# A separate conda environment will be created for each of these.
#
# Some valid options (as of late 2018) are:
# - python=2.7
# - python=3.5
# - python=3.6
# - python=3.7
# - python=3.8
# - pypy2.7
# - pypy3.5
# - pypy3.6

DEFAULT_PYTHON_VERSION="python=3.8"
SUPPORTED_PYTHON_VERSIONS="python=3.8 python=3.6 pypy3.5 python=2.7"

# GIT_REPO_URL=https://${GIT_REPO_DOMAIN}/${GIT_REPO_NAMESPACE}/${PACKAGE_NAME}

# Valid Options are "None" or any valid SPDX Identifier:
#   - None (All Rights Reserved)
#   - MIT
#   - GPL-3.0-only
#   - Apache-2.0
#   - GPL-2.0-only
#   - BSD-3-Clause
#   - AGPL-3.0-only
#   - LGPL-3.0-only
#   - MPL-2.0
#
# See: https://choosealicense.com/licenses/
# License text pulled from:
#   https://github.com/spdx/license-list-data/tree/master/text

LICENSE_ID="MIT"

# SPDX_LICENSE_ID="MIT"
# LICENSE_NAME="MIT License"
# LICENSE_CLASSIFIER="License :: OSI Approved :: MIT License"
# LICENSE_CLASSIFIER="License :: Other/Proprietary License"
# COPYRIGHT_STRING="Copyright (c) ${YEAR} ${AUTHOR_NAME} (${AUTHOR_EMAIL}) - ${LICENSE_NAME}"

# Pages are used by the ci runner to host coverage reports
# PAGES_DOMAIN=gitlab.io
# PAGES_DOMAIN=github.io
# PAGES_DOMAIN=bitbucket.io
# PAGES_DOMAIN=gitlab-pages.yourdomain.com

DOCKER_REGISTRY_DOMAIN=registry.gitlab.com
# DOCKER_REGISTRY_DOMAIN=docker.yourdomain.com
#
# DOCKER_ROOT_IMAGE=registry.gitlab.com/mbarkhau/bootstrapit/root
# DOCKER_ENV_BUILDER_IMAGE=registry.gitlab.com/mbarkhau/bootstrapit/env_builder
# DOCKER_REGISTRY_URL=${DOCKER_REGISTRY_DOMAIN}/${GIT_REPO_NAMESPACE}/${PACKAGE_NAME}
# DOCKER_BASE_IMAGE=${DOCKER_REGISTRY_URL}/base

# LICENSE_NAME="Proprietary License"
# classifiers: https://pypi.org/pypi?%3Aaction=list_classifiers

# 1: Disables a failsafe for publishing to pypi
IS_PUBLIC=1


# PAGES_URL="https://${NAMESPACE}.${PAGES_DOMAIN}/${PACKAGE_NAME}/"

## Download and run the actual update script

if [[ $KEYWORDS == "keywords used on pypi" ]]; then
    echo "FAILSAFE! Default bootstrapit config detected.";
    echo "Did you forget to update parameters in your 'bootstrapit.sh' ?"
    exit 1;
fi

PROJECT_DIR=$(dirname "$0");

if ! [[ -f "$PROJECT_DIR/scripts/bootstrapit_update.sh" ]]; then
    mkdir -p "$PROJECT_DIR/scripts/";
    RAW_FILES_URL="https://gitlab.com/mbarkhau/bootstrapit/raw/master";
    curl --silent "$RAW_FILES_URL/scripts/bootstrapit_update.sh" \
        > "$PROJECT_DIR/scripts/bootstrapit_update.sh.tmp";
    mv "$PROJECT_DIR/scripts/bootstrapit_update.sh.tmp" \
        "$PROJECT_DIR/scripts/bootstrapit_update.sh";
fi

source "$PROJECT_DIR/scripts/bootstrapit_update.sh";
