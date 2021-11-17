#!/usr/bin/env python3
"""
Copy over documentation from XML schema files to the XSD.

File: transfer_docs_to_xsd.py

Copyright 2021 Ankur Sinha
Author: NeuroML contributors
"""


import lxml.etree as ET
import re


def format_description(text):
    """Format the description.

    This is too complex to be done in the Jinja template. It can be done, but
    it'll be messy.

    - convert underscores in text to URLs and bold,
    - no need to convert asterisk, since they're underline in myAST already,
    - no need to format http:// URLs, since they're also handled automatically.

    :param text: text to process
    :type text: string
    :returns: converted string

    """
    if not text or len(text) == 0:
        return ""
    # Add spaces after these so we correctly split "(_gbase" type constructs
    puncts = ["(", ",", ";", "."]
    for punct in puncts:
        text = text.replace(punct, punct + " ")
    # Add spaces before these
    for punct in [")"]:
        text = text.replace(punct, " " + punct)

    words = text.split()
    text2 = ""
    for word in words:
        if len(word) > 0:
            if word.count('_') == 2:
                pre = word[0:word.find('_')]
                ct = word[word.find('_') + 1:word.rfind('_')]
                post = word[word.rfind('_') + 1:]
                word = "{} **{}** {}".format(pre, ct, post)
            elif word[0] == '_':
                word = "**{}** ".format(word[1:])

        text2 = text2 + word + " "
    return text2.rstrip()


def get_component_type_docs():
    """Get all component type documentation from the XML ComponentType definition files.
    :returns: TODO

    """
    schema_files = [
        "Cells.xml",
        "NeuroML2CoreTypes.xml",
        "Simulation.xml",
        "Channels.xml",
        "NeuroMLCoreCompTypes.xml",
        "Synapses.xml",
        "Inputs.xml",
        "NeuroMLCoreDimensions.xml",
        "Networks.xml",
        "PyNN.xml"
    ]
    component_type_docs = {}
    for file in schema_files:
        srcfile = "../NeuroML2CoreTypes/" + file
        print("Definitions: processing {}".format(srcfile))
        try:
            tree = ET.parse(srcfile)
            root = tree.getroot()
        except ET.XMLSyntaxError as e:
            print(f"Could not parse file {file}: {e}")
            continue
        namespaces = root.nsmap
        component_types = root.findall(".//ComponentType", namespaces=namespaces)
        for ct in component_types:
            ct_name = ct.attrib['name'].lower()
            ct_doc = re.sub(' +', ' ', ct.attrib['description']).replace("\n", " ").rstrip().lstrip()
            component_type_docs[ct_name] = ct_doc
    # print(component_type_docs)
    return component_type_docs


def update_xsd(documentation_dict, replace=True):
    """Update the XSD documentation.

    If replace is true, we replace the current text in the XSD. Otherwise, we
    combine the two texts.
    """
    XSD_file = "../Schemas/NeuroML2/NeuroML_v2.2.xsd"
    XSD_file_new = "../Schemas/NeuroML2/NeuroML_v2.2_docs.xsd"
    try:
        tree = ET.parse(XSD_file)
        root = tree.getroot()
    except ET.XMLSyntaxError as e:
        print(f"Could not parse file {XSD_file}: {e}")

    namespaces = root.nsmap
    nsinfo = namespaces['xs']
    print(namespaces)
    complex_types = root.findall(".//xs:complexType", namespaces=namespaces)
    ct_list = []
    for ct in complex_types:
        ct_name = ct.attrib['name'].lower()
        ct_list.append(ct_name)
        print("Schema: processing {}".format(ct_name))
        if ct_name in documentation_dict:
            doc_text = ""
            xml_doc = documentation_dict[ct_name]

            doc_node = ct.find("./xs:annotation/xs:documentation", namespaces=namespaces)
            doc_text = ""
            if doc_node is not None:
                print("Found documentation node in {}".format(ct_name))
                if len(doc_node) > 1:
                    print("Multiple doc elements found?")
                if replace:
                    doc_text = ""
                else:
                    doc_text = re.sub(' +', ' ', doc_node.text).replace("\n", " ").rstrip().lstrip()
            else:
                print("No documentation node found in {}. Creating new.".format(ct_name))
                new_annotation = ET.SubElement(ct, '{' + nsinfo + '}annotation')
                doc_node = ET.SubElement(new_annotation, '{' + nsinfo + '}documentation')
            doc_node.text = format_description(xml_doc + doc_text)

    ET.indent(tree)
    tree.write(XSD_file_new, method="xml", xml_declaration=True)
    print("New file written to {}".format(XSD_file_new))
    print("Please check the differences before replacing the main file.")
    return ct_list


if __name__ == "__main__":
    component_type_docs = get_component_type_docs()
    component_types_xsd = set(update_xsd(component_type_docs))
    component_types_xml = set(component_type_docs.keys())

    print()
    print("Following component types are defined in the XML but not the XSD: {}".format(component_types_xml - component_types_xsd))
    print()
    print("Following component types are defined in the XSD but not the XML: {}".format(component_types_xsd - component_types_xml))
