Files starting with NML2_ in this folder will be valid against ../Schemas/NeuroML2/NeuroML_v2beta.xsd

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

If the validation fails, please file an issue.
