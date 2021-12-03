#!/bin/bash

# Copyright 2021 Ankur Sinha
# Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
# File : format-xsd.sh
#
# format XSD file with xmllint


if [ "$#" -ne 1 ]
then
    echo "Please provide the XSD file to format as an argument"
    exit 1
fi

if [ -x "$(command -v xmllint)"  ]
then
    echo "Formatting $1"
    xmllint --format "$1" -o "$1".formatted
    mv "$1".formatted "$1"
else
    echo "xmllint not found"
fi
