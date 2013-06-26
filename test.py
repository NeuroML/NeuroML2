###
#     Temporary script to test beta specification & examples.
#
#     Subject to change without notice!!!
###

import os
import sys
from lxml import etree
from urllib import urlopen

import subprocess
import filecmp
import unittest
import logging

lems_def_dir="NeuroML2CoreTypes"
lems_def_list=os.listdir(lems_def_dir)

lems_schema = "../LEMS/Schemas/LEMS/LEMS_v0.7.xsd"
lems_schema_file = urlopen(lems_schema)

lems_xmlschema_doc = etree.parse(lems_schema_file)
lems_xmlschema = etree.XMLSchema(lems_xmlschema_doc)

lems_ex_dir="../LEMS/examples"
lems_ex_list=os.listdir(lems_ex_dir)

nml2_schema = "Schemas/NeuroML2/NeuroML_v2beta.xsd"
nml2_schema_file = urlopen(nml2_schema)

nml2_xmlschema_doc = etree.parse(nml2_schema_file)
nml2_xmlschema = etree.XMLSchema(nml2_xmlschema_doc)

nml2_ex_dir="examples"
nml2_ex_list=os.listdir(nml2_ex_dir)

def checkSameFile(fileA, fileB):
    print "Comparing {} to {}".format(fileA, fileB)
    return filecmp.cmp(fileA, fileB)

def check_valid_LEMS(schema, document):
    tree = etree.parse(lems_def_dir+"/"+document)
    assert lems_xmlschema.validate(tree), "{} is not valid LEMS!".format(document)

def check_valid_NeuroML(document):
    #doc = etree.parse(nml2_ex_dir+"/"+file)
    #valid = nml2_xmlschema.validate(doc)
    p = subprocess.Popen(["jnml -validate "+ nml2_ex_dir+"/"+document], shell=True, stdout=subprocess.PIPE)
    p.communicate()
    assert not bool(p.returncode), "{} is not valid NeuroML!".format(document)

def test_validate_LEMS_files():
    print("Validating LEMS files against: {}".format(lems_schema))
    for document in lems_def_list:
        if document.endswith("xml") and not document.startswith("LEMS") and not document.startswith("Ex"):
            yield check_valid_LEMS, lems_schema, document


def test_validate_NeuroML_files():
    print("Validating NeuroML 2 files against: {}".format(nml2_schema))
    for document in nml2_ex_list:
        if document.endswith("nml"):
            yield check_valid_NeuroML, document


if __name__ == '__main__':
    import nose
    print "--------------------------------------------------"
    print "    Checking local copies of NeuroML schemas"

    if not checkSameFile('Schemas/NeuroML2/NeuroML_v2beta.xsd',  '../libNeuroML/neuroml/nml/NeuroML_v2beta.xsd'):
        print("FAIL: NeuroML schemas in libNeuroML not in sync!")

    if not checkSameFile('Schemas/NeuroML2/NeuroML_v2alpha.xsd', '../org.neuroml.model/src/main/resources/Schemas/NeuroML2/NeuroML_v2alpha.xsd'):
        print("FAIL: NeuroML alpha schemas in org.neuroml.model not in sync!")
    if not checkSameFile('Schemas/NeuroML2/NeuroML_v2beta.xsd',  '../org.neuroml.model/src/main/resources/Schemas/NeuroML2/NeuroML_v2beta.xsd'):
        print("FAIL: NeuroML beta schemas in org.neuroml.model not in sync!")


    if os.path.isdir('../Cvapp-NeuroMorpho.org') and not checkSameFile('Schemas/NeuroML2/NeuroML_v2alpha.xsd', '../Cvapp-NeuroMorpho.org/Schemas/NeuroML2/NeuroML_v2alpha.xsd'):
        print("FAIL: NeuroML alpha schemas in Cvapp-NeuroMorpho.org not in sync!")
    if os.path.isdir('../Cvapp-NeuroMorpho.org') and not checkSameFile('Schemas/NeuroML2/NeuroML_v2beta.xsd',  '../Cvapp-NeuroMorpho.org/Schemas/NeuroML2/NeuroML_v2beta.xsd'):
        print("FAIL: NeuroML beta schemas in Cvapp-NeuroMorpho.org not in sync!")

    if os.path.isdir('../neuroConstruct') and not checkSameFile('Schemas/NeuroML2/NeuroML_v2alpha.xsd', '../neuroConstruct/NeuroML2/Schemas/NeuroML2/NeuroML_v2alpha.xsd'):
        print("FAIL: NeuroML alpha schemas in neuroConstruct not in sync!")
    if os.path.isdir('../neuroConstruct') and not checkSameFile('Schemas/NeuroML2/NeuroML_v2beta.xsd',  '../neuroConstruct/NeuroML2/Schemas/NeuroML2/NeuroML_v2beta.xsd'):
        print("FAIL: NeuroML beta schemas in neuroConstruct not in sync!")

    print "--------------------------------------------------"
    print "    Checking local copies of Comp Type defs & examples"

    are_files_identical_list = []
    for filename in lems_def_list:
        if filename.endswith("xml") and not filename.startswith("Ex"):
            main_def = lems_def_dir+"/"+filename
            copy_org_neuroml_model = "../org.neuroml.model/src/main/resources/"+lems_def_dir+"/"+filename
            are_files_identical_list.append(checkSameFile(main_def, copy_org_neuroml_model))
    if not all(are_files_identical_list):
        print("FAIL: NeuroML core component types definitions in org.neuroml.model are not in sync!")

    are_files_identical_list = []
    for filename in nml2_ex_list:
        if filename.endswith("nml"):
            main_ex = nml2_ex_dir+"/"+filename
            copy_org_neuroml_model = "../org.neuroml.model/src/main/resources/"+nml2_ex_dir+"/"+filename
            are_files_identical_list.append(checkSameFile(main_ex, copy_org_neuroml_model))
    if not all(are_files_identical_list):
        print("FAIL: NeuroML examples in org.neuroml.model are not in sync!")

    are_files_identical_list = []
    for filename in lems_ex_list:
        if filename.endswith("xml"):
            main_ex = lems_ex_dir+"/"+filename
            copy_org_lems_ex = "../jLEMS/src/test/resources/"+filename
            are_files_identical_list.append(checkSameFile(main_ex, copy_org_lems_ex))
    if not all(are_files_identical_list):
        print("FAIL: LEMS examples in jLEMS are not in sync!")

    are_files_identical_list = []
    for filename in lems_ex_list:
        if filename.endswith("xml"):
            main_ex = lems_ex_dir+"/"+filename
            copy_org_lems_ex = "../pylems/examples/"+filename
            are_files_identical_list.append(checkSameFile(main_ex, copy_org_lems_ex))
    if not all(are_files_identical_list):
        print("FAIL: LEMS examples in pylems are not in sync!")


    if '-r' in sys.argv:

        print "--------------------------------------------------"
        print "    Testing execution of LEMS files using jLEMS"

        import subprocess, os
        lems_def_list.sort()

        to_ignore = ['LEMS_NML2_Ex13_Instances.xml']
        for file in lems_def_list:

            if file.endswith("xml") and file.startswith("LEMS") and not file in to_ignore:

                lems_file = '%s/%s'%(lems_def_dir,file)
                print "Testing %s..." %(lems_file)

                #subprocess.call(['lems %s'%(lems_file)])
                #os.system('~/jLEMS/lems %s'%(lems_file))
                subprocess.call('jnml %s -nogui &'%(lems_file), shell=True)

    nose.main()
