## Examples with tests for various ways to include `<morphology>` and `<biophysicalProperties>` in `<cell>`


See https://github.com/NeuroML/NeuroML2/issues/150 for background.

Cells with morphologies and biophysical properties can be expressed as:

```xml
    <cell id="pyr_soma_m_in_b_in">
...
        <morphology id="morph0">

            <segment ...>
            ...

        </morphology>

        <biophysicalProperties id="biophys1">
        ...
        </biophysicalProperties>

    </cell>
```
or
```xml
    <cell id="pyr_soma_m_out_b_out" morphology="morph0" biophysicalProperties="biophys1">
        ...
    </cell>

    <!-- Potentially in other files... -->

    <morphology id="morph0">

        <segment ...>
        ...

    </morphology>

    <biophysicalProperties id="biophys1">
    ...
    </biophysicalProperties>

```
See [pyr_soma_m_in_b_in.cell.nml](pyr_soma_m_in_b_in.cell.nml), [pyr_soma_m_out_b_in.cell.nml](pyr_soma_m_out_b_in.cell.nml), [pyr_soma_m_in_b_out.cell.nml](pyr_soma_m_in_b_out.cell.nml), [pyr_full_out.cell.nml](pyr_full_out.cell.nml) etc.



