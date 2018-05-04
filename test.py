###
#    This script validates the local NeuroML2 definitions as LEMS
#    files and the NeuroML examples as NeuroML files. If any of these
#    is not valid, it will report a test failure.
#
#    It will also check for the consistency of the NeuroML and LEMS
#    files in this repo with the copies that are supposed to be
#    present in other local directories. Finally, it will check
#    whether the local jnml executable can validate the NeuroML
#    examples in the examples/ directory. It will report (though not
#    by throwing a full test failure, as this shouldn't really concern
#    this repo as long as the tests above pass) if any of these
#    conditions is not met.
#
#    Subject to change without notice.
###

import os
import sys
from lxml import etree
from urllib import urlopen

import subprocess
import filecmp

verbose = False
vverbose = False
if len(sys.argv) == 2 and sys.argv[1]=="-v":
    verbose = True
if len(sys.argv) == 2 and sys.argv[1]=="-vv":
    vverbose = True

lems_def_dir="NeuroML2CoreTypes"
lems_def_list=os.listdir(lems_def_dir)

lems_exs_dir="LEMSexamples"
lems_exs_list=os.listdir(lems_exs_dir)

lems_schema = "../LEMS/Schemas/LEMS/LEMS_v0.7.4.xsd"
lems_schema_file = urlopen(lems_schema)

lems_xmlschema_doc = etree.parse(lems_schema_file)
lems_xmlschema = etree.XMLSchema(lems_xmlschema_doc)

lems_master_ex_dir="../LEMS/examples"
lems_master_ex_list=os.listdir(lems_master_ex_dir)

nml2_schema_name = "NeuroML_v2beta5.xsd"
nml2_schema = "Schemas/NeuroML2/%s"%nml2_schema_name
nml2_schema_file = urlopen(nml2_schema)

nml2_xmlschema_doc = etree.parse(nml2_schema_file)
nml2_xmlschema = etree.XMLSchema(nml2_xmlschema_doc)

nml2_ex_dir="examples"
nml2_ex_list=os.listdir(nml2_ex_dir)

template_src_dir="../git/som-codegen"
template_java_dir="../org.neuroml.export/src/main/resources"
##template_python_dir="../pylems/lems/"
template_list=['cvode/cvode.vm', 'cvode/Makefile', 'matlab/matlab_ode.vm', 'modelica/main_class.vm', 'modelica/run.vm', 'xpp/xpp.vm']


def check_same_file(fileA, fileB):

    same = filecmp.cmp(fileA, fileB)
    if vverbose: print " -- Comparing files {} and {}...".format(fileA, fileB)
    if not same and verbose: print " -- Files {} and {} are different!".format(fileA, fileB)
    return same

def check_valid_lems(schema, document):
    tree = etree.parse(lems_def_dir + "/" + document)
    assert lems_xmlschema.validate(tree), "{} is not valid LEMS!".format(document)

def check_valid_neuroml(document):
    tree = etree.parse(nml2_ex_dir + "/" + document)
    assert nml2_xmlschema.validate(tree)

def check_jnml_validates_neuroml(document):
    p = subprocess.Popen(["jnml -validate "+ nml2_ex_dir+"/"+document], shell=True, stdout=subprocess.PIPE)
    p.communicate()
    return not bool(p.returncode), "{} is not valid NeuroML!".format(document)

def test_validate_lems_files():
    print("Validating LEMS files against: {}".format(lems_schema))
    for document in lems_def_list:
        if document.endswith("xml") and not document.startswith("LEMS") and not document.startswith("Ex"):
            yield check_valid_lems, lems_schema, document

def test_validate_neuroml_files():
    print("Validating NeuroML 2 files against: {}".format(nml2_schema))
    for document in nml2_ex_list:
        if document.endswith("nml"):
            yield check_valid_neuroml, document


if __name__ == '__main__':
    import nose
    print "--------------------------------------------------"
    print "    Checking local copies of NeuroML schemas"

    if not check_same_file('Schemas/NeuroML2/%s'%nml2_schema_name,  '../libNeuroML/neuroml/nml/%s'%nml2_schema_name):
        print("FAIL: NeuroML schemas in libNeuroML not in sync!")
    else:
        print("NeuroML schemas in libNeuroML are in sync.")


    if os.path.isdir('../neuroConstruct') and not check_same_file('Schemas/NeuroML2/NeuroML_v2alpha.xsd', '../neuroConstruct/NeuroML2/Schemas/NeuroML2/NeuroML_v2alpha.xsd'):
        print("FAIL: NeuroML alpha schemas in neuroConstruct not in sync!")
    else:
        print("NeuroML alpha schemas in neuroConstruct are in sync.")
        
    if os.path.isdir('../neuroConstruct') and not check_same_file('Schemas/NeuroML2/%s'%nml2_schema_name,  '../neuroConstruct/NeuroML2/Schemas/NeuroML2/%s'%nml2_schema_name):
        print("FAIL: NeuroML beta schemas in neuroConstruct not in sync!")
    else:
        print("NeuroML beta schemas in neuroConstruct are in sync.")
        
    if os.path.isdir('../git/NeuroMLWebsite') and not check_same_file('Schemas/NeuroML2/%s'%nml2_schema_name,  '../git/NeuroMLWebsite/public/schema/neuroml2/%s'%nml2_schema_name):
        print("FAIL: NeuroML beta schemas in NeuroMLWebsite not in sync!")
    else:
        print("NeuroML beta schemas in NeuroMLWebsite are in sync.")

    print "--------------------------------------------------"
    print "    Checking local copies of examples"
    
    are_files_identical_list = []
    for filename in lems_master_ex_list:
        if filename.endswith("xml"):
            main_ex = lems_master_ex_dir+"/"+filename
            copy_org_lems_ex = "../jLEMS/src/test/resources/"+filename
            are_files_identical_list.append(check_same_file(main_ex, copy_org_lems_ex))
    if not all(are_files_identical_list):
        print("FAIL: LEMS examples in jLEMS are not in sync!")
    else:
        print("LEMS examples in jLEMS are in sync.")

    are_files_identical_list = []
    for filename in lems_master_ex_list:
        if filename.endswith("xml"):
            main_ex = lems_master_ex_dir+"/"+filename
            copy_org_lems_ex = "../pylems/examples/"+filename
            are_files_identical_list.append(check_same_file(main_ex, copy_org_lems_ex))
    if not all(are_files_identical_list):
        print("FAIL: LEMS examples in pylems are not in sync!")
    else:
        print("LEMS examples in pylems are in sync.")
        

    are_files_identical_list = []
    for filename in template_list:
            src_template = template_src_dir+"/"+filename
            java_template = template_java_dir+"/"+filename
            are_files_identical_list.append(check_same_file(src_template, java_template))
    if not all(are_files_identical_list):
        print("FAIL: Templates for Java are not in sync!")
    else:
        print("LEMS Templates for Java are in sync.")

    print("-------------------------------------------------------")
    print("    Testing if jnml validates the NeuroML example files")
    not_validated_by_jnml =[]
    for document in nml2_ex_list:
        if document.endswith("nml"):
            if not check_jnml_validates_neuroml(document):
                not_validated_by_jnml.append(document)
                print("FAIL: jnml does not validate {}".format(document))
    if not not_validated_by_jnml:
        print("jnml validates all NeuroML example files.")


    if '-r' in sys.argv:

        print "--------------------------------------------------"
        print "    Testing execution of LEMS files using jLEMS"

        import subprocess
        import os
        lems_exs_list.sort()

        to_ignore = ['LEMS_NML2_Ex13_Instances.xml']
        for file in lems_exs_list:

            if file.endswith("xml") and file.startswith("LEMS") and not file in to_ignore:

                lems_file = '%s/%s'%(lems_exs_dir,file)
                print "Testing %s..." %(lems_file)

                #subprocess.call(['lems %s'%(lems_file)])
                #os.system('~/jLEMS/lems %s'%(lems_file))
                subprocess.call('jnml %s -nogui &'%(lems_file), shell=True)

    print("-------------------------------------------------------")
    print("    Validating NeuroML definitions and examples")
    nose.main()
