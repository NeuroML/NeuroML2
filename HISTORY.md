v2beta1 / 2013-XX-XX
--------------------

* Renamed the main Schema from NeuroML_v2beta.xsd to NeuroML_v2beta1.xsd
    Changes below reflected in the schema

* Modified `<segment>` to ensure its id is only ever a non negative integer. 
    This required defining a BaseWithoutId element. Requested by Subhasis Ray, who 
    pointed out the type of the segment ids should be the same in `<segment id=X>` 
    and `<parent segment=X>`.

* Connections with segment ids & fraction along
    Added option to specify preSegmentId, preFractionAlong, etc. on connections, e.g.
    <connection id="0" preCellId="../popA/0/dendCell" preSegmentId="0" preFractionAlong="0.5" postCellId="../popB/0/dendCell" postSegmentId="1" postFractionAlong="1"/>
    to allow detailed connectivity between multicompartmental cells.
    See examples/NML2_SegmentConnections.nml for valid example

* Restructure of NMDA/STP synapses
    Previous elements nmdaSynapse and stpSynapse have been replaced by blockingPlasticSynapse 
    which has optional child elements of types  basePlasticityMechanism and baseBlockMechanism.
    See examples/NML2_SynapseTypes.nml for examples of these 
    Thanks to Eugenio Piasini for overhauling these synapse types.


* networkWithTemperature added 
    Should this be added to master??


