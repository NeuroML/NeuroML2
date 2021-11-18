#!/bin/bash

# Copyright 2021 Ankur Sinha
# Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com> 
# File : format-xsds.sh
#
# format XSD files with xmllint

if [ -x "$(command -v xmllint)"  ]
then
    for i in *xsd
    do
        xmllint --format "$i" -o "$i".formatted
        mv "$i".formatted "$i"
    done
else
    echo "xmllint not found"
fi
