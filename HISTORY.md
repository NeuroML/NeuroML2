History of changes in the official releases of NeuroML 2/LEMS
-------------------------------------------------------------

Note, this records major changes/updates in not just the [NeuroML Schemas](https://github.com/NeuroML/NeuroML2/tree/master/Schemas/NeuroML2)
and [LEMS](https://github.com/LEMS/LEMS), but also the Python ([libNeuroML](https://github.com/NeuralEnsemble/libNeuroML) and
[PyLEMS](https://github.com/LEMS/pylems)) and Java ([jLEMS](https://github.com/LEMS/jLEMS),
[org.neuroml.model](https://github.com/NeuroML/org.neuroml.model), [jNeuroML](https://github.com/NeuroML/jNeuroML), etc.) libraries.

**Only contributors who are not [NeuroML Editors](https://docs.neuroml.org/NeuroMLOrg/Board.html) are specifically pointed out below.**

v2.3.1 / 2024-08-25
--------------------

* **Renamed the main Schema from NeuroML_v2.3.xsd to [NeuroML_v2.3.1.xsd](https://github.com/NeuroML/NeuroML2/blob/master/Schemas/NeuroML2/NeuroML_v2.3.1).**

* Adds support for external <morphology>/<biophysicalProperties> in cell element. Also simulator mappings for NEURON/NetPyNE support this. See [here](https://docs.neuroml.org/Userdocs/ImportingMorphologyFiles.html#neuroml2) for more details. Multiple examples of NeuroML2/LEMS files using this feature can be found [here](https://github.com/NeuroML/NeuroML2/tree/development/LEMSexamples/morphologies). 

* pyNeuroML analysis feature updates: better support for analysing kinetic scheme based channels in `pynml-channelanalysis`; better support for plotting generated spike trains with `pynml-plotspikes`.

* Improved testing of Java based libraries on latest versions of Java and recent Mac OS versions. 

* Improved support for adding RDF annotations to NeuroML files.

* Added ability to load (a subset of) XPPAUT files with `pynml-xpp` and export the model to LEMS or back to XPPAUT.

* Improvements to handling of SBML and SED-ML files - added to pynml ability to validate both formats, or run SED-ML files which refer to SBML models using simulator tellurium.

* Added option to archive NeuroML models as COMBINE Archives with `pynml-archive`.

* Initial support for sending archived NeuroML models to Biosimulations.org for simulation.

* Improved ability for pynml and related tools to detect the correct file type (NeuroML or LEMS) for the appropriate export/simulation option, and give advice when an incorrect file is provided. 

* Updates to `pynml-plotmorph` for plotting morphologies in 2D, and in 3D with VisPy.


v2.3 / 2023-09-20
--------------------

* **Renamed the main Schema from NeuroML_v2.2.xsd to [NeuroML_v2.3.xsd](https://github.com/NeuroML/NeuroML2/blob/master/Schemas/NeuroML2/NeuroML_v2.3).**

* Added new cell type `<hindmarshRose1984Cell>`

* jLEMS adds features including option for reportFile in [LEMS Simulation files](https://docs.neuroml.org/Userdocs/LEMSSimulation.html) to use `__SIMULATOR__` and `__TIMESTAMP__` placeholders, and `<Meta>` for simulator specific info, e.g. variable time step in NEURON, see [example](https://github.com/OpenSourceBrain/NEURONShowcase/blob/master/HH/LEMS_NML2_Ex5_DetCell_cvode.xml).

* Tested Java libraries up to Java 19 & Python libraries up to Python v3.11

* Significant usability updates to libNeuroML & pyNeuroML - see individual releases.

* Update to how units are generated in NEURON mod file for greater consistency, and validity with `modlunit` checks. See [here](https://github.com/NeuroML/org.neuroml.export/pull/107/files).

* Toolchain and models on OSB all tested against NEURON v8.1, NEST v3.3 and PyNN v0.10.1

* Support for generation of EDEN Python scripts with `jnml MyLEMS.xml -eden` in jNeuroML and pyNeuroML, and many more tests with EDEN simulator (v0.2.2)

* NeuroMLlite updated to work with Arbor v0.8.1

* Significant updates in NeuroMLlite to work with MDF: https://github.com/ModECI/MDF/tree/main/examples/NeuroML

* See individual package change logs/released versions:
   - NeuroML2: https://github.com/NeuroML/NeuroML2/releases/tag/v1.9.1
   - jLEMS: https://github.com/LEMS/jLEMS/releases/tag/v0.10.8
   - org.neuroml.model.injectingplugin: https://github.com/NeuroML/org.neuroml.model.injectingplugin/releases/tag/v1.9.1
   - org.neuroml1.model: https://github.com/NeuroML/org.neuroml1.model/releases/tag/v1.9.1
   - org.neuroml.model: https://github.com/NeuroML/org.neuroml.model/releases/tag/v1.9.1
   - org.neuroml.export: https://github.com/NeuroML/org.neuroml.export/releases/tag/v1.9.1
   - org.neuroml.import: https://github.com/NeuroML/org.neuroml.import/releases/tag/v1.9.1
   - jNeuroML: https://github.com/NeuroML/jNeuroML/releases/tag/v0.12.4

   - pylems: https://github.com/LEMS/pylems/releases/tag/v0.6.4
   - libNeuroML: https://github.com/NeuralEnsemble/libNeuroML/releases/tag/v0.5.5
   - NeuroMLlite: https://github.com/NeuroML/NeuroMLlite/releases/tag/v0.5.7
   - pyNeuroML: https://github.com/NeuroML/pyNeuroML/releases/tag/v1.1.1

...

v2.2 / 2021-12-15
--------------------

* **Renamed the main Schema from NeuroML_v2.1.xsd to [NeuroML_v2.2.xsd](https://github.com/NeuroML/NeuroML2/blob/master/Schemas/NeuroML2/NeuroML_v2.2).**

* Significant updates to documentation in NeuroML LEMS XML definitions. Have been propagated to core documentation e.g. https://docs.neuroml.org/Userdocs/Schemas/Networks.html

* Major changes to pyNeuroML & libNeuroML to aid usability. These updates have been reflected in the NeuroML user guides & other documentation, e.g.: https://docs.neuroml.org/Userdocs/GettingStarted.html

* Updates to automated testing of Python & Java libraries: all moved to GitHub Actions (for overview see [here](https://github.com/NeuroML/.github/tree/main/testsheet)); updated to test on latest version of Python & Java and Windows/Mac.

* Removed `ValueAcrossSegOrSegGroup` (https://github.com/NeuroML/NeuroML2/pull/165 that fixes https://github.com/NeuroML/NeuroML2/issues/162) and update any elements using it to directly include `Value` and `SegmentGroup` attributes. This allows their correct validation.


v2.1 / 2021-03-22
--------------------

* **Renamed the main Schema from NeuroML_v2.0.xsd to [NeuroML_v2.1.xsd](https://github.com/NeuroML/NeuroML2/blob/master/Schemas/NeuroML2/NeuroML_v2.1).**

* The main updates for this release were infrastructure related, mainly updates for **Python 3 compatibility** and enhanced testing and documentation.

* Documentation for the NeuroML specification and core libraries was consolidated at http://docs.neuroml.org. Thanks to [Ankur Sinha](https://github.com/sanjayankur31).

* [libNeuroML](https://docs.neuroml.org/Userdocs/Software/libNeuroML.html) was updated with improved Python 3 support, along with better helper methods for handling cells, see https://github.com/NeuralEnsemble/libNeuroML/blob/development/notebooks/CellMorphology.ipynb

* [pyNeuroML](https://docs.neuroml.org/Userdocs/Software/pyNeuroML.html) had many updates to improve the user experience and make as many jNeuroML features as possible accessible through it.

* [NeuroMLlite](https://docs.neuroml.org/Userdocs/Software/NeuroMLlite.html) had significant updates, with initial support for [Arbor](https://arbor-sim.github.io/), [Brian2](https://briansimulator.org/), [SONATA](https://github.com/AllenInstitute/sonata) and [ModECI MDF](http://www.modeci.org/).

* [NetPyNE](https://netpyne.org) support in jNeuroML was extended and improved

* The C++ API for NeuroML, [NeuroML_API](https://github.com/NeuroML/NeuroML_API) has been updated to use the latest Schema.


v2.0 / 2020-04-06
--------------------

* **Renamed the main Schema from NeuroML_v2beta5.xsd to [NeuroML_v2.0.xsd](https://github.com/NeuroML/NeuroML2/blob/master/Schemas/NeuroML2/NeuroML_v2.0).**
  Changes outlined below are reflected in the new schema

_Example NeuroML models_

* The standard NeuroML examples have been updated/revised (and tests added) to ensure as many as possible of them run when converted to NEURON via jNeuroML.

_Export formats_

* Improved export to graphical view of LEMS ComponentTypes, e.g. try: jnml LEMS_NML2_Ex2_Izh.xml  -graph

* Improved/retested export to SBML & SED-ML. Added export option -sbml-sedml, which converts LEMS file to SBML format with a SED-ML file describing the experiment to run. Successfully tested with Tellurium SBML simulator.

* Minor updates to improve export to Moose. Latest developments with Moose support outlined here: https://github.com/NeuroML/NeuroML2/issues/94


v2beta5 / 2019-11-05
--------------------

* **Renamed the main Schema from NeuroML_v2beta4.xsd to [NeuroML_v2beta5.xsd](https://github.com/NeuroML/NeuroML2/blob/master/Schemas/NeuroML2/NeuroML_v2beta5.xsd).**
  Changes outlined below are reflected in the new schema

_Core NeuroML elements_

* Allows **weighted electrical and continuous connections** ([examples](https://github.com/NeuroML/NeuroML2/blob/development/LEMSexamples/LEMS_NML2_Ex26_Weights.xml))

* Allows **weighted inputs** (e.g. define one pulseGenerator and have individually weighted inputs from this to each cell in population; [examples](https://github.com/NeuroML/NeuroML2/blob/development/LEMSexamples/LEMS_NML2_Ex26_Weights.xml))

* Adds `<channelDensityVShift>` which can be used to **add a channel with an explicit vshift parameter** (e.g. adjust activation variable s by 10mV; [example](https://github.com/OpenSourceBrain/PospischilEtAl2008/blob/f8f663c69d7ca74b3b323a7ed436ab84994ddb59/NeuroML2/channels/Na/Na.cell.nml#L36))

* Adds input type `<spikeGeneratorRefPoisson>`, a **poisson spike generator with a refractory period** ([example](https://github.com/NeuroML/NeuroML2/blob/development/LEMSexamples/LEMS_NML2_Ex16_Inputs.xml))

* Adds `<voltageClampTriple>`, a **voltage clamp with 3 clamp levels** ([definition](https://github.com/NeuroML/NeuroML2/blob/207bbc301e59a741a0a1c7adc140037a1330a513/NeuroML2CoreTypes/Inputs.xml#L664))

* Adds `<doubleSynapse>`, a **single synaptic mechanism containing multiple currents**, which can be used e.g. to bundle an AMPA and NMDA on one synapse, which can in turn be used for individual connections in projections ([example](https://github.com/NeuroML/NeuroML2/blob/development/LEMSexamples/LEMS_NML2_Ex27_MultiSynapses.xml))

_LEMS functionality_

* Add option to put **reportFile="report.txt"** in Target component in `<Lems>` to save short report of simulator version, runtime etc. ([example](https://github.com/NeuroML/NeuroML2/blob/development/LEMSexamples/LEMS_NML2_Ex5_DetCell.xml#L11))

_Bug fixes_

* Fixes for **issue with statistics of stochastic spiking inputs at very high frequencies** (see [issue](https://github.com/NeuroML/NeuroML2/issues/121))

_Simulator support_

* Extensive support for **mapping to NetPyNE format** added (generate this with: jnml LEMS_Model.xml -netpyne). For examples and tests see: https://github.com/OpenSourceBrain/NetPyNEShowcase

* Much better interaction with PyNN, see examples at https://github.com/OpenSourceBrain/PyNNShowcase and https://github.com/NeuroML/NeuroML2/issues/73. Also see examples mentioned in OSB paper (below).

* Improved mapping to **Brian & Brian2**, see https://github.com/OpenSourceBrain/BrianShowcase

* Improved mapping to **Moose** (single compartment cells only), see https://github.com/OpenSourceBrain/MOOSEShowcase

_Library support_

* Better support for accessing **all jnml functionality through Python in pyNeuroML**, see https://github.com/NeuroML/pyNeuroML

* New **C++ API**: https://github.com/NeuroML/NeuroML_API. Thanks to [Jonathan Cooper](https://github.com/jonc125).

* New **Matlab API**: https://github.com/NeuroML/NeuroMLToolbox. Thanks to [Jonathan Cooper](https://github.com/jonc125)

_Models_

* Most of the NeuroML models as featured in the [Open Source Brain paper](https://www.cell.com/neuron/fulltext/S0896-6273(19)30444-1) are compliant with v2beta5

v2beta4 / 2016-6-27
-------------------

* **Renamed the main Schema from NeuroML_v2beta3.xsd to [NeuroML_v2beta4.xsd](https://github.com/NeuroML/NeuroML2/blob/master/Schemas/NeuroML2/NeuroML_v2beta4.xsd).**
  Changes outlined below are reflected in the new schema

_Cell types_

* **Added `<pinskyRinzelCA3Cell>`, based on Pinsky and Rinzel 1994.** See [here](http://www.opensourcebrain.org/projects/pinskyrinzelmodel) for more.
Thanks to [Justas Birgolas](https://github.com/JustasB) for this.

* **Added `<izhikevich2007Cell>`**. Version of Izhikevich cell from 2007 book has been added. Main advantage is explicit capacitance, allowing dimensional currents
to be applied. See [here](https://github.com/OpenSourceBrain/IzhikevichModel/tree/master/NeuroML2) for more.

* **Added `<fitzHughNagumo1969Cell>`** Version of FitzHugh Nagumo cell based on 1969 model. See https://github.com/OpenSourceBrain/FitzHugh-Nagumo. Thanks to
[Boris Marin](https://github.com/borismarin).

* **Cells with 2 independent pools of Ca2+**. The `<cell2CaPools>` has been added for cells with 2 independent pools of Ca2+. This may be required where some Ca channels contribute
to changes in internal [Ca2+] (thus influencing [Ca2+] dependent K channels) and some don't (just pass charge). See [here](https://github.com/OpenSourceBrain/SolinasEtAl-GolgiCell/blob/master/NeuroML2/Golgi.cell.nml) for example.
Thanks to [Rokas Stanislovas](https://github.com/RokasSt).

_Synapses_

* **Gap junctions and analog synapses.** Added support for gap junctions ([example](https://github.com/NeuroML/NeuroML2/blob/master/examples/NML2_GapJunctionInstances.nml))
and analog synapses ([example](https://github.com/NeuroML/NeuroML2/blob/master/examples/NML2_AnalogSynapses.nml)). Supported in jLEMS and NEURON mapping
via [jNeuroML](https://github.com/NeuroML/jNeuroML).

* **New synapse types `<alphaSynapse>` and `<expThreeSynapse>`.** Added synapse types `<alphaSynapse>` (rise time = decay time) and `<expThreeSynapse>`
(1 exponential rise time, 2 decay times). See [here](https://github.com/NeuroML/NeuroML2/blob/master/examples/NML2_SynapseTypes.nml)

* **Improved recording from multiple synapses on multicompartmental cells**. See [here](https://github.com/NeuroML/NeuroML2/blob/master/LEMSexamples/LEMS_NML2_Ex25_MultiComp.xml)
for an example of recording/saving of different variables on multiple synapses on a multicompartmental cell.

_Ion channels/conductances_

* **Fractional conductances from sub gates in channels**. Added `<gateFractional>` which allows multiple children `<subGate>`, each of which has a fractional conductance.
See [here](https://github.com/NeuroML/NeuroML2/blob/master/LEMSexamples/LEMS_NML2_Ex24_FractionalConductance.xml) and
[here](https://github.com/OpenSourceBrain/AllenInstituteNeuroML/blob/master/CellTypesDatabase/models/NeuroML2/Kv2like.channel.nml). Thanks to
[Boris Marin](https://github.com/borismarin).

* **Gate with instantaneous opening**. Added `<gateHHInstantaneous>` with only `<steadyState>` child, i.e. no time dependence of opening, just a voltage dependent steady state.

* **Improved support for kinetic scheme based channels**. Channels based on kinetic schemes (using `<ionChannelKS>` and `<gateKS>`) have much better support in
jLEMS and NEURON via [jNeuroML](https://github.com/NeuroML/jNeuroML), see [here](https://github.com/OpenSourceBrain/AllenInstituteNeuroML/blob/master/CellTypesDatabase/models/NeuroML2/NaV.channel.nml) and
[here](https://github.com/OpenSourceBrain/SolinasEtAl-GolgiCell/blob/master/NeuroML2/Golgi_KAHP.channel.nml).

* **Alternative GHK channel density.** Added a second mechanism for specifying channel densities which lead to currents based on the Goldman Hodgkin Katz current, `<channelDensityGHK2>`.
See [here](https://github.com/OpenSourceBrain/ghk-nernst/blob/master/NeuroML2/ghk2_na_k_ca.nml) and
[here](https://github.com/andrisecker/CA1-Oriens-Lacunosum-Moleculare---Lawrence-et-al.-2006/blob/master/NeuroML2/LawrenceOLM.cell.nml) for examples.
Thanks to [András Ecker](https://github.com/andrisecker).

_Network_

* **Connections with weights and delays**. Better support in jNeuroML and NEURON for `<connectionWD>`. See [here](https://github.com/NeuroML/NeuroML2/blob/master/LEMSexamples/LEMS_NML2_Ex12_Net2.xml).

_Input/output_

* **Additional spiking/current inputs**. New types of inputs to apply to cells, including `<poissonFiringSynapse>`, `<transientPoissonFiringSynapse>`, `<timedSynapticInput>` and
`<compoundInput>`. See [here](https://github.com/NeuroML/NeuroML2/blob/master/examples/NML2_Inputs.nml) for examples. Thanks to [Rokas Stanislovas](https://github.com/RokasSt).

* **Saving of spike times.** Added support for specifying in LEMS simulation file that spike times should be saved (as opposed to full membrane potential trace). See
[here](https://github.com/NeuroML/NeuroML2/blob/master/LEMSexamples/LEMS_NML2_Ex23_Spiketimes.xml) for more. Thanks to [Finn Krewer](https://github.com/FinnK).

_Testing_

* **OMV tests on core examples.** Added tests on core LEMS examples using OMV (Open Source Brain Model Validation framework). This can be used to run the examples
with jNeuroML and other simulators and ensure correct spike times, etc. See the [LEMSexamples/test](https://github.com/NeuroML/NeuroML2/tree/development/LEMSexamples/test)
directory. The output from these tests on 16 different simulator configurations can be seen [here](https://travis-ci.org/OpenSourceBrain/osb-model-validation).
Thanks to
[Boris Marin](https://github.com/borismarin).

* **OMV tests on OSB models.** There are ~30 different projects on OSB using NeuroML 2 which are being tested using the OMV framework. See
[this page](https://travis-ci.org/OpenSourceBrain/osb-model-validation) for an overview of these.

_Tool support_

* **libNeuroML updated**. [libNeuroML](https://github.com/NeuralEnsemble/libNeuroML), the Python API for reading/writing NeuroML2 has been regenerated from the
latest Schema. There is also better support for Python 3.

* **pyNeuroML is a well tested alternative to jNeuroML**. [pyNeuroML](https://github.com/NeuroML/pyNeuroML) is a Python module which can be installed with
`pip install pyNeuroML` and can be used to access most of the functionality of [jNeuroML](https://github.com/NeuroML/jNeuroML). Thanks to
[Rick Gerkin](https://github.com/rgerkin) for testing/updating.

_Documentation_

* **Consolidated web page for documentation.** Direct links to all schemas, papers, libraries, tools, examples, contact details are now available on one page: https://neuroml.org/getneuroml


v2beta3 / 2014-9-11
-------------------

* **Renamed the main Schema from NeuroML_v2beta2.xsd to [NeuroML_v2beta3.xsd](https://github.com/NeuroML/NeuroML2/blob/master/Schemas/NeuroML2/NeuroML_v2beta3.xsd).**
  Changes outlined below are reflected in the new schema

* **Inhomogeneous channel densities.** The elements for expressing non uniform channel densities (`<inhomogeneousParam>`,
  `<variableParameter>`, `<inhomogeneousValue>`, etc. which were based on those used in NeuroML v1.8.1) have been updated, retested
  and improved. See https://raw.githubusercontent.com/OpenSourceBrain/L5bPyrCellHayEtAl2011/master/neuroConstruct/generatedNeuroML2/L5PC.cell.nml
  for an example.

* **Export compatibility check.** There is now an explicit check in jNeuroML when a NeuroML 2 model is exported to a
  specific format (e.g. Brian, MATLAB, XPP) to see whether the model features present are supported in the export,
  e.g. MATLAB does not support networks but running with jLEMS does, Brain export does not support multicompartmental
  neurons but NEURON does, etc. A detailed error will be thrown by jnml, e.g. `jnml LEMS_NML2_Ex3_Net.xml -xpp`. See
  [here](https://github.com/NeuroML/org.neuroml.export/blob/development/src/main/java/org/neuroml/export/ModelFeature.java)
  for more on current model features.

* **NEURON export via jNeuroML improved.** A number of improvements to the export of NEURON code from NeuroML 2 models
  have been made, including: much improved support for mapping multicompartmental cells in NeuroML 2 to NEURON simulations;
  improved handling of channel densities with Nernst based reversal potential; handling of inhomogeneous channel densities
  mentioned above; better saving of data (matching jLEMS saved data files); option to automatically compile the generated
  mod files and/or run without NEURON GUI, e.g. `jnml MyLEMS.xml -neuron -nogui -run` (Linux only so far).

* **Restructured NeuroML2 repository.** with folders: [examples](https://github.com/NeuroML/NeuroML2/tree/master/examples)
  (for pure NML2 files), [LEMSexamples](https://github.com/NeuroML/NeuroML2/tree/master/LEMSexamples)  (for LEMS files using
  NML2 definitions) and [NeuroML2CoreTypes](https://github.com/NeuroML/NeuroML2/tree/master/NeuroML2CoreTypes)  (for the NML2
  ComponentType definitions)

* Allows a `<property>` element with tag/value attributes (as in NeuroML v1.8.1) in `<annotation>` element

* Updated & improved `<simpleSeriesResistance>` element & also works now when exported to NEURON

* Added `<gateHHratesTauInf>` for gates which use alpha and beta, but also have generic expressions for tau and inf using alpha
  and beta in non standard ways.

* Changed Kohm to kohm in standard unit definitions.

* Licences have been added to each of the repositories on https://github.com/NeuroML and https://github.com/LEMS.




v2beta2 / 2014-3-5
------------------

* **Renamed the main Schema from NeuroML_v2beta1.xsd to [NeuroML_v2beta2.xsd](https://github.com/NeuroML/NeuroML2/blob/master/Schemas/NeuroML2/NeuroML_v2beta2.xsd).**
  Changes outlined below are reflected in the new schema

* **Better support for GHK & Nernst.**
    There is better support for Goldman Hodgkin Katz currents (using the
    [channelDensityGHK](http://www.neuroml.org/NeuroML2CoreTypes/Cells.html#channelDensityGHK) element),
    as well as conductances whose reversal potentials are determined by the Nernst equation
    [channelDensityNernst](http://www.neuroml.org/NeuroML2CoreTypes/Cells.html#channelDensityNernst).
    See http://www.opensourcebrain.org/projects/ghk-nernst for more details
    and some working examples in LEMS/NeuroML2 which can be run & compared against NEURON versions.
    Thanks to Boris Marin for making up these examples & checking through the implementations in NeuroML.

* **Much better support in PyLEMS for NeuroML 2/LEMS models.**
    With this release PyLEMS is a much stabler option for simulating LEMS models in general & NeuroML 2 example models.
    See https://github.com/LEMS/pylems/blob/master/README.md for the latest details on PyLEMS support.
    PyLEMS has also been put on the Python Package Index and can be installed with: pip install PyLEMS

* **Better import & export of many formats using jNeuroML.**
    There have been significant improvements in the export & import options for a number of formats,
    including export of NEURON and import of SBML. See here:
    https://github.com/NeuroML/jNeuroML/blob/master/src/main/java/org/neuroml/JNeuroML.java
    for the range of export & import formats currently supported.

* **Added [baseSpikingCell](http://www.neuroml.org/NeuroML2CoreTypes/Cells.html#baseSpikingCell)**
    Added a ComponentType definition for baseSpikingCell (which indicates a cell that emits a spike), in between
    baseCell (which indicates any type of cell) and baseCellMembPot/baseCellMembPotDL (which are spike emitting cells
    with dimensional/dimensionless membrane potential)

* **Added [fixedFactorConcentrationModel](http://www.neuroml.org/NeuroML2CoreTypes/Cells.html#fixedFactorConcentrationModel)**
    There has been a new element added which specifies how internal [Ca2+] varies with incoming Ca2+ current: "A fixed
    factor rho is used to scale the incoming current INDEPENDENTLY OF THE SIZE OF THE COMPARTMENT to produce a
    concentration change." This formulation is used in many models, particularly based on some of Roger Traub's, e.g.
    https://github.com/OpenSourceBrain/ACnet2/blob/master/neuroConstruct/generatedNeuroML2/Ca_conc.nml

* **Ordering of channelDensity more restrictive.**
    In this release, the order of `<channelPopulation>`, `<channelDensity>`, `<channelDensityNernst>`,
    `<channelDensityGHK>` in `<membraneProperties>` is more restrictive; they have to appear in that order. See
    [here](https://github.com/NeuroML/NeuroML2/blob/development/Schemas/NeuroML2/NeuroML_v2beta2.xsd#L1040).
    This is due to the previous flexibility in the ordering in the last Schema producing some difficult to
    understand constructs in the generated code for libNeuroML (Python) & org.neuroml.model (Java).

* **Using log as opposed to ln in Channel.xml**
    Since ln is preferred to log for natural log in Python, Java & most programming languages, using this by default,
    see: https://github.com/NeuroML/NeuroML2/commit/89e600acb8e21ff0c511606156dc3d0197ed8959.
    Using ln in expressions will still be supported by jLEMS/jNeuroML, but is discouraged.

* **Updated the names used in complexType definitions in the Schema for some I&F cells**
    For example IaFTauCell -> [IafTauCell](https://github.com/NeuroML/NeuroML2/blob/development/Schemas/NeuroML2/NeuroML_v2beta2.xsd#L767)
    (note small f); this is more consistent with the NeuroML 2 element,
    iafTauCell, which is unchanged. However, the classes in the generated Python & Java APIs are updated to the
    new form, e.g. IafTauCell iaf = new IafTauCell();


v2beta1 / 2013-09-03
====================

* Renamed the main Schema from NeuroML_v2beta.xsd to NeuroML_v2beta1.xsd. Changes outlined below reflected in the schema

* Modified `<segment>` to ensure its id is only ever a non negative integer.
    This required defining a BaseWithoutId element. Requested by Subhasis Ray, who
    pointed out the type of the segment ids should be the same in `<segment id=X>`
    and `<parent segment=X>`.

* Connections with segment ids & fraction along.
    Added option to specify preSegmentId, preFractionAlong, etc. on connections, e.g.
    `<connection id="0" preCellId="../popA/0/dendCell" preSegmentId="0" preFractionAlong="0.5"
postCellId="../popB/0/dendCell" postSegmentId="1" postFractionAlong="1"/>`
    to allow detailed connectivity between multicompartmental cells. See examples/NML2_SegmentConnections.nml for valid example

* Restructure of NMDA/STP synapses.
    Previous elements nmdaSynapse and stpSynapse have been replaced by blockingPlasticSynapse
    which has optional child elements of types  basePlasticityMechanism and baseBlockMechanism.
    See examples/NML2_SynapseTypes.nml for examples of these. Thanks to Eugenio Piasini for overhauling these synapse types.


* networkWithTemperature added.
    The method for specifying the temperature to use for child elements of a network whose behaviour varies with
    temperature has been altered, `<networkWithTemperature ...>` is used now. See
    [here](http://sourceforge.net/mailarchive/forum.php?thread_name=51F66D10.2080604%40ucl.ac.uk&forum_name=neuroml-technology)
    for discussion on this. Example at NeuroML2CoreTypes/LEMS_NML2_Ex17_Tissue.xml

* Channel Density with reversal potential calculated by Nernst equation.
    Added support for channel densities where, instead of a fixed reversal potential, the internal and external
    concentrations of the ion flowing through are used to calculate reversal potential. See
    [here](http://www.neuroml.org/NeuroML2CoreTypes/Cells.html#channelDensityNernst) for more details
