#!/bin/bash

set -e

echo "saving input files for the best solution found ..."

if [ ! -e best ] ; then
    mkdir best
fi

cp -Rf ./RavenInput/ ./best/
exit 0

