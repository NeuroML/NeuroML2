v2beta2 / 2013-12-11

* Renamed the main Schema from NeuroML_v2beta1.xsd to NeuroML_v2beta2.xsd. Changes outlined below reflected in the schema

* Better support for GHK...

* Update to fixedFactorConc...

* PyLEMS

* Ordering of channelDensity





v2beta1 / 2013-09-03
--------------------

* Renamed the main Schema from NeuroML_v2beta.xsd to NeuroML_v2beta1.xsd. Changes outlined below reflected in the schema

* Modified `<segment>` to ensure its id is only ever a non negative integer. 
    This required defining a BaseWithoutId element. Requested by Subhasis Ray, who 
    pointed out the type of the segment ids should be the same in `<segment id=X>` 
    and `<parent segment=X>`.

* Connections with segment ids & fraction along.
    Added option to specify preSegmentId, preFractionAlong, etc. on connections, e.g.
    `<connection id="0" preCellId="../popA/0/dendCell" preSegmentId="0" preFractionAlong="0.5" postCellId="../popB/0/dendCell" postSegmentId="1" postFractionAlong="1"/>`
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


