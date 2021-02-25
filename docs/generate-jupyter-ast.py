#!/usr/bin/env python3
"""
Generate Jupyter-book MyAST sources for indices of the NeuroML comp_definition from
their XML sources.

File: generate-jupyter-ast.py

Copyright 2021 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""

from datetime import date
from decimal import Decimal
from decimal import getcontext
from lems.model.model import Model
import requests
import tempfile
import asttemplates

# To display correct conversion values, we limit the precision context to 2
# places (required by Hz). Higher precisions, such as the default machine
# precision include the usual issues with floating point arithmetic and do not
# display exact conversions
#
# References: https://docs.python.org/3/tutorial/floatingpoint.html
# https://docs.python.org/3/library/decimal.html#module-decimal
getcontext().prec = 5

# Main worker bits start here
comp_definitions = ["Cells", "Synapses", "Channels", "Inputs", "Networks", "PyNN", "NeuroMLCoreDimensions", "NeuroMLCoreCompTypes"]
#  comp_definitions = ["NeuroMLCoreCompTypes", "Cells", "Synapses"]

comp_types = {}
comp_type_src = {}
comp_type_desc = {}
ordered_comp_types = {}

GitHubCompSources = "https://github.com/NeuroML/NeuroML2/blob/master/NeuroML2CoreTypes/"
GitHubCompSourcesRaw = "https://raw.githubusercontent.com/NeuroML/NeuroML2/master/NeuroML2CoreTypes/"
nml_version = "2.1"
nml_branch = "master"
nml_date = date.today().strftime("%d/%m/%y")
nml_commit = "6e4643d0eaa7246982b351a01e28856eeb320500"


def get_component_types(srcdir):
    """Obtain a list of all defined component types.


    Does not return anything. Fills global variables.
    It works in two stages.

    First, from the XML comp_definition files, we read all the models and get the required metadata:
    - names,
    - the xml source file in which it is defined,
    - description of the component.

    Next, we read all the XML files to get an ordered list of components.

    We get this list by reading the XML files and parsing them rather than
    using the LEMS API used above because the LEMS API does not guarantee what
    order the components will be returned in. By using the file as the source
    here, we ensure that we get the component list in the same order in which
    they are defined in the XML file.

    :returns: nothing

    """
    for comp_definition in comp_definitions:
        fullpath = "{}/{}.xml".format(srcdir, comp_definition)
        """Stage 1"""
        model = Model(include_includes=False)
        model.import_from_file(fullpath)

        for comp_type in model.component_types:
            comp_types[comp_type.name] = comp_type
            comp_type_src[comp_type.name] = comp_definition
            comp_type_desc[comp_type.name] = comp_type.description if comp_type.description is not None else "ComponentType: " + comp_type.name

        """Stage 2"""
        ordered_comp_type_list = []
        with open(fullpath) as fp:
            for line in fp:
                s = '<ComponentType name='
                if s in line:
                    i = line.index(s)
                    e = line.find('"', i + len(s) + 1)
                    comp_type_defined = line[i + len(s) + 1: e]
                    ordered_comp_type_list.append(comp_type_defined)
        ordered_comp_types[comp_definition] = ordered_comp_type_list


def get_extended_from_comp_type(comp_type_name):
    """Get name of the parent ComponentType.

    :param comp_type_name: name of component type to get parent for.
    :type comp_type_name: str.

    :returns: parent ComponentType if derived from one.
    """
    if comp_type_name not in comp_types:
        return None
    extCompTypeName = comp_types[comp_type_name].extends
    if extCompTypeName is None:
        return None
    return comp_types[extCompTypeName]


def main(srcdir, destdir):
    """Main parser and generator function.

    :param srcdir: directory holding source NeuroML Core Type XML files
    :type srcdir: str
    :param destdir: directory where generated files should be stored
    :type destdir: str

    :returns: nothing
    """

    # If not defined or empty, download a new copy to a temporary directory
    if not srcdir or src == "":
        print("No src directory specified. Downloading files to a temporary directory..")
        tempdir = tempfile.TemporaryDirectory()
        tmpsrcdir = tempdir.name
        print("Temporariy directory: {}".format(tmpsrcdir))
        for comp_definition in comp_definitions:
            url = GitHubCompSourcesRaw + comp_definition + ".xml"
            srcfile = tmpsrcdir + "/" + comp_definition + ".xml"
            print("Downloading {} to {}".format(url, srcfile))
            with open(srcfile, 'wb') as f:
                response = requests.get(url)
                f.write(response.content)
    else:
        tmpsrcdir = srcdir

    # read the downloaded files
    get_component_types(tmpsrcdir)

    if not destdir or destdir == "":
        destdir = "."
    print("Output files will be written to {} directory".format(destdir))

    for comp_definition in comp_definitions:
        fullpath = "{}/{}.xml".format(tmpsrcdir, comp_definition)
        outputfile = "{}/{}.md".format(destdir, comp_definition)
        """Stage 1"""
        model = Model(include_includes=False)
        model.import_from_file(fullpath)

        print("Processing {}".format(fullpath))
        print("Writing output to {}".format(outputfile))
        ast_doc = open(outputfile, 'w')

        """Page header"""
        print(asttemplates.page_header.render(
            comp_definition=comp_definition,
            comp_description=model.description,
            GitHubCompSources=GitHubCompSources,
            nml_version=nml_version, nml_branch=nml_branch,
            nml_date=nml_date,
            nml_commit=nml_commit
        ), file=ast_doc)

        """Dimensions and units"""
        if "Dimensions" in comp_definition:
            dimensions = model.dimensions
            dimensions = sorted(dimensions, key=lambda dim: dim.name)
            units = model.units
            units = sorted(units, key=lambda unit: unit.symbol)

            # lables are translated as lowercase in jupyter, so we append two
            # consecutive underscores to differentiate same ones, like M and m.
            symbols = []
            for unit in units:
                if unit.symbol.lower() in symbols:
                    unit.symbol = unit.symbol + "__"
                symbols.append(unit.symbol.lower())

            print(asttemplates.dimension.render(comp_definition=comp_definition,
                                                dimensions=dimensions, units=units), file=ast_doc)

            # Get factors
            for unit in units:
                unit.factors = []
                for unit2 in units:
                    if unit.symbol != unit2.symbol and unit.dimension == unit2.dimension:
                        factor1 = model.get_numeric_value("1%s" % unit.symbol.replace("__", ""), unit.dimension)
                        factor2 = model.get_numeric_value("1%s" % unit2.symbol.replace("__", ""), unit2.dimension)
                        conversion = float(Decimal(factor1) / Decimal(factor2))
                        if conversion > 10000:
                            conversion = '{:.2e}'.format(conversion)
                        else:
                            conversion = '{}'.format(conversion)
                        if conversion.endswith('.0'):
                            conversion = conversion[:-2]
                        unit.factors.append([conversion, unit2.symbol])

            print(asttemplates.unit.render(comp_definition=comp_definition,
                                           units=units), file=ast_doc)

        """Component Types"""
        for o_comp_type in ordered_comp_types[comp_definition]:
            o_comp_type = o_comp_type.replace('rdf:', 'rdf_')
            comp_type = model.component_types[o_comp_type]

            """Header"""
            cno = None
            if " cno_00" in str(comp_type.description):
                cno = comp_type.description.split(" ")[-1]
                comp_type.description = comp_type.description.replace(cno, "")
            if not comp_type.description.endswith("."):
                comp_type.description += "."
            print(asttemplates.comp.render(comp_definition=comp_definition,
                                           comp_type=comp_type, cno=cno), file=ast_doc)

            """Process parameters, derived parameters, texts, paths, expsures,
            requirements and ports"""
            params = {}
            derived_params = {}
            texts = {}
            paths = {}
            exposures = {}
            requirements = {}
            eventPorts = {}

            """Get lists of them all"""
            for param in comp_type.parameters:
                params[param] = comp_type.name
            for derived_param in comp_type.derived_parameters:
                derived_params[derived_param] = comp_type.name
            for text in comp_type.texts:
                texts[text] = comp_type.name
            for path in comp_type.paths:
                paths[path] = comp_type.paths
            for exp in comp_type.exposures:
                exposures[exp] = comp_type.name
            for req in comp_type.requirements:
                requirements[req] = comp_type.name
            for ep in comp_type.event_ports:
                eventPorts[ep] = comp_type.name

            """Get parent ComponentType if derived from one."""
            extd_comp_type = get_extended_from_comp_type(comp_type.name)

            """Recursively go up the tree and get attributes inherited from ancestors."""
            while extd_comp_type is not None:
                for param in extd_comp_type.parameters:
                    pk = params.copy().keys()
                    for pp0 in pk:
                        if pp0.name == param.name:
                            del params[pp0]
                    params[param] = extd_comp_type.name
                for derived_param in extd_comp_type.derived_parameters:
                    derived_params[derived_param] = extd_comp_type.name
                for text in extd_comp_type.texts:
                    texts[text] = extd_comp_type.name
                for path in extd_comp_type.paths:
                    paths[path] = extd_comp_type.paths
                for exp in extd_comp_type.exposures:
                    ek = exposures.copy().keys()
                    for ee0 in ek:
                        if ee0.name == exp.name:
                            del exposures[ee0]
                    exposures[exp] = extd_comp_type.name
                for req in extd_comp_type.requirements:
                    requirements[req] = extd_comp_type.name
                for ep in extd_comp_type.event_ports:
                    eventPorts[ep] = extd_comp_type.name

                """Recurse up the next parent"""
                extd_comp_type = get_extended_from_comp_type(extd_comp_type.name)

            if len(params) > 0:
                keysort = sorted(params.keys(), key=lambda param: param.name)
                print(asttemplates.params.render(title="Parameters",
                                                 comp_type=comp_type,
                                                 entries=params,
                                                 keysort=keysort), file=ast_doc)
            if len(derived_params) > 0:
                keysort = sorted(derived_params.keys(), key=lambda derived_param: derived_param.name)
                print(asttemplates.params.render(title="Derived parameters",
                                                 comp_type=comp_type,
                                                 entries=derived_params,
                                                 keysort=keysort), file=ast_doc)

            if len(comp_type.texts) > 0:  # TODO: Check if Text elements are inherited...
                print(asttemplates.misc1c.render(title="Text fields",
                                                 textlist=comp_type.texts), file=ast_doc)
            if len(comp_type.paths) > 0:  # TODO: Check if Path elements are inherited...
                print(asttemplates.misc1c.render(title="Paths",
                                                 textlist=comp_type.paths), file=ast_doc)
            if len(comp_type.component_references) > 0:
                print(asttemplates.misc2c.render(title="Component References",
                                                 textlist=comp_type.component_references), file=ast_doc)

            if len(comp_type.children) > 0:
                childlist = []
                childrenlist = []
                for child_or_children in comp_type.children:
                    if not child_or_children.multiple:
                        childlist.append(child_or_children)
                    else:
                        childrenlist.append(child_or_children)

                if len(childlist) > 0:
                    print(asttemplates.misc2c.render(title="Child list",
                                                     textlist=childlist), file=ast_doc)
                if len(childrenlist) > 0:
                    print(asttemplates.misc2c.render(title="Children list",
                                                     textlist=childrenlist), file=ast_doc)

            if len(comp_type.constants) > 0:
                print(asttemplates.constants.render(title="Constants",
                                                    textlist=comp_type.constants), file=ast_doc)

            if len(exposures) > 0:
                keysort = sorted(exposures, key=lambda entry: entry.name)
                print(asttemplates.exposures.render(title="Exposures",
                                                    comp_type=comp_type,
                                                    entries=exposures,
                                                    keysort=keysort), file=ast_doc)

            if len(requirements) > 0:
                keysort = sorted(requirements, key=lambda entry: entry.name)
                print(asttemplates.requirements.render(title="Requirements",
                                                       comp_type=comp_type,
                                                       entries=requirements,
                                                       keysort=keysort), file=ast_doc)

            if len(eventPorts) > 0:
                keysort = sorted(eventPorts, key=lambda entry: entry.name)
                print(asttemplates.eventPorts.render(title="Event Ports",
                                                     comp_type=comp_type,
                                                     entries=eventPorts,
                                                     keysort=keysort), file=ast_doc)

            if len(comp_type.attachments) > 0:
                print(asttemplates.misc2c.render(title="Attachments",
                                                 textlist=comp_type.attachments), file=ast_doc)

            if comp_type.dynamics and comp_type.dynamics.has_content():
                print(asttemplates.dynamics.render(title="Dynamics",
                                                   comp_type=comp_type), file=ast_doc)
        ast_doc.close()
        print("Finished processing {}".format(fullpath))

    if not srcdir:
        tempdir.cleanup()


if __name__ == "__main__":
    src = ""
    destdir = "output"
    main(src, destdir)
