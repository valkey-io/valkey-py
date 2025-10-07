#!/bin/bash

set -e

SUFFIX=$1
if [ -z ${SUFFIX} ]; then
    echo "Supply valid python package extension such as whl or tar.gz. Exiting."
    exit 3
fi

script=`pwd`/${BASH_SOURCE[0]}
HERE=`dirname ${script}`
ROOT=`realpath ${HERE}/../..`

cd ${ROOT}
DESTENV=${ROOT}/.venvforinstall
if [ -d ${DESTENV} ]; then
    rm -rf ${DESTENV}
fi
python -m venv ${DESTENV}
source ${DESTENV}/bin/activate
pip install --upgrade --quiet pip setuptools wheel
pip install --quiet '.[dev]'
invoke devenv
invoke package

# find packages
PKG=`ls ${ROOT}/dist/*.${SUFFIX}`
ls -l ${PKG}

TESTDIR=${ROOT}/STAGETESTS
if [ -d ${TESTDIR} ]; then
    rm -rf ${TESTDIR}
fi
mkdir ${TESTDIR}
cp -R ${ROOT}/tests ${TESTDIR}/tests
cd ${TESTDIR}

# install, run tests
pip install ${PKG}
# Valkey tests
pytest -m 'not onlycluster'
# ValkeyCluster tests
CLUSTER_URL="valkey://localhost:16379/0"
pytest -m 'not onlynoncluster and not valkeymod and not ssl' --valkey-url=${CLUSTER_URL}
