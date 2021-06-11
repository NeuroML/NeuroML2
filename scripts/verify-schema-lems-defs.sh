#!/bin/bash

# Copyright 2021 NeuroML contributors
# Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com> 
# File : scripts/verify-schema-lems-defs.sh
#
# This file generates a diff between the complex types defined in the XSD
# schema file, and the component types defined in the LEMS definition files.
# Note that all component types and complex types are converted to lower case
# for comparison here.


SCHEMA_FILE="../Schemas/NeuroML2/NeuroML_v2.2.xsd"
SCHEMA_FILE_OUTPUT="schema-complex-types.txt"
LEMS_FILES_DIR="../NeuroML2CoreTypes/"
LEMS_FILES_OUTPUT="lems-component-types.txt"
DIFF_FILE="schema-vs-lems.diff"


function get_complex_types() {
    echo "Extracting complex type definitions from $SCHEMA_FILE"
    echo "Storing outputs in $SCHEMA_FILE_OUTPUT"
    grep -h -E -o "xs:complexType name=\"([[:alnum:]])+\"" $SCHEMA_FILE | sed -e 's/xs:complexType.*name="\(.*\)"/\L\1/' | sort -h | uniq > $SCHEMA_FILE_OUTPUT
}

function get_component_types() {
    echo "Extracting component type definitions from LEMS files in $LEMS_FILES_DIR"
    echo "Storing outputs in $LEMS_FILES_OUTPUT"
    grep -h -E -o "ComponentType name=\"([[:alnum:]])+\"" $LEMS_FILES_DIR/*.xml | sed -e 's/ComponentType.*name="\(.*\)"/\L\1/' | sort -h | uniq > $LEMS_FILES_OUTPUT
}

function generate_diff() {
    echo "Storing diff in $DIFF_FILE"
    diff -u $SCHEMA_FILE_OUTPUT $LEMS_FILES_OUTPUT > $DIFF_FILE
}

get_complex_types && get_component_types && generate_diff
