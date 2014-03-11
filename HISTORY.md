History of changes in the official releases of NeuroML 2
--------------------------------------------------------

Note, this records major changes/updates in not just the [NeuroML Schemas](https://github.com/NeuroML/NeuroML2/tree/master/Schemas/NeuroML2) and [LEMS](https://github.com/LEMS/LEMS), but also the Python ([libNeuroML](https://github.com/NeuralEnsemble/libNeuroML) and [PyLEMS](https://github.com/LEMS/pylems)) and Java ([jLEMS](https://github.com/LEMS/jLEMS), [org.neuroml.model](https://github.com/NeuroML/org.neuroml.model), [jNeuroML](https://github.com/NeuroML/jNeuroML), etc.) libraries.

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


