Files starting with NML2_ in this folder will be valid against the latest
version of the NeuroML schema (and quite possibly a few earlier ones) in ../Schemas/NeuroML2/

To validate these files using `jnml`, run:

```
jnml -validate <NML file>
```

To validate all files at once, run:

```
jnml -validate *.nml
```

If you'd like to use `pynml`, use:

```
pynml <NML file> -validate
```

`pynml` does not take multiple file arguments, so to validate all the files in
this directory, use:

```
for i in *.nml; do pynml $i -validate; done
```

See also https://docs.neuroml.org/Userdocs/ValidatingNeuroMLModels.html. If the validation fails, please file an issue.
