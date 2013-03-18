import os

import os.path as op
import subprocess

'''
try:
    from fabri3c.api import *
except ImportError as e:
    print "Problem loading Python module for Fabric"
'''

neuroml2_spec_repo = ['NeuroML/NeuroML2']

java_neuroml_repos = ['NeuroML/org.neuroml.model.injectingplugin',
                      'NeuroML/org.neuroml.model',
                      'NeuroML/org.neuroml1.model',
                      'NeuroML/org.neuroml.export',
                      'NeuroML/org.neuroml.import',
                      'NeuroML/jNeuroML']

libneuroml_repo = ['NeuralEnsemble/libNeuroML']

neuroml_repos = neuroml2_spec_repo + libneuroml_repo + java_neuroml_repos

jlems_repo = ['LEMS/jLEMS']

java_repos = java_neuroml_repos + jlems_repo

lems_spec_repos = ['LEMS/LEMS']

pylems_repos = ['LEMS/pylems']

lems_repos = jlems_repo + lems_spec_repos + pylems_repos

all_repos = neuroml_repos + lems_repos

# Set the prteferred method for cloning from GitHub
#github_pref = "HTTP"
github_pref = "SSH"
#github_pref = "Git Read-Only"

pre_gh={}
pre_gh["HTTP"]="https://github.com/openworm/"
pre_gh["SSH"]="git@github.com:openworm/"
pre_gh["Git Read-Only"]="git://github.com/openworm/"


for repo in all_repos:
    print "------ Updating: %s -------"%repo
    local_dir = ".."+os.sep+repo.split("/")[1]
    if not op.isdir(local_dir):
        print "Creating a new directory: "+local_dir
        subprocess.call("cd ..; pwd; git clone "%local_dir, shell=True)

    subprocess.call("cd %s; pwd; git pull"%local_dir, shell=True)
    