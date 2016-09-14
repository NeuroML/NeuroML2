History of changes in the official releases of NeuroML 2/LEMS
-------------------------------------------------------------

Note, this records major changes/updates in not just the [NeuroML Schemas](https://github.com/NeuroML/NeuroML2/tree/master/Schemas/NeuroML2) 
and [LEMS](https://github.com/LEMS/LEMS), but also the Python ([libNeuroML](https://github.com/NeuralEnsemble/libNeuroML) and 
[PyLEMS](https://github.com/LEMS/pylems)) and Java ([jLEMS](https://github.com/LEMS/jLEMS), 
[org.neuroml.model](https://github.com/NeuroML/org.neuroml.model), [jNeuroML](https://github.com/NeuroML/jNeuroML), etc.) libraries.

Only contributors who are not [NeuroML Editors](https://neuroml.org/editors) are specifically pointed out below.

v2beta5 / 2016-??-??
--------------------


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


