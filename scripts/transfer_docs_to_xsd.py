#!/usr/bin/env python3
"""
Copy over documentation from XML schema files to the XSD.

File: transfer_docs_to_xsd.py

Copyright 2021 Ankur Sinha
Author: NeuroML contributors
"""


import lxml.etree as ET
import re


xml_files = [
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

    # Remove spaces between dots and URL suffixes
    # introduced by previous tweaks
    suffixes = ["org", "com"]
    for suf in suffixes:
        text = text.replace(". " + suf, "." + suf)

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


def update_xsd():
    """Update the XSD documentation.

    This takes whatever is in the XML files and puts in the XSD, replacing
    anything that may be in the XSD already.
    """
    XSD_file = "../Schemas/NeuroML2/NeuroML_v2.2.xsd"
    XSD_file_new = "../Schemas/NeuroML2/NeuroML_v2.2_docs.xsd"
    try:
        xsdtree = ET.parse(XSD_file)
        xsdroot = xsdtree.getroot()
    except ET.XMLSyntaxError as e:
        print(f"Could not parse file {XSD_file}: {e}")

    xsdnamespaces = xsdroot.nsmap
    xsdnsinfo = xsdnamespaces['xs']
    complex_types = xsdroot.findall(".//xs:complexType", namespaces=xsdnamespaces)
    ct_list = []

    # iterate over all schema files
    # find it in the XSD, make changes
    for file in xml_files:
        xmlfile = "../NeuroML2CoreTypes/" + file
        print("Definitions: processing {}".format(xmlfile))
        try:
            xmltree = ET.parse(xmlfile)
            xmlroot = xmltree.getroot()
        except ET.XMLSyntaxError as e:
            print(f"Could not parse file {file}: {e}")
            continue
        xmlnamespaces = xmlroot.nsmap
        component_types = xmlroot.findall(".//ComponentType", namespaces=xmlnamespaces)

        for ct in component_types:
            ct_name = ct.attrib['name'].lower()
            ct_doc = re.sub(' +', ' ', ct.attrib['description']).replace("\n", " ").rstrip().lstrip()
            ct_doc += "\n"

            # find this in the schema
            for cxt in complex_types:
                cxt_name = cxt.attrib['name'].lower()
                doc_text = ""
                if cxt_name == ct_name:

                    # complex type documentation
                    doc_node = ct.find("./xs:annotation/xs:documentation",
                                       namespaces=xsdnamespaces)
                    # remove the existing doc node, we'll re-add a new one at
                    # the top of the complextype so that generateDS puts this
                    # documentation first in nml.py
                    if doc_node is not None:
                        if len(doc_node) > 1:
                            print("Warning: multiple doc elements found?")
                            for n in doc_node:
                                n.getparent().remove(n)
                        else:
                            doc_node.getparent().remove(doc_node)

                    # create new annotation at top of complextype
                    new_annotation = ET.Element('{' + xsdnsinfo + '}annotation')
                    ct.insert(0, new_annotation)
                    doc_node = ET.SubElement(new_annotation, '{' + xsdnsinfo + '}documentation')
                    doc_node.text = ct_doc + format_description(doc_text) + '\n'

                    # Parameter documentation
                    params = ct.findall("./Parameter", namespaces=xmlnamespaces)
                    for p in params:
                        pname = p.attrib['name']
                        pdim = p.attrib['dimension']
                        pdesc = None
                        pdoc = ""
                        if 'description' in p.attrib:
                            pdesc = format_description(p.attrib['description'])
                        # generateDS will say: <name> - pdoc
                        pdoc = "(dimension: {}){}".format(
                            pdim, ": " + pdesc if pdesc else ""
                        )
                        # create new document annotation for parameter
                        p_xsd_nodes = cxt.findall(".//xs:attribute", namespaces=xsdnamespaces)
                        for p_xsd_node in p_xsd_nodes:
                            if p_xsd_node.attrib['name'].lower() == pname.lower():

                                # remove existing doc
                                p_doc_node = p_xsd_node.find("./xs:annotation/xs:documentation",
                                                             namespaces=xsdnamespaces)
                                if p_doc_node is not None:
                                    p_doc_node.getparent().remove(p_doc_node)

                                p_annotation = ET.Element('{' + xsdnsinfo + '}annotation')
                                p_xsd_node.insert(0, p_annotation)
                                p_doc_node = ET.SubElement(p_annotation, '{' + xsdnsinfo + '}documentation')
                                p_doc_node.text = pdoc

    ET.indent(xsdtree)
    xsdtree.write(XSD_file_new, method="xml", xml_declaration=True)
    print("New file written to {}".format(XSD_file_new))
    print("Please check the differences before replacing the main file.")
    return ct_list


def compare_xml_xsd():
    """Compare what's defined in the XSD and in the XML."""

    XSD_file = "../Schemas/NeuroML2/NeuroML_v2.2.xsd"
    try:
        xsdtree = ET.parse(XSD_file)
        xsdroot = xsdtree.getroot()
    except ET.XMLSyntaxError as e:
        print(f"Could not parse file {XSD_file}: {e}")

    xsdnamespaces = xsdroot.nsmap
    complex_types = xsdroot.findall(".//xs:complexType", namespaces=xsdnamespaces)
    cxt_list = [ct.attrib['name'].lower() for ct in complex_types]
    cxt_list = set(cxt_list)

    component_types = []
    for file in xml_files:
        xmlfile = "../NeuroML2CoreTypes/" + file
        try:
            xmltree = ET.parse(xmlfile)
            xmlroot = xmltree.getroot()
        except ET.XMLSyntaxError as e:
            print(f"Could not parse file {file}: {e}")
            continue
        xmlnamespaces = xmlroot.nsmap
        component_types.extend(xmlroot.findall(".//ComponentType", namespaces=xmlnamespaces))
    ct_list = [ct.attrib['name'].lower() for ct in component_types]
    ct_list = set(ct_list)

    print()
    print("These are in the XML but not in the XSD: {}\n\n".format(cxt_list - ct_list))
    print("These are in the XSD but not in the XML: {}".format(ct_list - cxt_list))


if __name__ == "__main__":
    update_xsd()
    compare_xml_xsd()
