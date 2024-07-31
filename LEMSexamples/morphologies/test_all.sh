#!/bin/bash
set -ex

pynml -validate C*nml *cell.nml *channel.nml 

pynml-summary pyr_soma_m_in_b_in.cell.nml -v
pynml-summary pyr_soma_m_in_b_out.cell.nml -v
pynml-summary pyr_soma_m_out_b_in.cell.nml -v
pynml-summary pyr_soma_m_out_b_out.cell.nml -v

pynml LEMS_m_in_b_in.xml -nogui

pynml LEMS_m_in_b_in.xml -neuron -run -nogui
pynml LEMS_m_in_b_out.xml -neuron -run -nogui
pynml LEMS_m_out_b_in.xml -neuron -run -nogui
pynml LEMS_m_out_b_out.xml -neuron -run -nogui

pynml LEMS_m_in_b_in.xml -netpyne -run
pynml LEMS_m_in_b_out.xml -netpyne -run
pynml LEMS_m_out_b_in.xml -netpyne -run
pynml LEMS_m_out_b_out.xml -netpyne -run

pynml LEMS_pyrfull_in.xml -neuron -run -nogui
pynml LEMS_pyrfull_in.xml -netpyne -run

pynml LEMS_pyrfull_out.xml -neuron -run -nogui
pynml LEMS_pyrfull_out.xml -netpyne  -run 

echo "All tests completed!"
